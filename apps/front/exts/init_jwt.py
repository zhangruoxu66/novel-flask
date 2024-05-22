from functools import wraps

from flask import Flask, redirect, url_for, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

from pub.utils.http_utils import fail_api, is_ajax_request

jwt = JWTManager()


@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
    if is_ajax_request():
        return fail_api(code=1066, msg='身份认证信息已过期！')
    else:
        return redirect(url_for("user.to_login"))


def user_login_req(func):
    @jwt_required(optional=True)
    @wraps(func)
    def wrapper(*args, **kwargs):
        identity = get_jwt_identity()
        if not identity or not identity.get('id'):
            if is_ajax_request():
                return jsonify(success=False, code=1001, msg='未登录或登录失效！')
            else:
                return redirect(url_for("user.to_login", originUrl=request.url))

        return func(*args, **kwargs)

    return wrapper


def init_jwt(app: Flask):
    jwt.init_app(app)
