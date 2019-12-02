---
layout: default
title: Token Object
parent: API Documentation
nav_order: 3
---

# Token Object

## *class* **sanic_jwt.extended.tokens.Token**
{: .text-purple-100 .text-mono}

An object to hold token data(both encoded string and decoded data) 

This object has **no** public methods.

### Ⓟ ***raw_jwt***: str
{: .pl-6 .text-purple-100 .text-mono}
- An encoded raw jwt string
{: .pl-10}

### Ⓟ ***raw_data***: Dict[str, Any]
{: .pl-6 .text-purple-100 .text-mono}
- A decoded raw jwt data
{: .pl-10}

### Ⓟ ***type***: str
{: .pl-6 .text-purple-100 .text-mono}
- Type of token. `access` or `refresh`
{: .pl-10}

### Ⓟ ***role***: Optional[str]
{: .pl-6 .text-purple-100 .text-mono}
- Role of token. `None` if token has no role
{: .pl-10}

### Ⓟ ***fresh***: Optional[bool]
{: .pl-6 .text-purple-100 .text-mono}
- A boolean that represents freshness of token
{: .pl-10}

### Ⓟ ***identity***: str
{: .pl-6 .text-purple-100 .text-mono}
- The identity of token. alias of `sub`
{: .pl-10}

### Ⓟ ***iss***: Optional[str]
{: .pl-6 .text-purple-100 .text-mono}
- The issuer of token
{: .pl-10}

### Ⓟ ***sub***: str
{: .pl-6 .text-purple-100 .text-mono}
- A subject of token
{: .pl-10}

### Ⓟ ***aud***: Optional[str]
{: .pl-6 .text-purple-100 .text-mono}
- An audience of token
{: .pl-10}

### Ⓟ ***exp***: Optional[datetime.datetime]
{: .pl-6 .text-purple-100 .text-mono}
- A expiration of token
{: .pl-10}

### Ⓟ ***nbf***: datetime.datetime
{: .pl-6 .text-purple-100 .text-mono}
- `Not valid before`
{: .pl-10}

### Ⓟ ***iat***: datetime.datetime
{: .pl-6 .text-purple-100 .text-mono}
- `Issued At`
{: .pl-10}

### Ⓟ ***jti***: uuid.UUID
{: .pl-6 .text-purple-100 .text-mono}
- A unique value(uuid) of token

### Ⓟ ***public_claims***: Dict[str, Any]
{: .pl-6 .text-purple-100 .text-mono}
- Public claims 

### Ⓟ ***private_claims***: Dict[str, Any]
{: .pl-6 .text-purple-100 .text-mono}
- Private claims

## Signature of Token

```python
class Token:
    raw_jwt: str
    raw_data: Dict[str, Any] = ...
    type: str = ...
    role: Optional[str] = ...
    fresh: Optional[bool] = ...
    identity: str = ...
    iss: Optional[str] = ...
    sub: str = ...
    aud: Optional[str] = ...
    exp: Optional[datetime.datetime] = ...
    nbf: datetime.datetime = ...
    iat: datetime.datetime = ...
    jti: uuid.UUID = ...
    public_claims: Dict[str, Any] = ...
    private_claims: Dict[str, Any] = ...
```

