<h1 align="center">🛡 Sanic-JWT-Extended 🛡</h1>

<div align="center"> 


|           |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
|:----------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Buiild    | [![Tests](https://github.com/NovemberOscar/Sanic-JWT-Extended/workflows/Tests/badge.svg)](https://github.com/NovemberOscar/Sanic-JWT-Extended/actions?query=workflow%3ATests) [![Deploy](https://github.com/NovemberOscar/Sanic-JWT-Extended/workflows/Upload%20to%20PyPI/badge.svg)](https://github.com/NovemberOscar/Sanic-JWT-Extended/actions?query=workflow%3A%22Upload+to+PyPI%22) [![Netlify](https://img.shields.io/netlify/c2cf1ea1-bae1-448f-b52c-0dea6516446a?label=docs)](https://app.netlify.com/sites/sanic-jwt-extended/deploys)                                                                                         |
| Quality   | [![codecov](https://codecov.io/gh/NovemberOscar/Sanic-JWT-Extended/branch/master/graph/badge.svg)](https://codecov.io/gh/NovemberOscar/Sanic-JWT-Extended) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/5fe125514047445b80d6e3e75c2a7dbe)](https://www.codacy.com/manual/NovemberOscar/Sanic-JWT-Extended?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=NovemberOscar/Sanic-JWT-Extended&amp;utm_campaign=Badge_Grade) [![Maintainability](https://api.codeclimate.com/v1/badges/368dbc256c4837087c1e/maintainability)](https://codeclimate.com/github/NovemberOscar/Sanic-JWT-Extended/maintainability) |
| Package   | ![PyPI](https://img.shields.io/pypi/v/sanic-jwt-extended.svg?label=stable) ![GitHub release (latest SemVer including pre-releases)](https://img.shields.io/github/v/release/NovemberOscar/Sanic-JWT-Extended?include_prereleases&label=latest) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sanic-jwt-extended.svg)                                                                                                                                                                                                                                                                                                  |
| Stats     | [![Downloads](https://pepy.tech/badge/sanic-jwt-extended)](https://pepy.tech/project/sanic-jwt-extended)    [![Downloads](https://pepy.tech/badge/sanic-jwt-extended/month)](https://pepy.tech/project/sanic-jwt-extended/month)                                                                                                                                                                                                                                                                                                                                                                                                        |
| Community | [![Gitter](https://badges.gitter.im/Sanic-JWT-Extended/community.svg)](https://gitter.im/Sanic-JWT-Extended/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
</div>

> **☢️ This is README of 1.0 version. [Click here](https://github.com/NovemberOscar/Sanic-JWT-Extended/tree/v0.4.4) to checkout legacy version(v0.4.4)**

## 🚀 What is Sanic-JWT-Extended?
Sanic-JWT-Extended is an open source Sanic extension that provides JWT support (comply with RFC standard)

## 💡 Why Sanic-JWT-Extended?
Sanic-JWT-Extended not only adds support for using JSON Web Tokens (JWT) to Sanic for protecting views,
but also many helpful (and **optional**) features  built in to make working with JSON Web Tokens
easier. These include:

* Support for adding public claims with [namespacing](https://auth0.com/docs/tokens/concepts/claims-namespacing)
* Support for adding private claims
* [Refresh tokens](https://auth0.com/blog/refresh-tokens-what-are-they-and-when-to-use-them/)
* Token freshness and separate view decorators to only allow fresh tokens
* Access control
* blacklist support with some built-in blacklist
* Provides Token object for easier jwt manifulation

## ⚡️ Installation
```shell script
$ pip install sanic-jwt-extended --pre
```
```shell script
$ poetry add sanic-jwt-extended --git https://github.com/NovemberOscar/Sanic-JWT-Extended.git
```
```shell script
$ pipenv install sanic-jwt-extended --pre
```

## 📚 Documentation
<a href="https://sanic-jwt-extended.seonghyeon.dev">
<img src="https://i.imgur.com/eXRmcKO.png)](https://sanic-jwt-extended.seonghyeon.dev/" width="300" />
</a>


## 🛠 Developing Sanic-JWT-Extended

### Prerequesties
- [poetry](https://github.com/sdispater/poetry)

### Installaion
```shell script
$ make env
```
this will install dependencies with poetry. if poetry not found, will install poetry.

### Development
- `make format`: this will format your code with `isort` and `black`
- `make check`: this will lint your code with `isort`, `black`, `mypy` and `pylint`
- `make clean`: this will remove temporary things.

### Commit Convention
```
<{verb}>({scope}): {summary}
```
#### Example
- test: `<test>(foobar): Add TCs about FooBar`
- fix: `<fix>(#12): Fix SpamEgg`
- normal: `<feat>(cookie): Add cookie writer`

### Testing
```shell script
$ make check  # check convention and type
$ poetry run pytest
```

with coverage:
```shell script
$ poetry run pytest --cov=sanic_jwt_extended tests/
```

**Make sure you wrote TCs about your work!**