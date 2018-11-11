from datetime import datetime
from calendar import timegm
from functools import wraps

from sanic.request import Request

from sanic_jwt_extended.exceptions import WrongTokenError, NoAuthorizationError, InvalidHeaderError, FreshTokenRequired
from sanic_jwt_extended.tokens import decode_jwt, Token


async def get_jwt_data(app, token):

    jwt_data = await decode_jwt(
        encoded_token=token,
        secret=app.config.JWT_SECRET_KEY,
        algorithm=app.config.JWT_ALGORITHM,
        identity_claim_key=app.config.JWT_IDENTITY_CLAIM,
        user_claims_key=app.config.JWT_USER_CLAIMS
        )

    return jwt_data


async def get_jwt_data_in_request_header(app, request: Request, request_type: str):
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

    data = await get_jwt_data(app, token)
    if request_type != data["type"]:
        raise WrongTokenError('Only {} tokens are allowed'.format(request_type))

    return data


def jwt_required(fn):
    @wraps(fn)
    async def wrapper(*args, **kwargs):
        request = args[0]
        app = request.app
        token = await get_jwt_data_in_request_header(app, request, "access")
        kwargs["token"] = Token(app, token)

        return await fn(*args, **kwargs)
    return wrapper


def jwt_optional(fn):
    @wraps(fn)
    async def wrapper(*args, **kwargs):
        token = {}
        request = args[0]
        app = request.app

        try:
            token = get_jwt_data_in_request_header(app, request, "access")
        except (NoAuthorizationError, InvalidHeaderError):
            pass

        kwargs["token"] = Token(app, token)
        return await fn(*args, **kwargs)
    return wrapper


def fresh_jwt_required(fn):
    @wraps(fn)
    async def wrapper(*args, **kwargs):
        request = args[0]
        app = request.app

        token = await get_jwt_data_in_request_header(app, request, "access")
        fresh = token["fresh"]

        if isinstance(fresh, bool):
            if not fresh:
                raise FreshTokenRequired('Fresh token required')
        else:
            now = timegm(datetime.utcnow().utctimetuple())
            if fresh < now:
                raise FreshTokenRequired('Fresh token required')

        kwargs["token"] = Token(app, token)

        return await fn(*args, **kwargs)
    return wrapper


def jwt_refresh_token_required(fn):
    @wraps(fn)
    async def wrapper(*args, **kwargs):
        request = args[0]
        app = request.app

        token = await get_jwt_data_in_request_header(app, request, "refresh")

        if token["type"] != "refresh":
            raise WrongTokenError('Only refresh tokens are allowed')

        kwargs["token"] = Token(app, token)

        return await fn(*args, **kwargs)
    return wrapper
