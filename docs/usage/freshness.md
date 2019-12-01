---
layout: default
title: Token Freshness
parent: Usages
nav_order: 5
---

## What is Fresh Token?
The fresh token pattern in [`flask-jwt-extended`](https://flask-jwt-extended.readthedocs.io/en/stable/token_freshness/) is also available in this extension. This pattern is very simple, you can choose to mark some access tokens as fresh and others as non-fresh

This is useful for allowing fresh tokens to do some critical things (such as update an email address or complete an online purchase), but to deny those features to non-fresh tokens. Utilizing Fresh tokens in conjunction with refresh tokens can lead to a more secure site, without creating a bad user experience by making users constantly re-authenticate.

# Token Freshness
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}


## Configuration

There's nothing to configurate to use fresh token pattern.

## Create Token

<div class="code-example" markdown="1">
Just pass `True` to `fresh` parameter when create access token
</div>
```python
access_token = JWT.create_access_token(identity=username, fresh=True)
```
[Find more about creating token]({{ site.baseurl }}{% link api_docs/jwt.md %}#class-sanic_jwtextendedjwt){: .btn .btn-outline }

## Protect Views

By decorate view function(method) with `jwt_required`, you can check token freshness

<div class="code-example" markdown="1">
Pass `True` to `fresh_required` parameter of `jwt_required`.
</div>
```python
@app.route("/protected", methods=["GET"])
@jwt_required(fresh_required=True)
async def protected(request: Request, token: Token):
    ...
```
[Find more about protecting views]({{ site.baseurl }}{% link usage/basic.md %}){: .btn .btn-outline }

## Use Token Object

propagated `Token` object contains freshness info in `Token.fresh`. if token type is not `access` or freshness not specifed, default value is `None` 

```python
token.fresh  # nullable
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


@app.route("/login", methods=["POST"])
async def login(request: Request):
    username = request.json.get("username", "user")

    access_token = JWT.create_access_token(identity=username, fresh=True)

    return json(
        dict(access_token=access_token), status=200
    )


@app.route("/protected", methods=["GET"])
@jwt_required(fresh_required=True)
async def protected(request: Request, token: Token):
    return json(dict(identity=token.identity, is_fresh=token.fresh, raw_data=token.raw_data, exp=str(token.exp)))


if __name__ == "__main__":
    app.run()
```