---
layout: default
title: Using Refresh Token
parent: Usages
nav_order: 2
---

## What Is Refresh Token?

Refresh token is a token carries the information necessary to get a new access token.

[Find more about refresh token at Auth0](https://auth0.com/blog/refresh-tokens-what-are-they-and-when-to-use-them/){: .btn .btn-purple }

# Using Refresh Token
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}


## Configuration

There's nothing to configurate to use refresh token.

## Create Refresh Token

<div class="code-example" markdown="1">
After `JWT` initialized and configured. you can create refresh token through `JWT.create_refresh_token`
</div>
```python
refresh_token = JWT.create_refresh_token(identity=username)
```
[Find more about creating token]({{ site.baseurl }}{% link usage/basic.md %}){: .btn .btn-outline }

## Protect Views

`jwt_require` or `jwt_optional` only accepts *access* tokens. so you should use `refresh_jwt_required` to protect view with **refresh token**

<div class="code-example" markdown="1">
Important
{: .label .label-yellow }
You should specify `token` keyword argument to view function(method) as same as `jwt_required`
</div>
```python
@app.route("/refresh", methods=["GET"])
@refresh_jwt_required
async def refresh(request: Request, token: Token):
    ...
```
[Find more about protecting views]({{ site.baseurl }}{% link usage/basic.md %}){: .btn .btn-outline }

---

## Full Example Code
{: .text-delta}


```python
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
```