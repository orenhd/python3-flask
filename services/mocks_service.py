# mocks_service
# - Exposes configured functions for generating and destructure common-used Mock objects

import json
from unittest.mock import Mock, MagicMock

import services.jwt_service as jwt_service

import config


def generate_controller_args_mocks(access_token_identity = None):
    req = Mock()
    req.json = {}
    res = MagicMock()
    abort = Mock()

    if access_token_identity:  # If an identity string was passed - generate an access token on header
        req.headers = {
            jwt_service.JWT_HEADER_NAME: jwt_service.encode(
                access_token_identity)
        }

    return (req, res, abort)

def get_parsed_res_call_args(res_call_args):
    args, kwargs = res_call_args # pylint: disable=unused-variable
    res_body = json.loads(args[0])
    res_status_code = args[1]
    return (res_body, res_status_code)
