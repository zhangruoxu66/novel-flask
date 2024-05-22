from flask import Flask

from apps.admin.exts.init_flask_redis_token import init_flask_redis_token
from apps.admin.exts.init_websocket import init_socketio
from pub.exts.init_apscheduler import init_scheduler
from apps.admin.exts.init_error_views import init_error_views
from apps.admin.exts.init_template_directives import init_template_directives
from pub.exts.init_cache_data import load_cache
from pub.exts.init_mail import init_mail
from pub.exts.init_migrate import init_migrate
from pub.exts.init_siwadoc import init_siwadoc
from pub.exts.init_sqlalchemy import init_databases
from pub.exts.init_upload import init_upload


def init_plugs(app: Flask) -> None:
    init_databases(app)
    init_template_directives(app)
    init_error_views(app)
    init_mail(app)
    init_scheduler(app)
    init_upload(app)
    init_migrate(app)
    load_cache(app)
    init_flask_redis_token(app)
    init_siwadoc(app)
    init_socketio(app)
