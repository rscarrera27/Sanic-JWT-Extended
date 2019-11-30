---
layout: default
title: Configuration Options
nav_order: 3
---

# Configuration Option

## Secrets

| KEY        | description                           | TYPE   | default |
|:-----------|:--------------------------------------|:-------|:--------|
| secret_key | encode/decode key for `HS*` algorithm | string | `None`  |
| public_key | decode key for `RS*` algorithm        | string | `None`  |
| secret_key | encode key for `RS*` algorithm        | string | `None`  |

## Default Values for Reserved Claims

| KEY         | description      | TYPE          | default |
|:------------|:-----------------|:--------------|:--------|
| default_iss | default issuer   | string or URI | `None`  |
| default_aud | default audience | string or URI | `None`  |

## General Configs

| key                   | description                                                                                                                                                                                                    | TYPE                          | default                 |
|:----------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------------------------|:------------------------|
| json_encoder          | json encoder                                                                                                                                                                                                   | Any                           | `JSONEncoder`           |
| token_location        | Where to look for a JWT when processing a request. The options are `headers`, `cookies` or `query_string`. You can pass in a sequence or a set to check more then one location, such as: `(headers, cookies)`. | Tuple[string]                 | `("header",)`           |
| access_token_expires  | How long an access token should live before it expires.                                                                                                                                                        | datetime.timedelta or `False` | `timedelta(minutes=15`) |
| refresh_token_expires | How long an refresh token should live before it expires.                                                                                                                                                       | datetime.timedelta or `False` | `timedelta(days=30) `   |
| algorithm             | Which algorithm to sign the JWT with. [See here](https://pyjwt.readthedocs.io/en/latest/algorithms.html) for the options.                                                                                      | string                        | `"HS256" `              |


## Additional Claim Configs

| key                    | description                 | type          | default |
|:-----------------------|:----------------------------|:--------------|:--------|
| public_claim_namespace | namespace for public claims | string or URI | `""`    |
| private_claim_prefix   | prefix for pricate claims   | string or URI | `""`    |

## Header Configs

| key               | description                                   | type   | default           |
|:------------------|:----------------------------------------------|:-------|:------------------|
| jwt_header_key    | What header to look for the JWT in a request. | string | `"Authorization"` |
| jwt_header_prefix | What type of header the JWT is in.            | string | `"Bearer"`        |

## Query Parameter Options

| key                  | description                                               | type   | default |
|:---------------------|:----------------------------------------------------------|:-------|:--------|
| jwt_query_param_name | What query paramater name to look for a JWT in a request. | string | `"jwt"` |

## Access Control Configs

| key       | description                    | type   | default      |
|:----------|:-------------------------------|:-------|:-------------|
| use_acl   | Enable/disable access control  | bool   | `False`      |
| acl_claim | Which claim to store role info | string | `permission` |

## Blacklist Configs

| key             | description                    | type               | default             |
|:----------------|:-------------------------------|:-------------------|:--------------------|
| use_blacklist   | Enable/disable token revoking. | bool               | `False`             |
| blacklist_class | Blacklist class to use         | Type[BlacklistABC] | `InMemoryBlacklist` |