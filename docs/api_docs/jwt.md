---
layout: default
title: JWT
parent: API Documentation
nav_order: 1
---

# JWT

## *class* **sanic_jwt.extended.JWT**
{: .text-purple-100 .text-mono}

A class to hold configs, create and revoke tokens. 

All methods this class has is classmethod. It's recommended to use without instanciate


### *def* **initialize**
{: .pl-6 .text-purple-100 .text-mono}

A classmethod to initialize class with context manager
{: .pl-10}

#### Parmeters
{: .pl-10 .fs-4 .text-purple-000}

- `app` - A Sanic application
{: .pl-10}

#### Return
{: .pl-10 .fs-4 .text-purple-000}

- ContextManager[JWT] - A context manager to setup extension
{: .pl-10}


### *def* **create_access_token**
{: .pl-6 .text-purple-100 .text-mono}

A classmethod to create new access token
{: .pl-10}

#### Parmeters
{: .pl-10 .fs-4 .text-purple-000}

- `identity` <sup>required</sup> - The identity of this token, which can be any data that is json serializable.
{: .pl-10}

- `role` - A string to specify role of access token for access control. 
{: .pl-10}

- `fresh` - A boolean to mark token as **fresh**. 
{: .pl-10}

- `expires_delta` - A `datetime.timedelta` to change time to expire. defaults to config's `access_token_expires`. this parameter is *positional-only*
{: .pl-10}

- `public_claims` - Optional JSON serializable to add public claims to token. this parameter is *positional-only*
{: .pl-10}

- `private_claims` - Optional JSON serializable to add private claims to token. this parameter is *positional-only*
{: .pl-10}

- `iss`
{: .pl-10}

- `aud`
{: .pl-10}

- `nbf`
{: .pl-10}


#### Return
{: .pl-10 .fs-4 .text-purple-000}

- str - An encoded access token
{: .pl-10}


### *def* **create_refresh_token**
{: .pl-6 .text-purple-100 .text-mono}

A classmethod to create new refresh token
{: .pl-10}

#### Parmeters
{: .pl-10 .fs-4 .text-purple-000}

- `identity` <sup>required</sup> - The identity of this token, which can be any data that is json serializable.
{: .pl-10}

- `role` - A string to specify role of access token for access control. 
{: .pl-10}

- `expires_delta` - A `datetime.timedelta` to change time to expire. defaults to config's `access_token_expires`. this parameter is *positional-only*
{: .pl-10}

- `public_claims` - Optional JSON serializable to add public claims to token. this parameter is *positional-only*
{: .pl-10}

- `private_claims` - Optional JSON serializable to add private claims to token. this parameter is *positional-only*
{: .pl-10}

- `iss`
{: .pl-10}

- `aud`
{: .pl-10}

- `nbf`
{: .pl-10}


#### Return
{: .pl-10 .fs-4 .text-purple-000}

- str - An encoded refresh token
{: .pl-10}


### *async def* **revoke**
{: .pl-6 .text-purple-100 .text-mono}

A classmethod to revoke specific token. revoked token will be stored to designated blacklist.
{: .pl-10}

#### Parmeters
{: .pl-10 .fs-4 .text-purple-000}

- `identity` <sup>required</sup> - A token object to revoke
{: .pl-10}


---

## Signature of JWT
```python
class JWT:
    config: Config = ...
    handler: Handler = ...
    blacklist: Optional[BlacklistABC] = ...

    @classmethod
    def initialize(cls: JWT, app: Sanic) -> ContextManager[JWT]: ...

    @classmethod
    def create_access_token(
        cls: JWT,
        identity: str,
        role: str = ...,
        fresh: bool = ...,
        *,
        expires_delta: datetime.timedelta = ...,
        public_claims: Dict[str, Any] = ...,
        private_claims: Dict[str, Any] = ...,
        iss: str = ...,
        aud: str = ...,
        nbf: datetime.datetime = ...,
    ) -> str: ...

    @classmethod
    def create_refresh_token(
        cls: JWT,
        identity: str,
        role: str = ...,
        *,
        expires_delta: datetime.timedelta = ...,
        public_claims: Dict[str, Any] = ...,
        private_claims: Dict[str, Any] = ...,
        iss: str = ...,
        aud: str = ...,
        nbf: datetime.datetime = ...,
    ) -> str: ...

    @classmethod
    async def revoke(cls: JWT, token: Token): ...

```