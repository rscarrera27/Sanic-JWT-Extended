"""
These are the default methods implementations that are used in this extension.
All of these can be updated on an app by app basis using the JWTManager
loader decorators. For further information, check out the following links:

http://flask-jwt-extended.readthedocs.io/en/latest/changing_default_behavior.html
http://flask-jwt-extended.readthedocs.io/en/latest/tokens_from_complex_object.html
"""
from sanic import response, Sanic
from sanic.response import HTTPResponse

from sanic_jwt_extended.config import Config

from typing import Any, Callable, Awaitable, Coroutine


def register_default_callbacks(app: Sanic):
    config = app.jwt.config

    async def default_user_claims_callback(identity: Any) -> dict:
        """
        By default, we add no additional claims to the access tokens.

        :param identity: data passed in as the ```identity``` argument to the
                         ```create_access_token``` and ```create_refresh_token```
                         functions
        """
        return dict()

    async def default_user_identity_callback(identity: Any) -> Any:
        """
        By default, we use the passed in object directly as the jwt identity.
        See this for additional info:

        :param identity: data passed in as the ```identity``` argument to the
                         ```create_access_token``` and ```create_refresh_token```
                         functions
        """
        return identity

    async def default_expired_token_callback() -> response.HTTPResponse:
        """
        By default, if an expired token attempts to access a protected endpoint,
        we return a generic error message with a 401 status
        """
        return response.json({config.error_msg_key: 'Token has expired'}, status=401)

    async def default_invalid_token_callback(error_string: str) -> response.HTTPResponse:
        """
        By default, if an invalid token attempts to access a protected endpoint, we
        return the error string for why it is not valid with a 422 status code
        :param error_string: String indicating why the token is invalid
        """
        return response.json({config.error_msg_key: error_string}, status=422)

    async def default_unauthorized_callback(error_string: str) -> response.HTTPResponse:
        """
        By default, if a protected endpoint is accessed without a JWT, we return
        the error string indicating why this is unauthorized, with a 401 status code
        :param error_string: String indicating why this request is unauthorized
        """
        return response.json({config.error_msg_key: error_string}, status=401)

    async def default_needs_fresh_token_callback() -> response.HTTPResponse:
        """
        By default, if a non-fresh jwt is used to access a ```fresh_jwt_required```
        endpoint, we return a general error message with a 401 status code
        """
        return response.json({config.error_msg_key: 'Fresh token required'}, status=401)

    async def default_revoked_token_callback() -> response.HTTPResponse:
        """
        By default, if a revoked token is used to access a protected endpoint, we
        return a general error message with a 401 status code
        """
        return response.json({config.error_msg_key: 'Token has been revoked'}, status=401)

    async def default_user_loader_error_callback(identity: Any) -> response.HTTPResponse:
        """
        By default, if a user_loader callback is defined and the callback
        function returns None, we return a general error message with a 401
        status code
        """
        result = {config.error_msg_key: "Error loading the user {}".format(identity)}
        return response.json(result, status=401)

    async def default_claims_verification_callback(user_claims: Any) -> bool:
        """
        By default, we do not do any verification of the user claims.
        """
        return True

    async def default_verify_claims_failed_callback() -> response.HTTPResponse:
        """
        By default, if the user claims verification failed, we return a generic
        error message with a 400 status code
        """
        return response.json({config.error_msg_key: 'User claims verification failed'}, status=400)

    async def default_decode_key_callback(claims: str) -> str:
        """
        By default, the decode key specified via the JWT_SECRET_KEY or
        JWT_PUBLIC_KEY settings will be used to decode all tokens
        """
        return config.decode_key

    async def default_encode_key_callback(identity: str) -> str:
        """
        By default, the encode key specified via the JWT_SECRET_KEY or
        JWT_PRIVATE_KEY settings will be used to encode all tokens
        """
        return config.encode_key

    app.jwt._user_claims_callback = default_user_claims_callback
    app.jwt._user_identity_callback = default_user_identity_callback
    app.jwt._expired_token_callback = default_expired_token_callback
    app.jwt._invalid_token_callback = default_invalid_token_callback
    app.jwt._unauthorized_callback = default_unauthorized_callback
    app.jwt._needs_fresh_token_callback = default_needs_fresh_token_callback
    app.jwt._revoked_token_callback = default_revoked_token_callback
    app.jwt._user_loader_callback = None
    app.jwt._user_loader_error_callback = default_user_loader_error_callback
    app.jwt._token_in_blacklist_callback = None
    app.jwt._claims_verification_callback = default_claims_verification_callback
    app.jwt._verify_claims_failed_callback = default_verify_claims_failed_callback
    app.jwt._decode_key_callback = default_decode_key_callback
    app.jwt._encode_key_callback = default_encode_key_callback
