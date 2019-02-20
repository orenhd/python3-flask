from flask import Blueprint, request as req, abort, make_response as res
from flask_jwt_extended import jwt_required

import controllers.user_controllers as user_controllers

user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/signup', methods=['POST'])
def user_signup():
    return user_controllers.user_signup_controller(req, res, abort)


@user_bp.route('/login', methods=['POST'])
def user_login():
    return user_controllers.user_login_controller(req, res, abort)


@user_bp.route('/<username>')
@jwt_required
def user_get(username):
    return user_controllers.user_get_controller(req, res, abort, username=username)
