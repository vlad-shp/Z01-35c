import sys
import os
import datetime
import time
from enum import Enum
from flask_socketio import SocketIO

from flask import Flask, redirect, send_from_directory
from flask_sqlalchemy import SQLAlchemy

try:
    from flask_admin import Admin
    from flask_admin.contrib import sqla
except:
    print("Failed to import flask-admin")

from safrs import SAFRSAPI
from safrs import SAFRSBase  # db Mixin
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
    writerUser = db.Column(db.String)
    recipientUser = db.Column(db.String)
    text = db.Column(db.String)
    sendTime = db.Column(db.DateTime, default=datetime.datetime.now())
    isRead = db.Column(db.Boolean, default=False)

    @classmethod
    @jsonapi_rpc(http_methods=['POST'])
    def GetAllMessageBetween2Users(cls, writerUser, recipientUser):
        """
            description : GetAllMessageBetween2Users
            summary: GetAllMessageBetween2Users
            args:
                writerUser: "string"
                recipientUser: "string"
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
                                                                        "recipientUser":{
                                                                                "type":"string",
                                                                            },
                                                                        "send_time":{
                                                                                "type": "string",
                                                                                "format": "datetime"
                                                                            },
                                                                        "text":{
                                                                                "type":"string",
                                                                            },
                                                                        "writerUser":{
                                                                                "type":"string",
                                                                            },
                                                                        "isRead":{
                                                                                "type":"boolean"
                                                                            }

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

        # db.session.query(User).filter_by(login=writerUser).first().isOnline = True
        # db.session.commit()

        def helpFunk(recipientUser_, writerUser_, mode=0):
            for msg in db.session.query(Message).filter_by(recipientUser=recipientUser_,
                                                           writerUser=writerUser_).all():
                message = dict()
                message["id"] = msg.id
                message["writerUser"] = msg.writerUser
                message["recipientUser"] = msg.recipientUser
                message["send_time"] = msg.sendTime
                message["text"] = msg.text
                message["isRead"] = msg.isRead
                if mode and msg.isRead == False:
                    db.session.query(Message).filter_by(id=msg.id).first().isRead = True
                    db.session.commit()
                    message["isRead"] = True

                content["messages"].append(message)

        helpFunk(recipientUser, writerUser)
        helpFunk(writerUser, recipientUser, 1)

        return content

    @classmethod
    @jsonapi_rpc(http_methods=['POST'])
    def GetUnreadMessagesInfo(cls, login):
        """
            description : GetUnreadMessagesInfo
            summary: GetUnreadMessagesInfo
            args:
                login: "string"
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
                                                                        "count":{
                                                                                "type":"integer",
                                                                            },
                                                                        "last":{
                                                                                "type":"string",
                                                                            },
                                                                        "lastMessageDateTime":{
                                                                                "type":"string",
                                                                                "format": "datetime",
                                                                            },
                                                                        "writer":{
                                                                                "type":"string",
                                                                            }
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
        for msg in db.session.query(Message).filter_by(recipientUser=login).all():

            isExistUserInContent = False
            for contentMsg in content["messages"]:
                if contentMsg["writer"] == msg.writerUser:
                    isExistUserInContent = True
                    if not msg.isRead:
                        contentMsg["count"] += 1
                    contentMsg["last"] = msg.text
                    contentMsg["lastMessageDateTime"] = msg.sendTime

                    break

            if not isExistUserInContent:
                message = dict()
                message["writer"] = msg.writerUser
                message["count"] = 1
                if msg.isRead:
                    message["count"] = 0
                message["last"] = msg.text
                message["lastMessageDateTime"] = msg.sendTime
                content["messages"].append(message)

        return content

    @classmethod
    @jsonapi_rpc(http_methods=['POST'])
    def SetMessageStatus(cls, idMessage, messageStatus):
        """
            description : SetMessageStatus
            summary: SetMessageStatus
            args:
                idMessage: "string"
                messageStatus: "string"
        """
        msg = db.session.query(Message).filter_by(id=idMessage).first()

        if messageStatus == "Read":
            msg.isRead = True
        else:
            msg.isRead = False

        db.session.commit()

        socketio.emit('userReadMessage', {'recipient': msg.recipientUser, 'writer': msg.writerUser})


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
                                                        "result":"string"
                                                    }
                                                }
                                            }
                                    }
                            }
                        }
        """
        user = db.session.query(User).filter_by(login=login).first()
        if user is None or password != user.password:
            return {"result": "failed"}
        if user.isOnline:
            return {"result": "online"}
        user.isOnline = True
        db.session.add(user)
        db.session.commit()
        socketio.emit('userSignIn', {'name': login})
        return {"result": "success"}

    @classmethod
    @jsonapi_rpc(http_methods=['POST'])
    def SignOut(cls, login):
        """
            description : SignOut
            summary: SignOut
            args:
                login: "string"
        """
        socketio.emit('userSignOut', {'name': login})
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
                                                        "result":"string"
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
        socketio.emit('userRegistered', {'name': login})
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
        idMessage = db.session.query(Message).count() + 1
        message = Message(id=idMessage, writerUser=sender_name, recipientUser=recipient_name, text=message_content,
                          sendTime=datetime.datetime.now())
        socketio.emit('userSendMessage',
                      {'send_date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
                       'sender_name': sender_name,
                       'recipient_name': recipient_name, 'text': message_content, 'id': message.id})
        db.session.add(message)
        db.session.commit()
        return {"result": "success"}

    @classmethod
    @jsonapi_rpc(http_methods=['GET'])
    def GetUsers(cls, *args, **some_body_key):
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
                                                            "type": "array",
                                                                "items": {
                                                                    "type":"object",
                                                                    "properties":{
                                                                        "name":{
                                                                                "type":"string",
                                                                            },
                                                                        "status":{
                                                                                "type":"boolean",
                                                                            }
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
        content = {"users": []}
        for user in db.session.query(User).all():
            userData ={"name":user.login, "status":user.isOnline}
            content["users"].append(userData)
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

        NR_INSTANCES = 200
        for i in range(NR_INSTANCES):
            user = User(login="User" + str(i), password="123", isOnline=False)
            db.session.add(user)

        # for i in range(3):
        #
        #     db.session.add(message)
        #     db.session.add(message0)
        #     # db.session.add(message1)
        #     # db.session.add(message2)
        #     # db.session.add(message3)
        #
        # db.session.commit()

        customSwagger = {
            "info": {"title": "Mini chat", "version": 1.0},

        }  # Customized swagger will be merged

        api = SAFRSAPI(
            app,
            host=swagger_host,
            port=PORT,
            prefix=API_PREFIX,
            custom_swagger=customSwagger,
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

SQLALCHEMY_TRACK_MODIFICATIONS = False
API_PREFIX = "/api"  # swagger location
app = Flask("SAFRS Demo App", template_folder="/home/thomaxxl/mysite/templates")
app.secret_key = "not so secret"

app.config.update(SQLALCHEMY_DATABASE_URI="sqlite:///",  # chat.db
                  DEBUG=False)  # DEBUG will also show safrs log messages + exception messages
socketio = SocketIO(app)


@app.route("/")
def goto_api():
    return redirect(API_PREFIX)


if __name__ == "__main__":
    HOST = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
    start_api(HOST, PORT)

    socketio.run(app)
    #app.run(host=HOST, port=PORT, threaded=False)
