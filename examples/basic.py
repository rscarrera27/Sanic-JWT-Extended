from sanic import Sanic
from sanic.response import json
from sanic.request import Request

from sanic_jwt_extended import JWT, jwt_required
import uuid

from sanic_jwt_extended.tokens import Token

app = Sanic(__name__)


with JWT.initialize(app) as manager:
    manager.config.secret_key = "secret"
    manager.config.public_claim_namespace = "http://seonghyeon.dev/"


@app.route("/login", methods=["POST"])
async def login(request: Request):
    username = request.json.get("username", "user")

    access_token = JWT.create_access_token(identity=username, public_claims={"class": "novel"})
    refresh_token = JWT.create_refresh_token(identity=uuid.uuid4().hex)

    return json(
        dict(access_token=access_token, refresh_token=refresh_token), status=200
    )


# Protect a view with jwt_required, which requires a valid access token
# in the request to access.
@app.route("/protected", methods=["GET"])
@jwt_required
async def protected(request: Request, token: Token):
    # Access the identity of the current user with get_jwt_identity
    return json(dict(identity=token.sub, type=token.type, raw_jwt=token.raw_data, exp=str(token.exp)))


if __name__ == "__main__":
    app.run()