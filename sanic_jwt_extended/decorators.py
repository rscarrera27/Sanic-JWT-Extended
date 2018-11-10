from functools import wraps

from sanic.request import Request

from sanic_jwt_extended.exceptions import WrongTokenError, NoAuthorizationError, InvalidHeaderError
from sanic_jwt_extended.tokens import decode_jwt, Token


def get_jwt_data(app, token):

    jwt_data = decode_jwt(
        encoded_token=token,
        secret=app.config.JWT_SECRET_KEY,
        algorithm=app.config.JWT_ALGORITHM,
        identity_claim_key=app.config.JWT_IDENTITY_CLAIM,
        user_claims_key=app.config.JWT_USER_CLAIMS
        )

    return jwt_data

