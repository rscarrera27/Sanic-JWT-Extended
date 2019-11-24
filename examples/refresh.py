import uuid

from sanic import Sanic
from sanic.response import json
from sanic.request import Request

from sanic_jwt_extended import JWT, refresh_jwt_required
from sanic_jwt_extended.tokens import Token

app = Sanic(__name__)


with JWT.initialize(app) as manager:
    manager.config.secret_key = "secret"


@app.route("/login", methods=["POST"])
async def login(request: Request):
    username = request.json.get("username", "user")

    access_token = JWT.create_access_token(identity=username)
    refresh_token = JWT.create_refresh_token(identity=username)

    return json(
        dict(access_token=access_token, refresh_token=refresh_token), status=200
    )


@app.route("/refresh", methods=["POST"])
@refresh_jwt_required
async def protected(request: Request, token: Token):
    return json({"refresh_token": JWT.create_access_token(identity=token.identity)})


if __name__ == "__main__":
    app.run()