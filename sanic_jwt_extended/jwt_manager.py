import datetime
from json import JSONEncoder

from sanic import Sanic
from sanic.response import json

from jwt import ExpiredSignatureError, InvalidTokenError

from sanic_jwt_extended.exceptions import (
    JWTDecodeError, NoAuthorizationError, InvalidHeaderError, WrongTokenError,
    RevokedTokenError, FreshTokenRequired,
    ConfigurationConflictError, AccessDenied)
from sanic_jwt_extended.tokens import (
    encode_refresh_token, encode_access_token
)


class JWTManager:
    """
    An object used to hold JWT settings for the
    Sanic-GraphQL-Auth extension.
    Instances of :class:`JWTManger` are *not* bound to specific apps, so
    you can create one in the main body of your code and then bind it
    to your app in a factory function.
    """
    def __init__(self, app: Sanic):
        """
        Create the JWTManager instance. You can either pass a sanic application in directly
        here to register this extension with the sanic app, or you can call init_app after creating
        this object (in a factory pattern).
        :param app: A sanic application
        """
        if app is not None:
            self.init_app(app=app)

    def init_app(self, app: Sanic):
        """
        Register this extension with the sanic app.
        :param app: A sanic application
        """
        self._set_error_handlers(app=app)
        self._set_default_configuration_options(app=app)
        app.jwt = self

    @staticmethod
    def _set_default_configuration_options(app):
        """
        Sets the default configuration options used by this extension
        """
        # Where to look for the JWT. Available options are cookies or headers
        app.config.setdefault('JWT_TOKEN_LOCATION', ['headers'])

        # Options for JWTs when the TOKEN_LOCATION is headers
        app.config.setdefault('JWT_HEADER_NAME', 'Authorization')
        app.config.setdefault('JWT_HEADER_TYPE', 'Bearer')

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

        app.config.setdefault("RBAC_ENABLED", False)

        app.json_encoder = JSONEncoder

    @staticmethod
    def _set_error_handlers(app: Sanic):
        """
         Sets the error handler callbacks used by this extension
         """
        @app.exception(NoAuthorizationError)
        async def handle_auth_error(request, e):
            return json({app.config.JWT_ERROR_MESSAGE_KEY: str(e)}, status=401)

        @app.exception(ExpiredSignatureError)
        async def handle_expired_error(request, e):
            return json({app.config.JWT_ERROR_MESSAGE_KEY: "Token has expired"}, status=401)

        @app.exception(InvalidHeaderError)
        async def handle_invalid_header_error(request, e):
            return json({app.config.JWT_ERROR_MESSAGE_KEY: str(e)}, status=422)

        @app.exception(InvalidTokenError)
        async def handle_invalid_token_error(request, e):
            return json({app.config.JWT_ERROR_MESSAGE_KEY: str(e)}, status=422)

        @app.exception(JWTDecodeError)
        async def handle_jwt_decode_error(request, e):
            return json({app.config.JWT_ERROR_MESSAGE_KEY: str(e)}, status=422)

        @app.exception(WrongTokenError)
        async def handle_wrong_token_error(request, e):
            return json({app.config.JWT_ERROR_MESSAGE_KEY: str(e)}, status=422)

        @app.exception(RevokedTokenError)
        async def handle_revoked_token_error(request, e):
            return json({app.config.JWT_ERROR_MESSAGE_KEY: "Token has been revoked"}, status=422)

        @app.exception(FreshTokenRequired)
        async def handle_fresh_token_required(request, e):
            return json({app.config.JWT_ERROR_MESSAGE_KEY: "Fresh token required"}, status=422)

        @app.exception(AccessDenied)
        async def handle_access_denied(request, e):
            return json({app.config.JWT_ERROR_MESSAGE_KEY: str(e)}, status=401)

    @staticmethod
    async def _create_refresh_token(app: Sanic, identity, user_claims, expires_delta=None):
        config = app.config

        if expires_delta is None:
            expires_delta = config.JWT_REFRESH_TOKEN_EXPIRES

        if config.JWT_CLAIMS_IN_REFRESH_TOKEN:
            user_claims = user_claims
        else:
            user_claims = None

        refresh_token = await encode_refresh_token(
            identity=identity,
            secret=config.JWT_SECRET_KEY,
            algorithm=config.JWT_ALGORITHM,
            expires_delta=expires_delta,
            user_claims=user_claims,
            identity_claim_key=config.JWT_IDENTITY_CLAIM,
            user_claims_key=config.JWT_USER_CLAIMS,
            json_encoder=app.json_encoder
        )

        return refresh_token

    @staticmethod
    async def _create_access_token(app: Sanic, identity, user_claims, role, fresh, expires_delta=None):
        config = app.config

        if expires_delta is None:
            expires_delta = config.JWT_ACCESS_TOKEN_EXPIRES

        if role and not config.RBAC_ENABLE:
            raise ConfigurationConflictError("RBAC is not enabled!")

        access_token = await encode_access_token(
            identity=identity,
            secret=config.JWT_SECRET_KEY,
            algorithm=config.JWT_ALGORITHM,
            expires_delta=expires_delta,
            fresh=fresh,
            user_claims=user_claims,
            role=role,
            identity_claim_key=config.JWT_IDENTITY_CLAIM,
            user_claims_key=config.JWT_USER_CLAIMS,
            json_encoder=app.json_encoder
        )
        return access_token
