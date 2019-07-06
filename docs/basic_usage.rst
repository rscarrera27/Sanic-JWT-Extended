Basic Usage
===========

In its simplest form, there is not much to using flask_jwt_extended. You use
:func:`~sanic_jwt_extended.create_access_token` to make new access JWTs,
the :func:`~sanic_jwt_extended.jwt_required` decorator to protect endpoints,
and :py:attr:`~sanic_jwt_extended.Token.jwt_identity` in the given token argument to get the identity
of a JWT in a protected endpoint.

.. literalinclude:: ../examples/basic.py

To access a jwt_required protected view, all we have to do is send in the
JWT with the request. By default, this is done with an authorization header
that looks like:

.. code-block :: bash

  Authorization: Bearer <access_token>


We can see this in action using CURL:

.. code-block :: bash

  $ curl http://localhost:5000/protected
  {
    "msg": "Missing Authorization Header"
  }

  $ curl -H "Content-Type: application/json" -X POST \
    -d '{"username":"test","password":"test"}' http://localhost:8000/login
  {
    "access_token": <ACCESS TOKEN>"
  }

  $ curl -H "Authorization: Bearer <ACCESS TOKEN>" http://localhost:5000/protected
  {
    "logined_as": "test"
  }

NOTE: Remember to change the secret key of your application, and insure that no
one is able to view it. The JSON Web Tokens are signed with the secret key, so
if someone gets that, they can create arbitrary tokens, and in essence log in
as any user.
