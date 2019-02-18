from flask import Blueprint, request, abort, make_response, jsonify
from bcrypt import hashpw, gensalt, checkpw
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

from models.user_model import UserModel

import consts.user_consts as user_consts

SALT_WORK_FACTOR = 10

user_bp = Blueprint('profile', __name__, url_prefix='/api/user')


@user_bp.route('/signup', methods=['POST'])
def user_signup():
    if not request.json or not 'username' in request.json:
        abort(400)
    UserModel(
        username=request.json['username'],
        password=hashpw(request.json['password'].encode(
            'UTF-8'), gensalt(SALT_WORK_FACTOR))
    ).save()
    return make_response(jsonify({'success': True}), 200)


@user_bp.route('/login', methods=['POST'])
def user_login():
    if not request.json or not 'username' in request.json:
        abort(400)
    requested_user = UserModel.objects(  # pylint: disable=no-member
        username=request.json['username']).first()
    if not requested_user:
        return make_response(jsonify({'success': True, 'msg': user_consts.AUTH_FAILED_USER_MSG}), 401)
    if checkpw(request.json['password'].encode(
            'UTF-8'),
            requested_user['password'].encode(
            'UTF-8')):

        # Create access token based on the logged in username
        access_token = create_access_token(identity=requested_user['username'])
        return make_response(jsonify({'success': True, 'data': {'access_token': access_token}, 'msg': user_consts.AUTH_SUCCESS_MSG}), 200)
    else:
        return make_response(jsonify({'success': True, 'msg': user_consts.AUTH_FAILED_PASSWORD_MSG}), 401)


@user_bp.route('/<username>')
@jwt_required
def user_get(username):
    requested_user = UserModel.objects(  # pylint: disable=no-member
        username=username).exclude('password').first()
    return make_response(jsonify({'success': True, 'data': requested_user.to_json()}), 200)
