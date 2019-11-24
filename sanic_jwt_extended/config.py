from dataclasses import dataclass
from datetime import timedelta
from json import JSONDecoder, JSONEncoder
from typing import Any, Optional, Tuple, Type, Union

from sanic_jwt_extended.blacklist import BlacklistABC


@dataclass
class Config:
    read_only: bool = False

    # JWT secrets
    secret_key: Optional[str] = None

    public_key: Optional[str] = None
    private_key: Optional[str] = None

    # Default values for reserved claims
    default_iss: Optional[str] = None
    default_aud: Optional[str] = None

    # General configs
    json_encoder: Any = JSONEncoder
    token_location: Tuple[str] = ("header",)
    access_token_expires: Union[timedelta, bool] = timedelta(minutes=15)
    refresh_token_expires: Union[timedelta, bool] = timedelta(days=30)
    algorithm: str = "HS256"

    public_claim_namespace: str = ""  # should be URL
    private_claim_prefix: str = ""

    # JWT in headers configs
    jwt_header_key: str = "Authorization"
    jwt_header_prefix: str = "Bearer"

    # JWT in query params option
    jwt_query_param_name: str = "jwt"

    # ACL config
    use_acl: bool = False
    acl_claim: str = "permission"

    # Blacklist config
    use_blacklist: bool = False
    blacklist_class: Optional[Type[BlacklistABC]] = None

    def __setattr__(self, key, value):
        if self.read_only:
            raise RuntimeError("Can not set attribute after app initialized.")
        super().__setattr__(key, value)
