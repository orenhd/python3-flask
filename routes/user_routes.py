from flask import Blueprint, request, abort, make_response, jsonify
from bcrypt import hashpw, gensalt, checkpw

from models.user_model import User

SALT_WORK_FACTOR = 10

user_bp = Blueprint('profile', __name__, url_prefix='/api/user')


@user_bp.route('/signup', methods=['POST'])
def user_signup():
    if not request.json or not 'username' in request.json:
        abort(400)
    User(
        username=request.json['username'],
        password=hashpw(request.json['password'].encode(
            'UTF-8'), gensalt(SALT_WORK_FACTOR))
    ).save()
    return make_response(jsonify({'success': True}), 200)


@user_bp.route('/login', methods=['POST'])
def user_login():
    if not request.json or not 'username' in request.json:
        abort(400)
    requested_user = User.objects(  # pylint: disable=no-member
        username=request.json['username']).first()
    if not requested_user:
        abort(401)
    if checkpw(request.json['password'].encode(
            'UTF-8'),
            requested_user['password'].encode(
            'UTF-8')):
        return make_response(jsonify({'success': True}), 200)
    else:
        abort(401)


@user_bp.route('/<username>')
def user_get(username):
    requested_user = User.objects(  # pylint: disable=no-member
        username=username).exclude('password').first()
    return make_response(jsonify({'success': True, 'data': requested_user.to_json()}), 200)
