# Sanic-JWT-Extended 
[![Downloads](https://pepy.tech/badge/sanic-jwt-extended)](https://pepy.tech/project/sanic-jwt-extended)

## What is Sanic-JWT-Extended?
Sanic-JWT-Extended is Sanic version of Flask-JWT-Extended. this is stable, 
but some features of Flask-JWT-Extended is not implemented yet. so this currently WIP.

## When to use Flask-JWT-Extended?
Sanic-JWT-Extended not only adds support for using JSON Web Tokens (JWT) to Sanic for protecting views,
but also many helpful (and **optional**) features  built in to make working with JSON Web Tokens
easier. These include:

* Support for adding custom claims to JSON Web Tokens
* [Refresh tokens](https://auth0.com/blog/refresh-tokens-what-are-they-and-when-to-use-them/)
* Token freshness and separate view decorators to only allow fresh tokens
* Role-based access control

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
