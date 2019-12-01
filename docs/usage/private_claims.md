---
layout: default
title: Storing Private Claims
parent: Usages
nav_order: 4
---
# Basic Usage
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

## What Is Private Claims?

claims to share information specific to your application., which might contain application specific information like `user_id` or `permission_level`.

[Find more about private claims at Auth0](https://auth0.com/docs/tokens/jwt-claims#private-claims){: .btn .btn-purple }

## Configuration

We highly **recommend** to configure `JWT.config.private_claim_prefix` to avoid collision, such as through [namespacing](https://auth0.com/docs/tokens/concepts/claims-namespacing)

```python
with JWT.initialize(app) as manager:
    manager.config.private_claim_prefix = "sanic-jwt-extended"
```

[Find more about configuration]({{ site.baseurl }}{% link config_options.md %}){: .btn .btn-outline }


## Create Token

Both access and refresh token can contain role. you must provide role in string

```python
refresh_token = JWT.create_access_token(identity=username, role="ADMIN")
```

You can also create token without role.

[Find more about creating token]({{ site.baseurl }}{% link api_docs/jwt.md %}#class-sanic_jwtextendedjwt){: .btn .btn-outline }

## Protect Views

There's nothing to configurate to get private claims

## Use Token Object

propagated `Token` object contains private claims in `Token.private_claims`. prefix is not exist on this time. 

```python
token.private_claims
```

[Find more about token object]({{ site.baseurl }}{% link usage/basic.md %}){: .btn .btn-outline }


---

## Full Example Code
{: .text-delta}


```python
import uuid

from sanic import Sanic
from sanic.response import json
from sanic.request import Request

from sanic_jwt_extended import JWT, jwt_required
from sanic_jwt_extended.tokens import Token

app = Sanic(__name__)

with JWT.initialize(app) as manager:
    manager.config.secret_key = "secret"
    manager.config.private_claim_prefix = "sanic_jwt_extended"


@app.route("/login", methods=["POST"])
async def login(request: Request):
    username = request.json.get("username", "user")

    access_token = JWT.create_access_token(identity=username, private_claims={"foo": "bar"})

    return json(
        dict(access_token=access_token, refresh_token=refresh_token), status=200
    )


@app.route("/protected", methods=["GET"])
@jwt_required
async def protected(request: Request, token: Token):
    return json(dict(private_claims=token.private_claims))



if __name__ == "__main__":
    app.run()
```