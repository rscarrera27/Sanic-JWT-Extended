<h1 align="center">🛡 Sanic-JWT-Extended 🛡</h1>

<div align="center"> 

[![Downloads](https://pepy.tech/badge/sanic-jwt-extended)](https://pepy.tech/project/sanic-jwt-extended)
![PyPI](https://img.shields.io/pypi/v/sanic-jwt-extended.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sanic-jwt-extended.svg)
![code style](https://img.shields.io/badge/code%20style-black-black.svg)
[![Documentation Status](https://api.netlify.com/api/v1/badges/c2cf1ea1-bae1-448f-b52c-0dea6516446a/deploy-status)](https://sanic-jwt-extended.seonghyeon.dev)

</div>

> **☢️ This is README of 1.0.dev version. [Click here](https://github.com/NovemberOscar/Sanic-JWT-Extended/tree/v0.4.4) to checkout current stable version(v0.4.4)**

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
<button 
href="https://sanic-jwt-extended.seonghyeon.dev/" 
style="
    display: inline-block;
    box-sizing: border-box;
    padding-top: 0.3em;
    padding-right: 1em;
    padding-bottom: 0.3em;
    padding-left: 1em;
    margin: 0;
    font-family: inherit;
    font-size: inherit;
    font-weight: 500;
    line-height: 1.5;
    color: #7253ed;
    text-decoration: none;
    vertical-align: baseline;
    cursor: pointer;
    background-color: #f7f7f7;
    border-width: 0;
    border-radius: 4px;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.12), 0 3px 10px rgba(0, 0, 0, 0.08);
    appearance: none;
    color: #fff;
    background-color: #5739ce;
    background-image: linear-gradient(#6f55d5, #5739ce);
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.25), 0 4px 10px rgba(0, 0, 0, 0.12);"
    >
Go to documentation
</button>


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
- `make check`: this will lint your code with `isort`, `black`, and `pylint`
- `make clean`: this will remove temporary things.

### Commit Convention
```
<{verb}>({scope}): {summary}
```

### Testing
- **TBD**
