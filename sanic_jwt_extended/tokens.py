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

