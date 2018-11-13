Insert User Claims
=====================

You may want to store additional information in the access token which you could
later access in the protected views. This can be done with the fill the `user_claims`
parameter in the :func:`~sanic_jwt_extended.create_access_token`
and :func:`~sanic_jwt_extended.create_refresh_token` and the data can be
accessed later in a protected endpoint with :py:attr:`~sanic_jwt_extended.Token.jwt_user_claims`
in the given token argument.

Storing data in an access token can be good for performance. If you store data
in the token, you wont need to look it up from disk next time you need it in
a protected endpoint. However, you should take care what data you put in the
token. Any data in the access token can be trivially viewed by anyone who can
read the token. **Do not** store sensitive information in access tokens!

.. literalinclude:: ../examples/user_claims.py
