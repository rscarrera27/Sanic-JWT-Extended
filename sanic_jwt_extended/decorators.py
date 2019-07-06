from datetime import datetime
from calendar import timegm
from functools import wraps
from typing import Dict, List

from sanic import Sanic
from sanic.request import Request

from sanic_jwt_extended.exceptions import WrongTokenError, NoAuthorizationError, InvalidHeaderError, FreshTokenRequired, \
    ConfigurationConflictError, AccessDenied
from sanic_jwt_extended.tokens import decode_jwt, Token


async def get_jwt_data(app: Sanic, token: str) -> Dict:
    """
    Decodes encoded JWT token by using extension setting

    :param app: A Sanic application
    :param token: Encoded JWT string to decode
    :return: Dictionary containing contents of the JWT
    """

    jwt_data: dict = await decode_jwt(
        encoded_token=token,
        secret=app.config.JWT_SECRET_KEY,
        algorithm=app.config.JWT_ALGORITHM,
        identity_claim_key=app.config.JWT_IDENTITY_CLAIM,
        user_claims_key=app.config.JWT_USER_CLAIMS
    )

    return jwt_data


async def get_jwt_data_in_request_header(app: Sanic, request: Request) -> Dict:
    """
    Get JWT token data from request header with configuration. raise NoAuthorizationHeaderError
    when no jwt header. also raise InvalidHeaderError when malformed jwt header detected.

    :param app: A Sanic application
    :param request: Sanic request object that contains app
    :return: Dictionary containing contents of the JWT
    """
    header_name: str = app.config.JWT_HEADER_NAME
    header_type: str = app.config.JWT_HEADER_TYPE

    token_header: str = request.headers.get(header_name)

    if not token_header:
        raise NoAuthorizationError("Missing {} Header".format(header_name))

    parts: List[str] = token_header.split()

    if not header_type:
        if len(parts) != 1:
            msg = "Bad {} header. Expected value '<JWT>'".format(header_name)
            raise InvalidHeaderError(msg)
        token: str = parts[0]
    else:
        if parts[0] != header_type or len(parts) != 2:
            msg = "Bad {} header. Expected value '{} <JWT>'".format(
                header_name,
                header_type
            )
            raise InvalidHeaderError(msg)
        token: str = parts[1]

    data: Dict = await get_jwt_data(app, token)
    return data


async def verify_jwt_data_type(token_data: dict, token_type: str) -> None:
    """
    Check jwt type with given argument. raise WrongTokenError if token type is not expected type,

    :param token_data: Dictionary containing contents of the JWT
    :param token_type: Token type that want to check (ex: access)
    """
    if token_data["type"] != token_type:
        raise WrongTokenError('Only {} tokens are allowed'.format(token_type))


def access_control(role=None, allow=None, deny=None):
    accessible = (role in (allow if allow else deny)) == (True if allow else False)

    if not accessible:
        raise AccessDenied('role {0} is not allowed to access'.format(role))


def _get_request(*args):
    """
    Get request object from args.
    """
    if isinstance(args[0], Request):
        request = args[0]
    else:
        request = args[1]
    return request


def jwt_required(function=None, allow=None, deny=None):
    """
    A decorator to protect a Sanic endpoint.
    If you decorate an endpoint with this, it will ensure that the requester
    has a valid access token before allowing the endpoint to be called.
    and if token check passed this will insert Token object to kwargs,
    This does not check the freshness of the access token.
    See also: :func:`~sanic_jwt_extended.fresh_jwt_required`
    """

    def actual_jwt_required(fn):
        @wraps(fn)
        async def wrapper(*args, **kwargs):
            request = _get_request(*args)
            app = request.app

            token = await get_jwt_data_in_request_header(app, request)
            await verify_jwt_data_type(token, "access")

            try:
                if allow:
                    access_control(token["role"], allow=allow)
                elif deny:
                    access_control(token["role"], deny=deny)
            except KeyError:
                raise ConfigurationConflictError("Please enable RBAC")

            kwargs["token"] = Token(app, token)

            return await fn(*args, **kwargs)
        return wrapper

    if function:
        return actual_jwt_required(function)
    else:
        if allow and deny:
            raise ConfigurationConflictError("Can not use 'deny' and 'allow' option together.")
        return actual_jwt_required


def jwt_optional(fn):
    """
    A decorator to optionally protect a Sanic endpoint
    If an access token in present in the request, this will insert filled Token object to kwargs.
    If no access token is present in the request, this will insert Empty Token object to kwargs
    If there is an invalid access token in the request (expired, tampered with,
    etc), this will still call the appropriate error handler instead of allowing
    the endpoint to be called as if there is no access token in the request.
    """
    @wraps(fn)
    async def wrapper(*args, **kwargs):
        token = {}
        request = _get_request(*args)
        app = request.app

        try:
            token = await get_jwt_data_in_request_header(app, request)
            await verify_jwt_data_type(token, "access")
        except (NoAuthorizationError, InvalidHeaderError):
            pass

        kwargs["token"] = Token(app, token)
        return await fn(*args, **kwargs)
    return wrapper


def fresh_jwt_required(function=None, allow=None, deny=None):
    """
    A decorator to protect a Sanic endpoint.
    If you decorate an endpoint with this, it will ensure that the requester
    has a valid and fresh access token before allowing the endpoint to be
    called.
    See also: :func:`~sanic_jwt_extended.jwt_required`
    """
    def actual_fresh_jwt_required(fn):
        @wraps(fn)
        async def wrapper(*args, **kwargs):
            request = _get_request(*args)
            app = request.app

            token = await get_jwt_data_in_request_header(app, request)
            await verify_jwt_data_type(token, "access")
            fresh = token["fresh"]

            if isinstance(fresh, bool):
                if not fresh:
                    raise FreshTokenRequired('Fresh token required')
            else:
                now = timegm(datetime.utcnow().utctimetuple())
                if fresh < now:
                    raise FreshTokenRequired('Fresh token required')

            try:
                if allow:
                    access_control(token["role"], allow=allow)
                elif deny:
                    access_control(token["role"], deny=deny)
            except KeyError:
                raise ConfigurationConflictError("Please enable RBAC")

            kwargs["token"] = Token(app, token)

            return await fn(*args, **kwargs)
        return wrapper

    if function:
        return actual_fresh_jwt_required(function)
    else:
        if allow and deny:
            raise ConfigurationConflictError("Can not use 'deny' and 'allow' option together.")
        return actual_fresh_jwt_required


def jwt_refresh_token_required(fn):
    """
    A decorator to protect a Sanic endpoint.
    If you decorate an endpoint with this, it will ensure that the requester
    has a valid refresh token before allowing the endpoint to be called.
    """
    @wraps(fn)
    async def wrapper(*args, **kwargs):
        request = _get_request(*args)
        app = request.app

        token = await get_jwt_data_in_request_header(app, request)
        await verify_jwt_data_type(token, "refresh")

        kwargs["token"] = Token(app, token)

        return await fn(*args, **kwargs)
    return wrapper
