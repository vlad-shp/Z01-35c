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


class User(BaseModel):
    """
        description: My user description
    """

    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, default="John Doe", unique=True)
    password = db.Column(db.String, default="")
    isOnline = db.Column(db.Boolean, default=False)




# API app initialization:
# Create the instances and exposes the classes


def start_api(swagger_host="127.0.0.1", PORT=None):
    # Add startswith methods so we can perform lookups from the frontend

    # Needed because we don't want to implicitly commit when using flask-admin
    SAFRSBase.db_commit = False

    with app.app_context():
        db.init_app(app)
        db.create_all()


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


API_PREFIX = "/api"  # swagger location
app = Flask("SAFRS Demo App", template_folder="/home/thomaxxl/mysite/templates")
app.secret_key = "not so secret"

app.config.update(SQLALCHEMY_DATABASE_URI="sqlite:///",  # chat.db
                  DEBUG=False)  # DEBUG will also show safrs log messages + exception messages


@app.route("/")
def goto_api():
    return redirect(API_PREFIX)


if __name__ == "__main__":
    HOST = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
    start_api(HOST, PORT)

    app.run(host=HOST, port=PORT, threaded=False)
