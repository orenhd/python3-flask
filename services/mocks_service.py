# mocks_service
# - Exposes configured functions for generatings common-used Mock objects

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
