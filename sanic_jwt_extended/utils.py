async def create_access_token(app, identity, user_claims=None, role=None, fresh=False, expires_delta=None):
    """
    Create a new access token.

    :param app: A Sanic application from request object
    :param identity: The identity of this token, which can be any data that is
                     json serializable. It can also be a python object
    :param user_claims: User made claims that will be added to this token. it
                        should be dictionary.
    :param role: A role field for RBAC
    :param fresh: If this token should be marked as fresh, and can thus access
                  :func:`~sanic_jwt_extended.fresh_jwt_required` endpoints.
                  Defaults to `False`. This value can also be a
                  `datetime.timedelta` in which case it will indicate how long
                  this token will be considered fresh.
    :param expires_delta: A `datetime.timedelta` for how long this token should
                          last before it expires. Set to False to disable
                          expiration. If this is None, it will use the
                          'JWT_ACCESS_TOKEN_EXPIRES` config value
    :return: An encoded access token
    """
    return await app.jwt._create_access_token(app, identity, user_claims, role, fresh, expires_delta)


async def create_refresh_token(app, identity, user_claims=None, expires_delta=None):
    """
    Create a new refresh token.

    :param app: A Sanic application from request object
    :param identity: The identity of this token, which can be any data that is
                     json serializable. It can also be a python object
    :param user_claims: User made claims that will be added to this token. it
                        should be dictionary.
    :param expires_delta: A `datetime.timedelta` for how long this token should
                          last before it expires. Set to False to disable
                          expiration. If this is None, it will use the
                          'JWT_REFRESH_TOKEN_EXPIRES` config value
    :return: An encoded access token
    """
    return await app.jwt._create_refresh_token(app, identity, user_claims, expires_delta)
