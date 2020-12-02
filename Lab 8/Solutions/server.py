import sys
import os
import datetime
from flask import Flask, redirect, send_from_directory
from flask_sqlalchemy import SQLAlchemy

try:
    from flask_admin import Admin
    from flask_admin.contrib import sqla
except:
    print("Failed to import flask-admin")
from safrs import SAFRSAPI
from safrs import SAFRSBase  # db Mixin
from safrs import SAFRSFormattedResponse
from safrs import jsonapi_rpc
import json
from functools import wraps


# This html will be rendered in the swagger UI
description = """
based on: https://github.com/thomaxxl/safrs
"""

db = SQLAlchemy()

def test_decorator(f):
    @wraps(f)
    def fwrapper(*args, **kwargs):
        result = f(*args, **kwargs)
        result.status_code = 200
        #result.headers['Location'] = 'https://blah/bleh'
        #result.data = json.dumps({'hoho' : 'ddd' })
        return result
    return fwrapper

class BaseModel(SAFRSBase, db.Model):
    __abstract__ = True

class Message(BaseModel):
    """
        description: My message description
    """
    __tablename__ = "Messages"

    id = db.Column(db.Integer, primary_key=True)
    writer_user = db.Column(db.String)
    recipient_user = db.Column(db.String)
    text = db.Column(db.String)
    send_time = db.Column(db.DateTime, default=datetime.datetime.now())

    custom_decorators = [test_decorator]

    def __str__(self):
        return f'{self.text}'

    @classmethod
    @jsonapi_rpc(http_methods=['GET'])
    def GetMessagesByUserName(cls, *args, **some_body_key):
        """
            description : Enter to varargs name
            summary: GetMessagesByUserName
            responses:
                200:
                    description: "Good"
                    schema:
                       {
                            "type":"object",
                            "properties":{
                                "meta":{
                                        "type":"object",
                                        "properties":{
                                            "result":{
                                                "type":"object",
                                                "properties":{
                                                    "id":{
                                                            "type":"array",
                                                            "items":"string"
                                                        },
                                                    "writer_user":{
                                                            "type":"array",
                                                            "items":"string"
                                                        },
                                                    "recipient_user":{
                                                            "type":"array",
                                                            "items":"string"
                                                        },
                                                    "send_time":{
                                                            "type":"array",
                                                            "items":"string"
                                                        },
                                                    "text":{
                                                            "type":"array",
                                                            "items":"string"
                                                        },

                                                    }
                                                }
                                            }
                                    }
                            }
                        }
        """
        content = {"id": [], "writer_user": [], "recipient_user": [], "send_time": [], "text": []}
        for msg in db.session.query(Message).filter_by(recipient_user=some_body_key['varargs']).all():
            content["id"].append(str(msg.id))
            content["writer_user"].append(str(msg.writer_user))
            content["recipient_user"].append(str(msg.recipient_user))
            content["send_time"].append(str(msg.send_time))
            content["text"].append(str(msg.text))

        db.session.query(Message).filter_by(recipient_user=some_body_key['varargs']).delete()
        db.session.commit()

        return content


class User(BaseModel):
    """
        description: My user description
    """

    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, default="John Doe", unique=True)

    @classmethod
    @jsonapi_rpc(http_methods=['GET'])
    def GetAuthenticationStatus(cls, *args, **some_body_key):
        """
            description : Enter to varargs user name
            summary: GetAuthenticationStatus
            responses:
                200:
                    description: "Good"
                    schema:
                       {
                            "type":"object",
                            "properties":{
                                "meta":{
                                        "type":"object",
                                        "properties":{
                                            "result":{
                                                "type":"object",
                                                "properties":{
                                                        "result":"string",
                                                    }
                                                }
                                            }
                                    }
                            }
                        }
        """
        if db.session.query(User).filter_by(name=some_body_key['varargs']).first() is not None:
            return {"result": "failed"}
        user = User(name=some_body_key['varargs'])
        db.session.add(user)
        db.session.commit()
        return {"result": "success"}

    @classmethod
    @jsonapi_rpc(http_methods=['POST'])
    def SendMail(cls, sender_name, recipient_name, message_content):
        """
        args:
            sender_name: sender_name
            recipient_name: recipient_name
            message_content: message_content
        """

        message = Message(writer_user=sender_name, recipient_user=recipient_name, text=message_content)
        db.session.add(message)
        db.session.commit()
        return {"result": "success"}

# API app initialization:
# Create the instances and exposes the classes


def start_api(swagger_host="127.0.0.1", PORT=None):
    # Add startswith methods so we can perform lookups from the frontend

    # Needed because we don't want to implicitly commit when using flask-admin
    SAFRSBase.db_commit = False

    with app.app_context():
        db.init_app(app)
        db.create_all()

        custom_swagger = {
            "info": {"title": "Mini chat"},
        }  # Customized swagger will be merged

        api = SAFRSAPI(
            app,
            host=swagger_host,
            port=PORT,
            prefix=API_PREFIX,
            custom_swagger=custom_swagger,
            schemes=["http"],
            description=description,
        )

        for model in [User, Message]:
            # Create an API endpoint
            api.expose_object(model)

        # see if we can add the flask-admin views
        try:
            admin = Admin(app, url="/admin")
            for model in [User, Message]:
                admin.add_view(sqla.ModelView(model, db.session))
        except Exception as exc:
            print(f"Failed to add flask-admin view {exc}")


API_PREFIX = "/api"  # swagger location
app = Flask("SAFRS Demo App", template_folder="/home/thomaxxl/mysite/templates")
app.secret_key = "not so secret"

app.config.update(SQLALCHEMY_DATABASE_URI="sqlite:///",
                  DEBUG=False)  # DEBUG will also show safrs log messages + exception messages

@app.route("/")
def goto_api():
    return redirect(API_PREFIX)


if __name__ == "__main__":
    HOST = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
    start_api(HOST, PORT)
    app.run(host=HOST, port=PORT, threaded=False)
