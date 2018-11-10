
def create_access_token(app, identity, user_claims=None, fresh=False, expires_delta=None):
    return app.jwt._create_access_token(app, identity, user_claims, fresh, expires_delta)


def create_refresh_token(app, identity, user_claims=None, expires_delta=None):
    return app.jwt._create_refresh_token(app, identity, user_claims, expires_delta)