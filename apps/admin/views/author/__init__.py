from flask import Flask

from apps.admin.views.author.author import admin_author_bp
from apps.admin.views.author.invite_code import admin_invite_code_bp


def register_author_views(app: Flask):
    app.register_blueprint(admin_author_bp)
    app.register_blueprint(admin_invite_code_bp)
