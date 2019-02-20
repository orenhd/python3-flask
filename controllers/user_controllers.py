import json
from bcrypt import hashpw, gensalt, checkpw

from models.user_model import UserModel

import config

import consts.user_consts as user_consts

import services.jwt_service as jwt_service

SALT_WORK_FACTOR = 10


def user_signup_controller(req, res, abort):
    if not req.json or not 'username' in req.json:
        abort(400)
    UserModel(
        username=req.json['username'],
        password=hashpw(req.json['password'].encode(
            'UTF-8'), gensalt(SALT_WORK_FACTOR))
    ).save()
    resp = res(json.dumps({'success': True}), 200)
    resp.headers['content-type'] = 'application/json'
    return resp


def user_login_controller(req, res, abort):
    if not req.json or not 'username' in req.json:
        abort(400)
    requested_user = UserModel.objects(  # pylint: disable=no-member
        username=req.json['username']).first()
    if not requested_user:
        resp = res(json.dumps(
            {'success': True, 'msg': user_consts.AUTH_FAILED_USER_MSG}), 401)
    if checkpw(req.json['password'].encode(
            'UTF-8'),
            requested_user['password'].encode(
            'UTF-8')):

        # Create access token based on the logged in username
        # Use jwt directly to maintain controller independent from app instance
        access_token = jwt_service.encode(requested_user['username'])
        resp = res(json.dumps({'success': True, 'data': {'access_token': access_token.decode(
            "utf-8")}, 'msg': user_consts.AUTH_SUCCESS_MSG}), 200)
    else:
        resp = res(json.dumps(
            {'success': True, 'msg': user_consts.AUTH_FAILED_PASSWORD_MSG}), 401)
    resp.headers['content-type'] = 'application/json'
    return resp


def user_get_controller(req, res, abort, **kwargs):
    requested_user = UserModel.objects(  # pylint: disable=no-member
        username=kwargs.get('username')).exclude('password').first()
    # Use jwt directly to maintain controller independent from app instance
    logged_in_user = UserModel.objects(  # pylint: disable=no-member
        username=jwt_service.get_identity(req)).exclude('password').first()
    if requested_user and logged_in_user:
        # Verify friendship
        requested_user_id_str = str(requested_user.id)
        is_friend = True if requested_user_id_str in logged_in_user['friends'] else False
        resp = res(json.dumps({'success': True, 'data': {'id': requested_user_id_str,
                                                         'username': requested_user['username'],
                                                         'friends': requested_user['friends'],
                                                         'is_friend': is_friend}}),
                   200)
        resp.headers['content-type'] = 'application/json'
        return resp
    else:
        abort(400)
