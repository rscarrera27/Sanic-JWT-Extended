from functools import wraps
from datetime import datetime
from calendar import timegm

from werkzeug.exceptions import BadRequest

from sanic.request import Request

from sanic_jwt_extended.exceptions import (
    CSRFError, FreshTokenRequired, InvalidHeaderError, NoAuthorizationError,
    UserLoadError
)

from sanic_jwt_extended.utils import Token


def verify_jwt_in_request(request: Request):
    """
    Ensure that the requeste has a valid access token. This does not check the
    freshness of the access token. Raises an appropiate exception there is
    no token or if the token is invalid.
    """
    if request.method not in request.app.jwt.config.exempt_methods:
        jwt_data = _decode_jwt_from_request(request_type='access', request=request)
        # ctx_stack.top.jwt = jwt_data
        request.jwt = Token(request.app, jwt_data)
        request.app.jwt.verify_token_claims(jwt_data)
        _load_user(jwt_data[request.app.jwt.config.identity_claim_key], jwt=request.app.jwt, token=request.jwt)


def verify_jwt_in_request_optional(request: Request):
    """
    Optionally check if this request has a valid access token.  If an access
    token in present in the request, :func:`~sanic_jwt_extended.get_jwt_identity`
    will return  the identity of the access token. If no access token is
    present in the request, this simply returns, and
    :func:`~sanic_jwt_extended.get_jwt_identity` will return `None` instead.

    If there is an invalid access token in the request (expired, tampered with,
    etc), this will still raise the appropiate exception.
    """
    try:
        if request.method not in request.app.jwt.config.exempt_methods:
            jwt_data = _decode_jwt_from_request(request_type='access', request=request)
            request.jwt = Token(request.app, jwt_data)
            request.app.jwt.verify_token_claims(jwt_data)
            _load_user(jwt_data[request.app.jwt.config.identity_claim_key], request.app.jwt, request.jwt)
    except (NoAuthorizationError, InvalidHeaderError):
        pass


def verify_fresh_jwt_in_request(request: Request):
    """
    Ensure that the requeste has a valid and fresh access token. Raises an
    appropiate exception if there is no token, the token is invalid, or the
    token is not marked as fresh.
    """
    if request.method not in request.app.jwt.config.exempt_methods:
        jwt_data = _decode_jwt_from_request(request_type='access', request=request)
        request.jwt = Token(request.app, jwt_data)
        fresh = jwt_data['fresh']
        if isinstance(fresh, bool):
            if not fresh:
                raise FreshTokenRequired('Fresh token required')
        else:
            now = timegm(datetime.utcnow().utctimetuple())
            if fresh < now:
                raise FreshTokenRequired('Fresh token required')
        request.app.verify_token_claims(jwt_data)
        _load_user(jwt_data[request.app.jwt.config.identity_claim_key], jwt=request.app.jwt, token=request.jwt)


def verify_jwt_refresh_token_in_request(request: Request):
    """
    Ensure that the requeste has a valid refresh token. Raises an appropiate
    exception if there is no token or the token is invalid.
    """
    if request.method not in request.app.jwt.config.exempt_methods:
        jwt_data = _decode_jwt_from_request(request_type='refresh', request=request)
        request.jwt = Token(request.app, jwt_data)
        _load_user(jwt_data[request.app.jwt.config.identity_claim_key], jwt=request.jwt, token=request.token)


def jwt_required(fn):
    """
    A decorator to protect a Flask endpoint.

    If you decorate an endpoint with this, it will ensure that the requester
    has a valid access token before allowing the endpoint to be called. This
    does not check the freshness of the access token.

    See also: :func:`~sanic_jwt_extended.fresh_jwt_required`
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request(kwargs.get("request"))
        return fn(*args, **kwargs)
    return wrapper


def jwt_optional(fn):
    """
    A decorator to optionally protect a Flask endpoint

    If an access token in present in the request, this will call the endpoint
    with :func:`~sanic_jwt_extended.get_jwt_identity` having the identity
    of the access token. If no access token is present in the request,
    this endpoint will still be called, but
    :func:`~sanic_jwt_extended.get_jwt_identity` will return `None` instead.

    If there is an invalid access token in the request (expired, tampered with,
    etc), this will still call the appropriate error handler instead of allowing
    the endpoint to be called as if there is no access token in the request.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request_optional(kwargs.get("request"))
        return fn(*args, **kwargs)
    return wrapper


def fresh_jwt_required(fn):
    """
    A decorator to protect a Flask endpoint.

    If you decorate an endpoint with this, it will ensure that the requester
    has a valid and fresh access token before allowing the endpoint to be
    called.

    See also: :func:`~sanic_jwt_extended.jwt_required`
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_fresh_jwt_in_request(kwargs.get("request"))
        return fn(*args, **kwargs)
    return wrapper


def jwt_refresh_token_required(fn):
    """
    A decorator to protect a Flask endpoint.

    If you decorate an endpoint with this, it will ensure that the requester
    has a valid refresh token before allowing the endpoint to be called.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_refresh_token_in_request(kwargs.get("request"))
        return fn(*args, **kwargs)
    return wrapper


