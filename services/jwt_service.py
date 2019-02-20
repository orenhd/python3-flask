# jwt_service
# - Exposes configured functions for working with PyJWT directly
# - Stores jwt related const values

from jwt import encode as jwt_encode, decode as jwt_decode

import config

# JWT const values
JWT_HEADER_NAME = 'x-access-token'
JWT_HEADER_TYPE = ''


def encode(identity):
    return jwt_encode({'identity': identity}, config.app['at_string'], algorithm='HS256')


def get_identity(request):
    jwt_decoded = jwt_decode(request.headers.get(
        'x-access-token'), config.app['at_string'], algorithms=['HS256'])
    return jwt_decoded.get('identity')
