from flask import Flask

from core.flask_redis_token import FlaskRedisToken

frt = FlaskRedisToken()


def init_flask_redis_token(app: Flask):
    frt.init_app(app)
