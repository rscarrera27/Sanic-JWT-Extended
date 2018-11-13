.. _Configuration Options:

Configuration Options
=====================

You can change many options for how this extension works via

.. code-block:: python

  app.config[OPTION_NAME] = new_options

General Options:
~~~~~~~~~~~~~~~~

.. tabularcolumns:: |p{6.5cm}|p{8.5cm}|

================================= =========================================
``JWT_TOKEN_LOCATION``            Where to look for a JWT when processing a request. The
                                  options are ``'headers'``, ``'cookies'``, ``'query_string'``, or ``'json'``. You can pass
                                  in a list to check more then one location, such as: ``['headers', 'cookies']``.
                                  Defaults to ``'headers'``
``JWT_ACCESS_TOKEN_EXPIRES``      How long an access token should live before it expires. This
                                  takes a ``datetime.timedelta``, and defaults to 15 minutes.
                                  Can be set to ``False`` to disable expiration.
``JWT_REFRESH_TOKEN_EXPIRES``     How long a refresh token should live before it expires. This
                                  takes a ``datetime.timedelta``, and defaults to 30 days.
                                  Can be set to ``False`` to disable expiration.
``JWT_ALGORITHM``                 Which algorithm to sign the JWT with. `See here <https://pyjwt.readthedocs.io/en/latest/algorithms.html>`_
                                  for the options. Defaults to ``'HS256'``.
``JWT_SECRET_KEY``                The secret key needed for symmetric based signing algorithms,
                                  such as ``HS*``. If this is not set, we use the
                                  flask ``SECRET_KEY`` value instead.
``JWT_IDENTITY_CLAIM``            Claim in the tokens that is used as source of identity.
                                  For interoperability, the JWT RFC recommends using ``'sub'``.
                                  Defaults to ``'identity'`` for legacy reasons.
``JWT_USER_CLAIMS``               Claim in the tokens that is used to store user claims.
                                  Defaults to ``'user_claims'``.
``JWT_CLAIMS_IN_REFRESH_TOKEN``   If user claims should be included in refresh tokens.
                                  Defaults to ``False``.
``JWT_ERROR_MESSAGE_KEY``         The key of the error message in a JSON error response when using
                                  the default error handlers.
                                  Defaults to ``'msg'``.
================================= =========================================


Header Options:
~~~~~~~~~~~~~~~
These are only applicable if ``JWT_TOKEN_LOCATION`` is set to use headers.

.. tabularcolumns:: |p{6.5cm}|p{8.5cm}|

================================= =========================================
``JWT_HEADER_NAME``               What header to look for the JWT in a request. Defaults to ``'Authorization'``
``JWT_HEADER_TYPE``               What type of header the JWT is in. Defaults to ``'Bearer'``. This can be
                                  an empty string, in which case the header contains only the JWT
                                  (insead of something like ``HeaderName: Bearer <JWT>``)
================================= =========================================
