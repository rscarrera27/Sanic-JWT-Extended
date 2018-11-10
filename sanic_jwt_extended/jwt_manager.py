import datetime
from json import JSONEncoder

from sanic import Sanic
from sanic.response import json

from jwt import ExpiredSignatureError, InvalidTokenError

from sanic_jwt_extended.exceptions import (
    JWTDecodeError, NoAuthorizationError, InvalidHeaderError, WrongTokenError,
    RevokedTokenError, FreshTokenRequired
)

class JWTManager:
    def __init__(self, app: Sanic):
        if app is not None:
            self.init_app(app=app)

        app.jwt = self

    def init_app(self, app: Sanic):
        self._set_error_handlers(app=app)
        self._set_default_configuration_options(app)

    @staticmethod
    def _set_default_configuration_options(app):
        # Where to look for the JWT. Available options are cookies or headers
        app.config.setdefault('JWT_TOKEN_LOCATION', ['headers'])

        # Options for JWTs when the TOKEN_LOCATION is headers
        app.config.setdefault('JWT_HEADER_NAME', 'Authorization')
        app.config.setdefault('JWT_HEADER_TYPE', 'JWT')

        # How long an a token will live before they expire.
        app.config.setdefault('JWT_ACCESS_TOKEN_EXPIRES', datetime.timedelta(minutes=15))
        app.config.setdefault('JWT_REFRESH_TOKEN_EXPIRES', datetime.timedelta(days=30))

        # What algorithm to use to sign the token. See here for a list of options:
        # https://github.com/jpadilla/pyjwt/blob/master/jwt/api_jwt.py
        app.config.setdefault('JWT_ALGORITHM', 'HS256')

        # Secret key to sign JWTs with. Only used if a symmetric algorithm is
        # used (such as the HS* algorithms). We will use the app secret key
        # if this is not set.
        app.config.setdefault('JWT_SECRET_KEY', None)

        app.config.setdefault('JWT_IDENTITY_CLAIM', 'identity')
        app.config.setdefault('JWT_USER_CLAIMS', 'user_claims')

        app.config.setdefault('JWT_CLAIMS_IN_REFRESH_TOKEN', False)

        app.config.setdefault('JWT_ERROR_MESSAGE_KEY', 'msg')

        app.json_encoder = JSONEncoder

