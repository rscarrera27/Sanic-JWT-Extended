---
layout: default
title: View Decorators
parent: API Documentation
nav_order: 2
---

# View Decorators

### *def* **jwt_required**
{: .text-purple-100 .text-mono}

A decorator to protect a Sanic endpoint.
{: .pl-6}

If you decorate an endpoint with this, it will ensure that the requester has a valid access token before allowing the endpoint to be called. 
{: .pl-6}

If blacklist has enabled, the decorator automatically checks token in request has been revoked.
{: .pl-6}

Endpoint to be decorated must specify `token` keyword argument to take over token object.
{: .pl-6}

```python
@app.route("/protected", methods=["GET"])
@jwt_required
async def protected(request, token):
    ...
```
{: .pl-6}

By enable `fresh_required` option, You can check the freshness of the access token.
{: .pl-6 }
```python
@app.route("/protected", methods=["GET"])
@jwt_required(fresh_required=True)
async def protected(request, token):
    ...
```
{: .pl-6}

By specify `allow` or `deny` option, You can control which roles has permission. if access control is enabled, 
{: .pl-6 }
```python
@app.route("/protected", methods=["GET"])
@jwt_required(allow=["ADMIN", "SUPER_ADMIN", ])
async def protected(request, token):
    ...
```
{: .pl-6}

#### Parmeters
{: .pl-6 .fs-4 .text-purple-000}

- `fresh_required` - A boolean to enable option
{: .pl-6}

- `allow` - A list of roles that expected to be allowed. this can't be used with `deny` together
{: .pl-6}

- `deny` - A list of roles that expected to be denied. this can't be used with `allow` together
{: .pl-6}

### *def* **jwt_optional**
{: .text-purple-100 .text-mono}

A decorator to optionally protect a Sanic endpoint.
{: .pl-6}

This means decorated endpoint will still be called if no access token is present in the request. but decorator will propagate `None` instead of valid token object
{: .pl-6}

But if there is an invalid access token in the request (expired, tampered with, etc), this will still call the appropriate error handler instead of allowing the endpoint to be called as if there is no access token in the request.
{: .pl-6}

```python
@app.route("/protected", methods=["GET"])
@jwt_optional
async def protected(request: Request, token: Optional[Token]):
    ...
```
{: .pl-6}

#### Parmeters
{: .pl-6 .fs-4 .text-purple-000}

This decorator dosen't requries any parameter
{: .pl-6 .text-grey-dk-000}



### *def* **refresh_jwt_required**
{: .text-purple-100 .text-mono}

A decorator to protect a Sanic endpoint.
{: .pl-6}

If you decorate an endpoint with this, it will ensure that the requester has a valid request token before allowing the endpoint to be called.
{: .pl-6}

If blacklist has enabled, the decorator automatically checks token in request has been revoked.
{: .pl-6}

Endpoint to be decorated must specify `token` keyword argument to take over token object.
{: .pl-6}


#### Parmeters
{: .pl-6 .fs-4 .text-purple-000}

- `fresh_required` - A boolean to enable option
{: .pl-6}

- `allow` - A list of roles that expected to be allowed. this can't be used with `deny` together
{: .pl-6}

- `deny` - A list of roles that expected to be denied. this can't be used with `allow` together
{: .pl-6}