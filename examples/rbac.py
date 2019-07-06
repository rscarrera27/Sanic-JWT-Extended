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
app.config['RBAC_ENABLE'] = True
JWTManager(app)


# Provide a method to create access tokens. The create_access_token()
# function is used to actually generate the token, and you can return
# it to the caller however you choose.
@app.route('/login', methods=['POST'])
async def login(request: Request):
    username = request.json.get('username', None)

    # Identity can be any data that is json serializable
    access_token = await create_access_token(identity=username, role="ADMIN", app=request.app)
    return json(dict(
        access_token=access_token
    ), status=200)


# Protect a view with jwt_required, which requires a valid access token
# in the request to access.
@app.route('/protected', methods=['GET'])
@jwt_required(allow=["ADMIN"]) # default to whitelist mode
async def protected(request: Request, token: Token):
    # Access the identity of the current user with get_jwt_identity
    current_user = token.jwt_identity
    return json(dict(logined_as=current_user))


if __name__ == '__main__':
    app.run(port=9000)
