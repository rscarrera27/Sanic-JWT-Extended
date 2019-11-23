from sanic.response import json


class Handler:
    no_authorization = lambda e: json({"msg": str(e)})
