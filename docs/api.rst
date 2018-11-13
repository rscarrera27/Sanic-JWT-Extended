API Documentation
=================
In here you will find the API for everything exposed in this extension.

Sanic-JWT-Extended
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. currentmodule:: sanic_jwt_extended

.. module:: sanic_jwt_extended

.. autoclass:: JWTManager

  .. automethod:: __init__
  .. automethod:: init_app

Protected endpoint decorators
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: jwt_required
.. autofunction:: jwt_refresh_token_required
.. autofunction:: fresh_jwt_required
.. autofunction:: jwt_optional


.. _Verify Tokens in Request:

Verify Tokens in Request
~~~~~~~~~~~~~~~~~~~~~~~~
These perform the same actions as the protected endpoint decorators, without
actually decorating a function. These are very useful if you want to create
your own decorators on top of sanic jwt extended (such as role_required), or

.. currentmodule:: sanic_jwt_extended.decorators

.. module:: sanic_jwt_extended.decorators

.. autofunction:: get_jwt_data_in_request_header
.. autofunction:: verify_jwt_data_type

Utilities
~~~~~~~~~
.. currentmodule:: sanic_jwt_extended

.. module:: sanic_jwt_extended

.. autofunction:: create_access_token
.. autofunction:: create_refresh_token

.. currentmodule:: sanic_jwt_extended.tokens

.. module:: sanic_jwt_extended.tokens

.. autofunction:: encode_access_token
.. autofunction:: encode_refresh_token

.. autofunction:: decode_jwt

Token Object
~~~~~~~~~~~~
.. currentmodule:: sanic_jwt_extended.tokens

.. module:: sanic_jwt_extended.tokens

.. autoclass:: Token

    .. autoattribute:: raw_jwt
    .. autoattribute:: jwt_identity
    .. autoattribute:: jwt_user_claims
    .. autoattribute:: jti