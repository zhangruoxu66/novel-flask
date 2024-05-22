from flask import Flask

from apps.admin.views.website.friend_link import admin_friend_link_bp
from apps.admin.views.website.website_info import admin_website_info_bp


def register_website_views(app: Flask):
    app.register_blueprint(admin_website_info_bp)
    app.register_blueprint(admin_friend_link_bp)
