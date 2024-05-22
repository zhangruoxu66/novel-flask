import datetime
from typing import Sequence, Iterable, Optional, List

from flask import Flask, current_app


class FlaskRedisToken:
    def __init__(self, app: Flask = None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        if not hasattr(app, "extensions"):
            app.extensions = {}
        app.extensions["flask-redis-token"] = self

        self._set_default_configuration_options(app)

    @staticmethod
    def _set_default_configuration_options(app: Flask) -> None:
        app.config.setdefault("FLASK_REDIS_TOKEN_LOGIN_VIEW", None)
        app.config.setdefault("FLASK_REDIS_TOKEN_SUPER_ADMIN_ROLE", None)
        app.config.setdefault("FLASK_REDIS_TOKEN_REMEMBER_ME", False)

        # redis相关
        app.config.setdefault("FLASK_REDIS_TOKEN_REDIS_HOST", "127.0.0.1")
        app.config.setdefault("FLASK_REDIS_TOKEN_REDIS_PORT", 6379)
        app.config.setdefault("FLASK_REDIS_TOKEN_REDIS_DB", 1)
        app.config.setdefault(
            "FLASK_REDIS_TOKEN_EXPIRES", datetime.timedelta(minutes=15)
        )

        # cookie相关
        app.config.setdefault("FLASK_REDIS_TOKEN_SESSION_COOKIE", True)
        app.config.setdefault("FLASK_REDIS_TOKEN_COOKIE_DOMAIN", None)
        app.config.setdefault("FLASK_REDIS_TOKEN_COOKIE_SECURE", False)
        app.config.setdefault("FLASK_REDIS_TOKEN_COOKIE_SAMESITE", None)
        app.config.setdefault("FLASK_REDIS_TOKEN_COOKIE_NAME", "flask_redis_token")
        app.config.setdefault("FLASK_REDIS_TOKEN_COOKIE_PATH", "/")
        app.config.setdefault("FLASK_REDIS_TOKEN_CSRF_COOKIE_NAME", "flask_redis_csrf_token")
        app.config.setdefault("FLASK_REDIS_TOKEN_CSRF_COOKIE_PATH", "/")

        # 存在redis中的key名称
        app.config.setdefault("FLASK_REDIS_TOKEN_FIELD_NAME", "token")
        app.config.setdefault("FLASK_REDIS_TOKEN_CSRF_FIELD_NAME", "CSRF_TOKEN")

        # csrf
        app.config.setdefault("FLASK_REDIS_TOKEN_CSRF_IN_COOKIES", True)
        app.config.setdefault("FLASK_REDIS_TOKEN_CSRF_HEADER_NAME", "FLASK-CSRF-TOKEN")
        app.config.setdefault("FLASK_REDIS_TOKEN_CSRF_PROTECT", False)
        app.config.setdefault("FLASK_REDIS_TOKEN_CSRF_METHODS", ["POST", "PUT", "PATCH", "DELETE"])

        # 设置token允许存在的位置，及不同位置中token的键名
        app.config.setdefault("FLASK_REDIS_TOKEN_LOCATION", ("headers", "cookies", "json", "query_string"))
        app.config.setdefault("FLASK_REDIS_TOKEN_HEADER_NAME", "Authorization")
        app.config.setdefault("FLASK_REDIS_TOKEN_FIELD_NAME", "flask_redis_token")


class Config(object):
    @property
    def login_view(self):
        return current_app.config["FLASK_REDIS_TOKEN_LOGIN_VIEW"]

    @property
    def redis_host(self) -> str:
        return current_app.config["FLASK_REDIS_TOKEN_REDIS_HOST"]

    @property
    def redis_port(self) -> int:
        return current_app.config["FLASK_REDIS_TOKEN_REDIS_PORT"]

    @property
    def redis_db(self) -> int:
        return current_app.config["FLASK_REDIS_TOKEN_REDIS_DB"]

    @property
    def redis_ex(self) -> datetime.timedelta:
        redis_ex = current_app.config["FLASK_REDIS_TOKEN_EXPIRES"]

        if redis_ex and not isinstance(redis_ex, datetime.timedelta):
            raise RuntimeError("FLASK_REDIS_TOKEN_EXPIRES必须是datetime.timedelta类型")

        return redis_ex

    @property
    def is_gen_cookie(self) -> bool:
        return current_app.config["FLASK_REDIS_TOKEN_GEN_COOKIE"]

    @property
    def cookie_domain(self) -> str:
        return current_app.config["FLASK_REDIS_TOKEN_COOKIE_DOMAIN"]

    @property
    def token_location(self) -> Sequence[str]:
        locations = current_app.config["FLASK_REDIS_TOKEN_LOCATION"]
        if isinstance(locations, str):
            locations = (locations,)
        elif not isinstance(locations, Iterable):
            raise RuntimeError("FLASK_REDIS_TOKEN_LOCATION must be a sequence or a set")
        elif not locations:
            raise RuntimeError(
                "FLASK_REDIS_TOKEN_LOCATION must contain at least one "
                'of "headers", "cookies", "query_string", or "json"'
            )
        for location in locations:
            if location not in ("headers", "cookies", "query_string", "json"):
                raise RuntimeError(
                    "FLASK_REDIS_TOKEN_LOCATION can only contain "
                    '"headers", "cookies", "query_string", or "json"'
                )
        return locations

    @property
    def token_in_cookies(self) -> bool:
        return "cookies" in self.token_location

    @property
    def token_in_headers(self) -> bool:
        return "headers" in self.token_location

    @property
    def token_in_query_string(self) -> bool:
        return "query_string" in self.token_location

    @property
    def token_in_json(self) -> bool:
        return "json" in self.token_location

    @property
    def header_name(self) -> str:
        name = current_app.config["FLASK_REDIS_TOKEN_HEADER_NAME"]
        if not name:
            raise RuntimeError("FLASK_REDIS_TOKEN_HEADER_NAME cannot be empty")
        return name

    @property
    def csrf_header_name(self) -> str:
        name = current_app.config["FLASK_REDIS_TOKEN_CSRF_HEADER_NAME"]
        if not name:
            raise RuntimeError("FLASK_REDIS_TOKEN_CSRF_HEADER_NAME cannot be empty")
        return name

    @property
    def token_field_name(self) -> str:
        return current_app.config["FLASK_REDIS_TOKEN_FIELD_NAME"]

    @property
    def token_cookie_name(self) -> str:
        return current_app.config["FLASK_REDIS_TOKEN_COOKIE_NAME"]

    @property
    def token_cookie_path(self) -> str:
        return current_app.config["FLASK_REDIS_TOKEN_COOKIE_PATH"]

    @property
    def csrf_cookie_name(self) -> str:
        return current_app.config["FLASK_REDIS_TOKEN_CSRF_COOKIE_NAME"]

    @property
    def csrf_cookie_path(self) -> str:
        return current_app.config["FLASK_REDIS_TOKEN_CSRF_COOKIE_PATH"]

    @property
    def session_cookie(self) -> bool:
        return current_app.config["FLASK_REDIS_TOKEN_SESSION_COOKIE"]

    @property
    def cookie_max_age(self) -> Optional[int]:
        return None if self.session_cookie else 2626560  # 1 month

    @property
    def cookie_secure(self) -> bool:
        return current_app.config["FLASK_REDIS_TOKEN_COOKIE_SECURE"]

    @property
    def cookie_samesite(self) -> str:
        return current_app.config["FLASK_REDIS_TOKEN_COOKIE_SAMESITE"]

    @property
    def csrf_protect(self) -> bool:
        return self.token_in_cookies and current_app.config["FLASK_REDIS_TOKEN_CSRF_PROTECT"]

    @property
    def csrf_in_cookies(self) -> bool:
        return current_app.config["FLASK_REDIS_TOKEN_CSRF_IN_COOKIES"]

    @property
    def super_admin_role(self) -> str:
        return current_app.config["FLASK_REDIS_TOKEN_SUPER_ADMIN_ROLE"]

    @property
    def csrf_methods(self) -> List[str]:
        return current_app.config["FLASK_REDIS_TOKEN_CSRF_METHODS"]

    @property
    def remember_me(self) -> str:
        return current_app.config["FLASK_REDIS_TOKEN_REMEMBER_ME"]

    @property
    def csrf_field_name(self) -> str:
        return current_app.config["FLASK_REDIS_TOKEN_CSRF_FIELD_NAME"]
