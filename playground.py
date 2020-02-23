import uuid

from sanic import Sanic
from sanic.response import json
from sanic.request import Request

from sanic_jwt_extended import JWT, jwt_required
from sanic_jwt_extended.tokens import Token

app = Sanic(__name__)

with JWT.initialize(app) as manager:
    manager.config.secret_key = "secret"
    # manager.config.private_claim_prefix = "sanic_jwt_extended"
    manager.config.public_claim_namespace = "https://seong_hyeon.dev/"


@app.route("/login", methods=["POST"])
async def login(request: Request):
    username = request.json.get("username", "user")

    access_token = JWT.create_access_token(identity=username, private_claims={"foo": "bar"}, public_claims={"perm": 100})

    return json(
        dict(access_token=access_token), status=200
    )


@app.route("/protected", methods=["GET"])
@jwt_required
async def protected(request: Request, token: Token):
    return json(dict(public_claims=token.public_claims,
        private_claims=token.private_claims,
                     raw_data=token.raw_data))


if __name__ == "__main__":
    app.run()
