from sanic import Sanic
from sanic.response import json
from sanic.request import Request
from sanic_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    create_refresh_token)
import uuid
from sanic_jwt_extended.tokens import Token

app = Sanic(__name__)

# Setup the Sanic-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
JWTManager(app)

user_claim = {"VERI TAS": "LUX MEA"}


# Provide a method to create access tokens. The create_access_token()
# function is used to actually generate the token, and you can return
# it to the caller however you choose.
@app.route('/login', methods=['POST'])
async def login(request: Request):
    if not request.json:
        return json({"msg": "Missing JSON in request"}, status=400)

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return json({"msg": "Missing username parameter"}, status=400)
    if not password:
        return json({"msg": "Missing password parameter"}, status=400)

    if username != 'test' or password != 'test':
        return json({"msg": "Bad username or password"}, status=403)

    # Identity can be any data that is json serializable
    access_token = await create_access_token(identity=username, app=request.app, user_claims=user_claim)
    return json(dict(access_token=access_token
                     ), status=200)


# Protect a view with jwt_required, which requires a valid access token
# in the request to access.
@app.route('/protected', methods=['GET'])
@jwt_required
async def protected(request: Request, token: Token):
    # Access the identity of the current user with get_jwt_identity
    user_claims = token.jwt_user_claims
    return json(dict(data=user_claims))

if __name__ == '__main__':
    app.run()
