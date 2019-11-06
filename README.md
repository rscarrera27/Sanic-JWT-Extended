# Sanic-JWT-Extended (NOW PREPARING 1.0 RELEASE WITH MAJOR CHANGES)
[![Downloads](https://pepy.tech/badge/sanic-jwt-extended)](https://pepy.tech/project/sanic-jwt-extended)
![PyPI](https://img.shields.io/pypi/v/sanic-jwt-extended.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sanic-jwt-extended.svg)
![code style](https://img.shields.io/badge/code%20style-black-black.svg)
[![Documentation Status](https://readthedocs.org/projects/sanic-jwt-extended/badge/?version=latest)](https://sanic-jwt-extended.readthedocs.io/en/latest/?badge=latest)

## What is Sanic-JWT-Extended?
Sanic-JWT-Extended is port of Flask-JWT-Extended for Sanic.

## When to use Sanic-JWT-Extended?
Sanic-JWT-Extended not only adds support for using JSON Web Tokens (JWT) to Sanic for protecting views,
but also many helpful (and **optional**) features  built in to make working with JSON Web Tokens
easier. These include:

* Support for adding custom claims to JSON Web Tokens
* [Refresh tokens](https://auth0.com/blog/refresh-tokens-what-are-they-and-when-to-use-them/)
* Token freshness and separate view decorators to only allow fresh tokens
* Role-based access control
* ~~built-in blacklist support~~ <= WIP

## Installation
```bash
pip install sanic-jwt-extended
```

## Usage
[View the documentation online](http://sanic-jwt-extended.readthedocs.io/en/latest/)

## Generating Documentation
You can generate a local copy of the documentation. After installing the requirements,
go to the `docs` directory and run:
```
$ make clean && make html
```
