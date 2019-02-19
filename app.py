from flask import Flask, make_response, jsonify, render_template
from werkzeug.exceptions import HTTPException
from mongoengine import connect
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO

from main import app, socketio

import config

from routes.user_routes import user_bp

import socket_bindings.paint_socket_bindings as paint_socket

# Init mongodb connection
connect(host=config.databases['mongodb']['uri'])

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = config.app['at_string']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = config.app['jwt_life_span']
app.config['JWT_HEADER_NAME'] = 'x-access-token'
app.config['JWT_HEADER_TYPE'] = ''
jwt = JWTManager(app)

# Register served static pages
@app.route(paint_socket.namespace)
def paint_socket_route():
    return render_template('paint-socket.html', namespace=paint_socket.namespace)


# Register App Blueprints
app.register_blueprint(user_bp, url_prefix='/api/user')

# Configure general error handler
@app.errorhandler(Exception)
def handle_error(e):
    err_code = 500
    if isinstance(e, HTTPException):
        err_code = e.code
    return make_response(jsonify({'success': False, 'msg': str(e)}), err_code)

# Configure 404 handler
@app.errorhandler(404)
def not_found(error):
    return make_response('Sorry, not found.', 404)


if __name__ == '__main__':
    socketio.run(app, debug=config.app['development_mode'],
                 use_reloader=config.app['development_mode'])
