from flask import Flask

from apps.admin.views.admin.admin_log import admin_log
from apps.admin.views.admin.cache import admin_cache_bp
from apps.admin.views.admin.dict import admin_dict
from apps.admin.views.admin.file import admin_file
from apps.admin.views.admin.index import admin_bp
from apps.admin.views.admin.mail import admin_mail
from apps.admin.views.admin.monitor import admin_monitor_bp
from apps.admin.views.admin.power import admin_power
from apps.admin.views.admin.role import admin_role
from apps.admin.views.admin.session_manage import admin_session_bp
from apps.admin.views.admin.task import admin_task
from apps.admin.views.admin.user import admin_user


def register_admin_views(app: Flask):
    app.register_blueprint(admin_bp)
    app.register_blueprint(admin_user)
    app.register_blueprint(admin_file)
    app.register_blueprint(admin_monitor_bp)
    app.register_blueprint(admin_log)
    app.register_blueprint(admin_power)
    app.register_blueprint(admin_role)
    app.register_blueprint(admin_dict)
    app.register_blueprint(admin_task)
    app.register_blueprint(admin_mail)
    app.register_blueprint(admin_cache_bp)
    app.register_blueprint(admin_session_bp)
