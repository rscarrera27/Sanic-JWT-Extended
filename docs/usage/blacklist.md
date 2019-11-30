---
layout: default
title: Blacklist and Token Revoking
parent: Usages
nav_order: 6
---

## What is Blacklist?
Blacklist is used to revoke a specific token so that it can be no longer access your endpoints.

Blacklisting works by providing blacklist. This blacklist's method to check revoked called when token tries to access endpoint. If the blacklist's method says that the token is revoked, we will reject request.

basically we provides `InMemoryBlacklist` and `RedisBlacklist`. or you can create your own blacklist by inherit `BlacklistABC`

# Blacklist and Token Revoking
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}


## Configuration

First, you should enable `use_blacklist` option

```python
with JWT.initialize(app) as manager:
    manager.config.use_blacklist = True
```

Then, provide instanciable blacklist **class** (not instance). if not provided, extension will use `InMemoryBlacklist` by default

```python
with JWT.initialize(app) as manager:
    manager.config.blacklist_class = RedisBlacklist
```

[Find more about configuration]({{ site.baseurl }}{% link usage/basic.md %}){: .btn .btn-outline }

## Protect Views

There is nothing to configure to check revoked tokens. decorator automatically rejects revoked token if `use_blacklist` is `True`

## Revoke Tokens

If you want to revoke specific token, just pass token object to `JWT.revoke`.

```python
JWT.revoke(token)
```

## Built-In Blacklist Class

### `InMemoryBlacklist`

Do not use in production environment!
{: .text-red-100 .code-example }

This blacklist uses python `list` as a token storage. revoked token's `jti` will be contained.

### `RedisBlacklist`

This blacklist uses `redis` as a token storage. When token revoked, this blacklist stores token's `jti` with expiration.

## Creating Your Own Blacklist Class

DON'T PANIC!
{: .text-purple-100 .code-example }

Creating your own blacklist is very easy. Just inherit `BlacklistABC` and implements `register` and `is_blacklisted` and `__init__` with no argument.

```python
class FooBarBlacklist(BlacklistABC):
    def __init__(self):  # no argument!
        pass

    def register(self, token: Token):
        pass

    def is_blacklisted(self, token: Token):
        pass
```


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
    manager.config.use_blacklist = True


@app.route("/login", methods=["POST"])
async def login(request: Request):
    username = request.json.get("username", "user")

    access_token = JWT.create_access_token(identity=username)

    return json(
        dict(access_token=access_token), status=200
    )


@app.route("/logout", methods=["POST"])
@refresh_jwt_required
async def logout(request: Request, token: Token):

    JWT.revoke(token)

    return json(
        dict(msg="Goodbye"), status=200
    )


@app.route("/protected", methods=["GET"])
@jwt_required
async def protected(request: Request, token: Token):
    return json(dict(identity=token.identity, type=token.type, raw_data=token.raw_data, exp=str(token.exp)))


if __name__ == "__main__":
    app.run()
```