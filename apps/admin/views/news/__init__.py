from flask import Flask

from apps.admin.views.news.news import admin_news_bp
from apps.admin.views.news.news_category import admin_news_category_bp


def register_news_views(app: Flask):
    app.register_blueprint(admin_news_category_bp)
    app.register_blueprint(admin_news_bp)
