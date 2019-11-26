---
layout: default
title: Token Freshness
parent: Usages
nav_order: 5
---
# Basic Usage
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}


## Configuration

First, you should initialize and configure `JWT` through `JWT.initialize` context  manager.

<div class="code-example" markdown="1">
Important
{: .label .label-yellow }
You must specify `secret_key` or `private_key` + `public_key` that needed to encode JWT with `algorithm`
</div>
```python
with JWT.initialize(app) as manager:
    manager.config.secret_key = "secret"
```
[Find more about configuration]({{ site.baseurl }}{% link usage/basic.md %}){: .btn .btn-outline }

## Create Token

<div class="code-example" markdown="1">
After `JWT` initialized and configured. you can create access token through `JWT.create_access_token`
</div>
```python
access_token = JWT.create_access_token(identity=username)
```
[Find more about creating token]({{ site.baseurl }}{% link usage/basic.md %}){: .btn .btn-outline }

## Protect Views

By decorate view function(method) with `jwt_required` or `jwt_optional`, You can protect view with JWT.

<div class="code-example" markdown="1">
Important
{: .label .label-yellow }
You should specify `token` keyword argument to view function(method) 
</div>
```python
@app.route("/protected", methods=["GET"])
@jwt_required
async def protected(request: Request, token: Token):
    ...
```
[Find more about protecting views]({{ site.baseurl }}{% link usage/basic.md %}){: .btn .btn-outline }

## Use Token Object

`jwt_required` and `jwt_optional` injects `Token` to your view function/method. by `token` keyword argument.
and given token object contains useful data of given JWT.

```python
token.identity  # identity(sub) of JWT
token.exp  # expiration(exp) of JWT
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

    access_token = JWT.create_access_token(identity=username)

    return json(
        dict(access_token=access_token), status=200
    )


@app.route("/protected", methods=["GET"])
@jwt_required
async def protected(request: Request, token: Token):
    return json(dict(identity=token.identity, type=token.type, raw_data=token.raw_data, exp=str(token.exp)))


if __name__ == "__main__":
    app.run()
```