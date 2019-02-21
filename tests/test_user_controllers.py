import json
from unittest import TestCase

from mongoengine import connect

import controllers.user_controllers as user_controllers

import services.mocks_service as mocks_service

import config

class UserControllersTestCase(TestCase):

    def setUp(self):
        self.db_conn = connect(host=config.databases['mongodb']['uri'])

    def tearDown(self):
        self.db_conn.close()

    def test_user_login(self):
        req, res, abort = mocks_service.generate_controller_args_mocks()
        req.json = {'username': 'admin', 'password': config.admin_user['password']}
        user_controllers.user_login_controller(req, res, abort)
        abort.assert_not_called()
        res.assert_called_once()
        args, kwargs = res.call_args
        self.assertEqual(kwargs, {})
        self.assertEqual(args[1], 200)