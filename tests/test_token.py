import pytest
from sanic import Sanic

from sanic_jwt_extended.exceptions import ConfigurationConflictError
from sanic_jwt_extended.jwt_manager import JWT
from sanic_jwt_extended.tokens import Token


class TestToken:
    @pytest.fixture
    def jwt_manager(self):
        app = Sanic()
        with JWT.initialize(app) as initialize:
            initialize.config.secret_key = "secret"
            initialize.config.use_blacklist = True

        return

    @pytest.mark.asyncio
    async def test_revoke(self, jwt_manager):
        raw_token = JWT.create_access_token("user")
        token = Token(raw_token)

        await token.revoke()
        assert (await JWT.blacklist.is_blacklisted(token)) is True

    @pytest.mark.asyncio
    async def test_revoke_fail(self, jwt_manager):
        raw_token = JWT.create_access_token("user")
        token = Token(raw_token)
        object.__setattr__(JWT.config, "use_blacklist", False)

        with pytest.raises(ConfigurationConflictError):
            await token.revoke()
