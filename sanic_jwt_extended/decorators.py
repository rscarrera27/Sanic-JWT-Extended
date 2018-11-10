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


def get_jwt_data_in_request(app, request: Request):
    header_name = app.config.JWT_HEADER_NAME
    header_type = app.config.JWT_HEADER_TYPE

    token_header = request.headers.get(header_name)

    if not token_header:
        raise NoAuthorizationError("Missing {} Header".format(header_name))

    parts = token_header.split()
    if not header_type:
        if len(parts) != 1:
            msg = "Bad {} header. Expected value '<JWT>'".format(header_name)
            raise InvalidHeaderError(msg)
        token = parts[0]
    else:
        if parts[0] != header_type or len(parts) != 2:
            msg = "Bad {} header. Expected value '{} <JWT>'".format(
                header_name,
                header_type
            )
            raise InvalidHeaderError(msg)
        token = parts[1]

    data = get_jwt_data(app, token)
    return data

