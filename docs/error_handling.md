---
layout: default
title: Error Handling
nav_order: 4
---

# Error Handling
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

## Kind of handlers

`JWT.handler` has these handlers:

| Name                   | Exception to handle       |
|:-----------------------|:--------------------------|
| `no_authorization`     | `NoAuthorizationError`    |
| `expired_signature`    | `ExpiredSignatureError`   |
| `invalid_header`       | `InvalidHeaderError`      |
| `invalid_token`        | `InvalidTokenError`       |
| `jwt_decode_error`     | `JWTDecodeError`          |
| `wrong_token`          | `WrongTokenError`         |
| `revoked_token`        | `RevokedTokenError`       |
| `fresh_token_required` | `FreshTokenRequiredError` |
| `access_denied`        | `AccessDeniedError`       |

## Change behavior of handler 

First, you need to make function with this signature

```python
async def my_handler(request: sanic.request.Request, exception: JWTExtendedException) -> sanic.response.HTTPResponse: 
    ...
```

Then assign function to handler you want to modify while initializing `JWT`

```python
with JWT.initialize(app) as manager:
    manager.handler.no_authorization = my_handler
```