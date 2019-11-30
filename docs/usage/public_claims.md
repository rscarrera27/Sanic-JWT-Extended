---
layout: default
title: Storing Public Claims 
parent: Usages
nav_order: 3
---

## What Is Public Claims?

Claims for public consumption, which might contain generic information like "name" and "email".

[Find more about public claims at Auth0](https://auth0.com/docs/tokens/jwt-claims#public-claims){: .btn .btn-purple }

# Storing Public Claims
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}


## Configuration

You should configure `JWT.config.public_claim_namespace`. for claim [namespacing](https://auth0.com/docs/tokens/concepts/claims-namespacing) (it is required to create collision-resistant names) 

<div class="code-example" markdown="1">
Important
{: .label .label-yellow }
It is **highly recommended** to use URL(with trailing slash) for namespace!
</div>
```python
```python
with JWT.initialize(app) as manager:
    manager.config.public_claim_namespace = "https://jwt.io/"
```
[Find more about configuration]({{ site.baseurl }}{% link usage/basic.md %}){: .btn .btn-outline }

## Create Token

Both access and refresh token can contain public claims. you must insert public claims in mapping

<div class="code-example" markdown="1">
Important
{: .label .label-yellow }
`public_claims` argument is **keyword-only** argument!
</div>
```python
refresh_token = JWT.create_access_token(identity=username, public_claims={"sso_user_id": "asdf", "user_info": {"name": "foo"}})
```

propagated map of public claims will be flatten and url-form

```json
{
    ...
    "https://jwt.io/sso_user_id": "asdf",
    "https://user/info/name": "foo"
    ...
}
```

[Find more about creating token]({{ site.baseurl }}{% link usage/basic.md %}){: .btn .btn-outline }

## Protect Views

There's nothing to configurate to get public claims

## Use Token Object

propagated `Token` object contains public claims in `Token.public_claims`. namespace prefix is not exist on this time. ( converted in original mapping you propagated, not flatten and namespaced form.)

```python
token.public_claims
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

from sanic_jwt_extended import JWT, refresh_jwt_required 
from sanic_jwt_extended.tokens import Token

app = Sanic(__name__)


with JWT.initialize(app) as manager:
    manager.config.secret_key = "secret"
    manager.config.public_claim_namespace = "https://jwt.io/"


@app.route("/login", methods=["POST"])
async def login(request: Request):
    username = request.json.get("username", "user")

    access_token = JWT.create_access_token(identity=username, public_claims={"foo": "bar"})

    return json(
        dict(access_token=access_token, refresh_token=refresh_token), status=200
    )


@app.route("/protected", methods=["GET"])
@jwt_required
async def protected(request: Request, token: Token):
    return json(dict(public_claims=token.public_claims))




if __name__ == "__main__":
    app.run()
```