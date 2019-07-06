Role-based access control(RBAC)
=========================

Sanic-JWT-Extended supports RBAC.

all you have to do is just make ``'RBAC_ENABLE'`` option to ``'True'``, give role
to jwt with ``'role'`` option in :func:`~sanic_jwt_extended.create_access_token`.
and specify role to allow or deny when using :func:`~sanic_jwt_extended.jwt_required`
and :func:`~sanic_jwt_extended.fresh_jwt_required`

.. warning::  ``'deny'`` and ``'allow'`` option **can not** be used together.

.. literalinclude:: ../examples/rbac.py



