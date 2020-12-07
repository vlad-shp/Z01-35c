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
    isRead = db.Column(db.Boolean, default=False)

    @classmethod
    @jsonapi_rpc(http_methods=['POST'])
    def GetMessagesByWriterAndRecipientUsers(cls, writer_user, recipient_user):
        """
            description : GetMessagesByWriterAndRecipientUsers
            summary: GetMessagesByWriterAndRecipientUsers
            args:
                writer_user: "string"
                recipient_user: "string"
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
                                                            "messages":{
                                                                "type": "array",
                                                                "items": {
                                                                    "type":"object",
                                                                    "properties":{
                                                                        "id":{
                                                                                "type":"integer",
                                                                            },
                                                                        "recipient_user":{
                                                                                "type":"string",
                                                                            },
                                                                        "send_time":{
                                                                                "type": "string",
                                                                                "format": "datetime"
                                                                            },
                                                                        "text":{
                                                                                "type":"string",
                                                                            },
                                                                        "writer_user":{
                                                                                "type":"string",
                                                                            },

                                                                    }
                                                                }
                                                            }
                                                    }
                                                }
                                        }
                                }
                            }
                        }
        """
        content = {"messages": []}

        # db.session.query(User).filter_by(login=writer_user).first().isOnline = True
        # db.session.commit()

        def helpFunk(recipient_user_, writer_user_):
            for msg in db.session.query(Message).filter_by(recipient_user=recipient_user_,
                                                           writer_user=writer_user_).all():
                msg.isRead = True
                message = dict()

                message["id"] = msg.id
                message["writer_user"] = msg.writer_user
                message["recipient_user"] = msg.recipient_user
                message["send_time"] = msg.send_time
                message["text"] = msg.text
                content["messages"].append(message)

        helpFunk(recipient_user, writer_user)
        helpFunk(writer_user, recipient_user)

        return content


class User(BaseModel):
    """
        description: My user description
    """

    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, default="John Doe", unique=True)
    password = db.Column(db.String, default="")
    isOnline = db.Column(db.Boolean, default=False)

    @classmethod
    @jsonapi_rpc(http_methods=['POST'])
    def SignIn(cls, login, password):
        """
            description : SignIn
            summary: SignIn
            args:
                login: "string"
                password: "string"
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
        user = db.session.query(User).filter_by(login=login).first()
        if user is None or password != user.password or user.isOnline:
            return {"result": "failed"}
        user.isOnline = True
        db.session.add(user)
        db.session.commit()
        return {"result": "success"}

    @classmethod
    @jsonapi_rpc(http_methods=['POST'])
    def SetOffline(cls, login):
        """
            description : SetOnline
            summary: SetOnline
            args:
                login: "string"
        """
        db.session.query(User).filter_by(login=login).first().isOnline = False
        db.session.commit()

    @classmethod
    @jsonapi_rpc(http_methods=['POST'])
    def Registration(cls, login, password):
        """
            description : Registration
            summary: Registration
            args:
                login: "string"
                password: "string"
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
        user = db.session.query(User).filter_by(login=login).first()
        if user is not None:
            return {"result": "failed"}
        user = User(login=login, password=password)
        db.session.add(user)
        db.session.commit()
        return {"result": "success"}

    @classmethod
    @jsonapi_rpc(http_methods=['POST'])
    def SendMail(cls, sender_name, recipient_name, message_content):
        """
        description : SendMail
        summary: SendMail
        args:
            sender_name: sender_name
            recipient_name: recipient_name
            message_content: message_content
        """

        message = Message(writer_user=sender_name, recipient_user=recipient_name, text=message_content,
                          send_time=datetime.datetime.now())
        db.session.add(message)
        db.session.commit()
        return {"result": "success"}

    @classmethod
    @jsonapi_rpc(http_methods=['GET'])
    def GetUsersOnline(cls, *args, **some_body_key):
        """
            description : GetUsersOnline
            summary: GetUsersOnline
            responses:
                200:
                    description: "UsersOnline"
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
                                                        "users":{
                                                            "type":"array",
                                                            "items":"string"
                                                        }
                                                    }
                                                }
                                            }
                                    }
                            }
                        }
        """
        content = {"users": []}
        for user in db.session.query(User).filter_by(isOnline=True).all():
            content["users"].append(user.login)
        return content


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

app.config.update(SQLALCHEMY_DATABASE_URI="sqlite:///chat.db",
                  DEBUG=True)  # DEBUG will also show safrs log messages + exception messages


@app.route("/")
def goto_api():
    return redirect(API_PREFIX)


if __name__ == "__main__":
    HOST = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
    start_api(HOST, PORT)

    app.run(host=HOST, port=PORT, threaded=False)
