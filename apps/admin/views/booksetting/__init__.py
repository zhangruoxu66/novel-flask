from flask import Flask

from apps.admin.views.booksetting.book_setting import admin_book_setting_bp


def register_book_setting_views(app: Flask):
    app.register_blueprint(admin_book_setting_bp)
