import json
from unittest import TestCase
from unittest.mock import Mock, MagicMock

from mongoengine import connect

import controllers.user_controllers as user_controllers

import config


class UserControllersTestCase(TestCase):

    def setUp(self):
        self.db_conn = connect(host=config.databases['mongodb']['uri'])

    def tearDown(self):
        self.db_conn.close()

    def test_user_login(self):
        req = Mock()
        req.json = {'username': 'admin', 'password': config.admin_user['password']}
        abort = Mock()
        res = MagicMock()
        user_controllers.user_login_controller(req, res, abort)
        abort.assert_not_called()
        res.assert_called_once()
        args, kwargs = res.call_args
        self.assertEqual(kwargs, {})
        self.assertEqual(args[1], 200)