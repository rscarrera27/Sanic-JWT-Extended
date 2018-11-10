import datetime
import uuid

from calendar import timegm

import jwt

from flask_jwt_extended.exceptions import JWTDecodeError


def _encode_jwt(additional_token_data, expires_delta, secret, algorithm,
                json_encoder=None):
    uid = str(uuid.uuid4())
    now = datetime.datetime.utcnow()
    token_data = {
        'iat': now,
        'nbf': now,
        'jti': uid,
    }
    # If expires_delta is False, the JWT should never expire
    # and the 'exp' claim is not set.
    if expires_delta:
        token_data['exp'] = now + expires_delta
    token_data.update(additional_token_data)
    encoded_token = jwt.encode(token_data, secret, algorithm,
                               json_encoder=json_encoder).decode('utf-8')
    return encoded_token


def encode_access_token(identity, secret, algorithm, expires_delta, fresh,
                        user_claims, identity_claim_key, user_claims_key,
                        json_encoder=None):

    if isinstance(fresh, datetime.timedelta):
        now = datetime.datetime.utcnow()
        fresh = timegm((now + fresh).utctimetuple())

    token_data = {
        identity_claim_key: identity,
        'fresh': fresh,
        'type': 'access',
    }

    # Don't add extra data to the token if user_claims is empty.
    if user_claims:
        token_data[user_claims_key] = user_claims

    return _encode_jwt(token_data, expires_delta, secret, algorithm,
                       json_encoder=json_encoder)


def encode_refresh_token(identity, secret, algorithm, expires_delta, user_claims,
                         identity_claim_key, user_claims_key,
                         json_encoder=None):
    """
    Creates a new encoded (utf-8) refresh token.

    :param identity: Some identifier used to identify the owner of this token
    :param secret: Secret key to encode the JWT with
    :param algorithm: Which algorithm to use for the toek
    :param expires_delta: How far in the future this token should expire
                          (set to False to disable expiration)
    :type expires_delta: datetime.timedelta or False
    :param user_claims: Custom claims to include in this token. This data must
                        be json serializable
    :param csrf: Whether to include a csrf double submit claim in this token
                 (boolean)
    :param identity_claim_key: Which key should be used to store the identity
    :param user_claims_key: Which key should be used to store the user claims
    :return: Encoded refresh token
    """
    token_data = {
        identity_claim_key: identity,
        'type': 'refresh',
    }

    # Don't add extra data to the token if user_claims is empty.
    if user_claims:
        token_data[user_claims_key] = user_claims

    return _encode_jwt(token_data, expires_delta, secret, algorithm,
                       json_encoder=json_encoder)

