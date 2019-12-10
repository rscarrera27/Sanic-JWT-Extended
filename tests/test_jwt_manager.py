import pytest
from sanic import Sanic

from sanic_jwt_extended.exceptions import ConfigurationConflictError
from sanic_jwt_extended.jwt_manager import JWT
from sanic_jwt_extended.tokens import Token


class TestJWT:
    @pytest.fixture
    def app(self):
        app = Sanic()
        return app

    # fmt: off
    @pytest.mark.parametrize("config", [
        {"secret_key": "super-secret"},
        {"algorithm": "RS256", "public_key": "pub1ic", "private_key": "pr1vate"},
        {"secret_key": "super-secret", "use_blacklist": True}
    ])
    @pytest.mark.parametrize("handler", [
        {"expired_signature": lambda r, e: ...}
    ])
    # fmt: on
    def test_initialize(self, app, recwarn, config, handler):
        with JWT.initialize(app) as initialize:
            for attr, value in config.items():
                setattr(initialize.config, attr, value)
            for attr, value in handler.items():
                setattr(initialize.handler, attr, value)

        with pytest.raises(RuntimeError):
            JWT.config.algorithm = "HS512"

        if config.get("use_blacklist"):
            assert len(recwarn) == 2

        for attr, value in config.items():
            assert getattr(initialize.config, attr) == value

        for attr, value in handler.items():
            assert getattr(initialize.handler, attr) == value

    # fmt: off
    @pytest.mark.parametrize("config", [
        {},
        {"algorithm": "RS256", "public_key": "pub1ic", "secret_key": "s3cr3t"},
        {"algorithm": "RS256", "private_key": "s3cr3t"},
    ])  # fmt: on
    def test_initialize_fail(self, app, config):
        with pytest.raises(ConfigurationConflictError):
            with JWT.initialize(app) as initialize:
                for attr, value in config.items():
                    setattr(initialize.config, attr, value)

    # fmt: off
    @pytest.mark.parametrize("args", [
        {"identity": "user"},
        {"identity": "user", "fresh": True},
        {"identity": "user", "role": "ADMIN"},
        {"identity": "user", "expires_delta": False},
        {"identity": "user", "public_claims": {"user_id": 0, "misc": {"foo": "bar"}}},
        {"identity": "user", "private_claims": {"secret_info": "secret"}}
    ])  # fmt: on
    def test_create_access_token(self, app, args):
        with JWT.initialize(app) as manager:
            manager.config.secret_key = "secret"
            manager.config.public_claim_namespace = "https://seonghyeon.dev/"
            manager.config.use_acl = True

        raw_token = JWT.create_access_token(**args)
        token = Token(raw_token)

        for k, v in args.items():
            if k == "expires_delta":
                assert getattr(token, "exp") == (v if v is not False else None)
            else:
                assert getattr(token, k) == v

    # fmt: off
    @pytest.mark.parametrize("args", [
        {"identity": "user", "role": "ADMIN"},
        {"identity": "user", "public_claims": {"user_id": 0, "misc": {"foo": "bar"}}},
    ])  # fmt: on
    def test_create_access_token_fail(self, app, args):
        with JWT.initialize(app) as manager:
            manager.config.secret_key = "secret"

        with pytest.raises(ConfigurationConflictError):
            JWT.create_access_token(**args)


