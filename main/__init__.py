import os
from flask import Flask
from flask_socketio import SocketIO

# The main module stores the app and socketio objects, so they can be imported throughout the app

app_name = "my_flask_app"

template_dir = os.path.abspath('./static')

app = Flask(app_name, template_folder=template_dir)
socketio = SocketIO(app)
