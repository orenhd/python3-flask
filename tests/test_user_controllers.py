import json
from unittest import TestCase

from mongoengine import connect

import controllers.user_controllers as user_controllers

import consts.user_consts as user_consts

import services.mocks_service as mocks_service

import config


class UserControllersTestCase(TestCase):

    def setUp(self):
        self.db_conn = connect(host=config.databases['mongodb']['uri'])

    def tearDown(self):
        self.db_conn.close()

    def test_user_login(self):
        req, res, abort = mocks_service.generate_controller_args_mocks()
        req.json = {
            'username': config.admin_user['username'], 'password': config.admin_user['password']}
        user_controllers.user_login_controller(req, res, abort)
        abort.assert_not_called()
        res.assert_called_once()
        res_body, res_status_code = mocks_service.get_parsed_res_call_args(
            res.call_args)
        self.assertEqual(res_body['success'], True)
        self.assertEqual(res_body['msg'], user_consts.AUTH_SUCCESS_MSG)
        self.assertEqual(res_status_code, 200)

    def test_user_login_incorrect_username(self):
        req, res, abort = mocks_service.generate_controller_args_mocks()
        req.json = {'username': 'username',
                    'password': config.admin_user['password']}
        user_controllers.user_login_controller(req, res, abort)
        abort.assert_not_called()
        res.assert_called_once()
        res_body, res_status_code = mocks_service.get_parsed_res_call_args(
            res.call_args)
        self.assertEqual(res_body['success'], False)
        self.assertEqual(res_body['msg'], user_consts.AUTH_FAILED_USER_MSG)
        self.assertEqual(res_status_code, 401)

    def test_user_login_incorrect_password(self):
        req, res, abort = mocks_service.generate_controller_args_mocks()
        req.json = {'username': config.admin_user['username'],
                    'password': 'password'}
        user_controllers.user_login_controller(req, res, abort)
        abort.assert_not_called()
        res.assert_called_once()
        res_body, res_status_code = mocks_service.get_parsed_res_call_args(
            res.call_args)
        self.assertEqual(res_body['success'], False)
        self.assertEqual(res_body['msg'], user_consts.AUTH_FAILED_PASSWORD_MSG)
        self.assertEqual(res_status_code, 401)
    
    def test_user_login_missing_username(self):
        req, res, abort = mocks_service.generate_controller_args_mocks()
        req.json = {'password': config.admin_user['password']}
        try:
            user_controllers.user_login_controller(req, res, abort)
        except:
            pass
        finally:
            res.assert_not_called()
            abort.assert_called_once_with(400)

    def test_user_get(self):
        req, res, abort = mocks_service.generate_controller_args_mocks(config.admin_user['username'])
        user_controllers.user_get_controller(req, res, abort, username=config.admin_user['username'])
        abort.assert_not_called()
        res.assert_called_once()
        res_body, res_status_code = mocks_service.get_parsed_res_call_args(
            res.call_args)
        self.assertEqual(res_body['success'], True)
        self.assertEqual(res_body['data'].get('username'), config.admin_user['username'])
        self.assertEqual(res_status_code, 200)
    
    def test_user_get_incorrect_username(self):
        req, res, abort = mocks_service.generate_controller_args_mocks(config.admin_user['username'])
        try:
            user_controllers.user_get_controller(req, res, abort, username='username')
        except:
            pass
        finally:
            res.assert_not_called()
            abort.assert_called_once_with(400)