def _load_user(identity, jwt, token):
    if jwt.has_user_loader():
        user = jwt.user_loader(identity)
        if user is None:
            raise UserLoadError("user_loader returned None for {}".format(identity))
        else:
            token.jwt_user = user


def _decode_jwt_from_headers(request):
    header_name = request.app.jwt.config.header_name
    header_type = request.app.jwt.config.header_type

    # Verify we have the auth header
    jwt_header = request.headers.get(header_name, None)
    if not jwt_header:
        raise NoAuthorizationError("Missing {} Header".format(header_name))

    # Make sure the header is in a valid format that we are expecting, ie
    # <HeaderName>: <HeaderType(optional)> <JWT>
    parts = jwt_header.split()
    if not header_type:
        if len(parts) != 1:
            msg = "Bad {} header. Expected value '<JWT>'".format(header_name)
            raise InvalidHeaderError(msg)
        encoded_token = parts[0]
    else:
        if parts[0] != header_type or len(parts) != 2:
            msg = "Bad {} header. Expected value '{} <JWT>'".format(
                header_name,
                header_type
            )
            raise InvalidHeaderError(msg)
        encoded_token = parts[1]

    return request.app.jwt.decode_token(encoded_token)


def _decode_jwt_from_cookies(request_type, request):
    app = request.app

    if request_type == 'access':
        cookie_key = app.jwt.config.access_cookie_name
        csrf_header_key = app.jwt.config.access_csrf_header_name
    else:
        cookie_key = app.jwt.config.refresh_cookie_name
        csrf_header_key = app.jwt.config.refresh_csrf_header_name

    encoded_token = request.cookies.get(cookie_key)
    if not encoded_token:
        raise NoAuthorizationError('Missing cookie "{}"'.format(cookie_key))

    if app.jwt.config.csrf_protect and request.method in app.jwt.config.csrf_request_methods:
        csrf_value = request.headers.get(csrf_header_key, None)
        if not csrf_value:
            raise CSRFError("Missing CSRF token in headers")
    else:
        csrf_value = None

    return app.jwt.decode_token(encoded_token, csrf_value=csrf_value)


def _decode_jwt_from_query_string(request):
    app = request.app
    query_param = app.jwt.config.query_string_name
    encoded_token = request.args.get(query_param)
    if not encoded_token:
        raise NoAuthorizationError('Missing "{}" query paramater'.format(query_param))

    return app.jwt.decode_token(encoded_token)


def _decode_jwt_from_json(request_type, request):
    if request.content_type != 'application/json':
        raise NoAuthorizationError('Invalid content-type. Must be application/json.')

    if request_type == 'access':
        token_key = request.app.jwt.config.json_key
    else:
        token_key = request.app.jwt.config.refresh_json_key

    try:
        encoded_token = request.json.get(token_key, None)
        if not encoded_token:
            raise BadRequest()
    except BadRequest:
        raise NoAuthorizationError('Missing "{}" key in json data.'.format(token_key))

    return request.app.jwt.decode_token(encoded_token)


def _decode_jwt_from_request(request_type, request):
    config = request.app.jwt.config
    app = request.app
    # All the places we can get a JWT from in this request
    decode_functions = []
    if config.jwt_in_cookies:
        decode_functions.append(lambda: _decode_jwt_from_cookies(request_type, request=request))
    if config.jwt_in_query_string:
        decode_functions.append(_decode_jwt_from_query_string)
    if config.jwt_in_headers:
        decode_functions.append(_decode_jwt_from_headers)
    if config.jwt_in_json:
        decode_functions.append(lambda: _decode_jwt_from_json(request_type, request=request) )

    # Try to find the token from one of these locations. It only needs to exist
    # in one place to be valid (not every location).
    errors = []
    decoded_token = None
    for decode_function in decode_functions:
        try:
            decoded_token = decode_function()
            break
        except NoAuthorizationError as e:
            errors.append(str(e))

    # Do some work to make a helpful and human readable error message if no
    # token was found in any of the expected locations.
    if not decoded_token:
        token_locations = config.token_location
        multiple_jwt_locations = len(token_locations) != 1

        if multiple_jwt_locations:
            err_msg = "Missing JWT in {start_locs} or {end_locs} ({details})".format(
                start_locs=", ".join(token_locations[:-1]),
                end_locs=token_locations[-1],
                details="; ".join(errors)
            )
            raise NoAuthorizationError(err_msg)
        else:
            raise NoAuthorizationError(errors[0])

    app.jwt.verify_token_type(decoded_token, expected_type=request_type)
    app.jwt.verify_token_not_blacklisted(decoded_token, request_type)
    return decoded_token
