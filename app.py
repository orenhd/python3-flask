from flask import Flask, make_response, jsonify
from werkzeug.exceptions import HTTPException
from mongoengine import connect

import config

from routes.user_routes import user_bp

# Init mongodb connection
connect(host=config.databases['mongodb']['uri'])

# Configure app
app = Flask(__name__)

app.register_blueprint(user_bp, url_prefix='/api/user')

# Configure general error handler
@app.errorhandler(Exception)
def handle_error(e):
    err_code = 500
    if isinstance(e, HTTPException):
        err_code = e.code
    return make_response(jsonify({'success': False, 'message': str(e)}), err_code)

# Configure 404 handler
@app.errorhandler(404)
def not_found(error):
    return make_response('Sorry, not found.', 404)


if __name__ == '__main__':
    app.run()