---
layout: default
title: Access Control
parent: Usages
nav_order: 7
---

## What is Access Control?
This extension provides built-in access control feature. By using access control, You can provide a role to JWT and specify which role can access which endpoints.

# Access Control
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}


## Configuration

First, you should enable `use_acl` option

```python
with JWT.initialize(app) as manager:
    manager.config.use_acl = True
```

Then, spcify which claim you want to store a role to. (default is `permission`)

```python
with JWT.initialize(app) as manager:
    manager.config.acl_claim = "role"
```

[Find more about configuration]({{ site.baseurl }}{% link config_options.md %}){: .btn .btn-outline }

## Create Token

<div class="code-example" markdown="1">
After `JWT` initialized and configured. you can create access token through `JWT.create_access_token`
</div>
```python
access_token = JWT.create_access_token(identity=username)
```
[Find more about creating token]({{ site.baseurl }}{% link api_docs/jwt.md %}#class-sanic_jwtextendedjwt){: .btn .btn-outline }

## Protect Views

`allow` and `deny` can't be used together.
{: .text-yellow-300 .code-example }

All decorators could check role.

<div class="code-example" markdown="1">
Specify `allow` or `deny` to allow or deny roles.
</div>
```python
@app.route("/protected", methods=["GET"])
@jwt_required(allow=["ADMIN", "SUPER-ADMIN"])
async def protected(request: Request, token: Token):
    ...
```
[Find more about protecting views]({{ site.baseurl }}{% link usage/basic.md %}){: .btn .btn-outline }

## Use Token Object

propagated `Token` object contains role info in `Token.role`. if role is not specifed, default value is `None` 

```python
token.role
```

[Find more about token object]({{ site.baseurl }}{% link usage/basic.md %}){: .btn .btn-outline }


---

## Full Example Code
{: .text-delta}


```python
import uuid

from enum import Enum

from sanic import Sanic
from sanic.response import json
from sanic.request import Request

from sanic_jwt_extended import JWT, jwt_required
from sanic_jwt_extended.tokens import Token

app = Sanic(__name__)


class Role(Enum):
    user = "USER"
    admin = "ADMIN"


with JWT.initialize(app) as manager:
    manager.config.secret_key = "secret"
    manager.config.use_acl = True


@app.route("/login", methods=["POST"])
async def login(request: Request):
    username = request.json.get("username", "user")

    access_token = JWT.create_access_token(identity=username, role=Role.user.value)

    return json(
        dict(access_token=access_token), status=200
    )


@app.route("/user", methods=["GET"])
@jwt_required(allow=[Role.user.value, ])
async def user(request: Request, token: Token):
    return json(dict(identity=token.identity, role=token.role, raw_data=token.raw_data, exp=str(token.exp)))


@app.route("/admin", methods=["GET"])
@jwt_required(allow=[Role.admin.value, ])
async def admin(request: Request, token: Token):
    return json(dict(identity=token.identity, role=token.role, raw_data=token.raw_data, exp=str(token.exp)))


if __name__ == "__main__":
    app.run()
```