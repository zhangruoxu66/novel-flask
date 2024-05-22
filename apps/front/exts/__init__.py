from flask import Flask

from apps.front.exts.init_error_views import init_error_views
from apps.front.exts.init_jwt import init_jwt
from pub.exts.init_siwadoc import init_siwadoc
from pub.exts.init_sqlalchemy import init_databases
from pub.exts.init_upload import init_upload


def init_plugs(app: Flask) -> None:
    init_databases(app)
    init_upload(app)
    init_jwt(app)
    init_error_views(app)
    init_siwadoc(app)
