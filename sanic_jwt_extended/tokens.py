import datetime
import uuid

from calendar import timegm
from typing import Union, Dict, Callable

import jwt

from sanic_jwt_extended.exceptions import JWTDecodeError
from sanic import Sanic


def _encode_jwt(additional_token_data: dict, expires_delta: datetime.timedelta, secret: str, algorithm: str,
                json_encoder: Callable[..., str]) -> str:
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


async def encode_access_token(identity: str, secret: str, algorithm: str, expires_delta: datetime.timedelta,
                              fresh: Union[datetime.timedelta, bool],
                              user_claims: dict, role: str, identity_claim_key: str, user_claims_key: str,
                              json_encoder: Callable[..., str] = None) -> str:
    """
    Creates a new encoded (utf-8) access token.
    :param identity: Identifier for who this token is for (ex, username). This
                     data must be json serializable
    :param secret: Secret key to encode the JWT with
    :param algorithm: Which algorithm to encode this JWT with
    :param expires_delta: How far in the future this token should expire
                          (set to False to disable expiration)
    :type expires_delta: datetime.timedelta or False
    :param fresh: If this should be a 'fresh' token or not. If a
                  datetime.timedelta is given this will indicate how long this
                  token will remain fresh.
    :param user_claims: Custom claims to include in this token. This data must
                        be json serializable
    :param role: A role field for RBAC
    :param identity_claim_key: Which key should be used to store the identity
    :param user_claims_key: Which key should be used to store the user claims
    :param json_encoder: json encoder
    :return: Encoded access token
    """
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

    if role:
        token_data["role"] = role

    return _encode_jwt(token_data, expires_delta, secret, algorithm,
                       json_encoder=json_encoder)


async def encode_refresh_token(identity, secret, algorithm, expires_delta, user_claims,
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
    :param identity_claim_key: Which key should be used to store the identity
    :param user_claims_key: Which key should be used to store the user claims
    :param json_encoder: json encoder
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


async def decode_jwt(encoded_token: str, secret: str, algorithm: str, identity_claim_key: str,
                     user_claims_key: str) -> Dict:
    """
    Decodes an encoded JWT

    :param encoded_token: The encoded JWT string to decode
    :param secret: Secret key used to encode the JWT
    :param algorithm: Algorithm used to encode the JWT
    :param identity_claim_key: expected key that contains the identity
    :param user_claims_key: expected key that contains the user claims
    :return: Dictionary containing contents of the JWT
    """
    # This call verifies the ext, iat, and nbf claims
    data: dict = jwt.decode(encoded_token, secret, algorithms=[algorithm])

    # Make sure that any custom claims we expect in the token are present
    if 'jti' not in data:
        raise JWTDecodeError("Missing claim: jti")
    if identity_claim_key not in data:
        raise JWTDecodeError("Missing claim: {}".format(identity_claim_key))
    if 'type' not in data or data['type'] not in ('refresh', 'access'):
        raise JWTDecodeError("Missing or invalid claim: type")
    if data['type'] == 'access':
        if 'fresh' not in data:
            raise JWTDecodeError("Missing claim: fresh")
    if user_claims_key not in data:
        data[user_claims_key] = {}

    return data


class Token:
    """
    Token object that contains decoded token data and passed with kwargs to endpoint function
    """
    data: dict
    app: Sanic

    def __init__(self, app: Sanic, token: dict):
        self.app = app
        self.data = token

    @property
    def raw_jwt(self) -> dict:
        """
        :return: full jwt data in dictionary form
        """
        return self.data

    @property
    def jwt_identity(self) -> Union[str, None]:
        """
        :return: jwt identity claim data (or this can be None if data does not exist)
        """
        return self.data.get(self.app.config.JWT_IDENTITY_CLAIM, None)

    @property
    def jwt_user_claims(self) -> Dict:
        """
        :return: user claim data
        """
        return self.data.get(self.app.config.JWT_USER_CLAIMS, {})

    @property
    def jti(self) -> str:
        """
        :return: jti data
        """
        return self.data.get("jti", None)
