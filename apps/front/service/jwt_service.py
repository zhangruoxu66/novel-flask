from collections import namedtuple

from flask import current_app
from flask_jwt_extended import create_access_token, create_refresh_token, get_csrf_token


def gen_all_cookie(identity) -> namedtuple:
    jwt_access_token = create_access_token(identity=identity)
    access_refresh_token = create_refresh_token(identity)
    if current_app.config['JWT_COOKIE_CSRF_PROTECT']:
        csrf_access_token = get_csrf_token(jwt_access_token)
        csrf_refresh_token = get_csrf_token(access_refresh_token)
    else:
        csrf_access_token = None
        csrf_refresh_token = None

    jwt_tokens = namedtuple(
        'jwt_tokens', ['access_token', 'access_refresh_token', 'csrf_token', 'csrf_refresh_token']
    )
    return jwt_tokens(
        access_token=jwt_access_token, access_refresh_token=access_refresh_token,
        csrf_token=csrf_access_token, csrf_refresh_token=csrf_refresh_token
    )
