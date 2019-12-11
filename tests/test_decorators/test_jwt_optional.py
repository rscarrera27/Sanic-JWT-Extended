import pytest
from sanic import Sanic
from sanic.response import json
from sanic.websocket import WebSocketProtocol

from sanic_jwt_extended.decorators import jwt_optional
from sanic_jwt_extended.jwt_manager import JWT
from tests.utils import DunnoValue


@pytest.yield_fixture
def app():
    app = Sanic()

    with JWT.initialize(app) as manager:
        manager.config.secret_key = "secret"

    @app.route("/protected", methods=["GET"])
    @jwt_optional
    async def protected(*args, **kwargs):
        return json({}, 204)

    yield app


@pytest.fixture
def test_cli(loop, app, sanic_client):
    return loop.run_until_complete(sanic_client(app, protocol=WebSocketProtocol))


async def test_jwt_optional(test_cli):
    token = JWT.create_access_token("user")

    # With token
    resp = await test_cli.get(
        '/protected',
        headers={JWT.config.jwt_header_key: f"{JWT.config.jwt_header_prefix} {token}"}
    )
    assert resp.status == 204

    # Without token
    resp = await test_cli.get('/protected')
    assert resp.status == 204

    # With unprocessable header
    resp = await test_cli.get(
        '/protected',
        headers={JWT.config.jwt_header_key: f"Token {token}"}
    )
    assert resp.status == 204


async def test_jwt_optional_fail(test_cli):
    # Wrong token
    token = "xxx.yyy.zzz"
    resp = await test_cli.get("/protected", headers={JWT.config.jwt_header_key: f"{JWT.config.jwt_header_prefix} {token}"})
    assert resp.status == 422
    assert await resp.json() == {"msg": DunnoValue(str)}

    # Wrong token type
    refresh_token = JWT.create_refresh_token("user")
    resp = await test_cli.get("/protected", headers={JWT.config.jwt_header_key: f"{JWT.config.jwt_header_prefix} {refresh_token}"})
    assert resp.status == 422
    assert await resp.json() == {"msg": DunnoValue(str)}
