from flask import Flask

from apps.admin.views.book.book import admin_book_bp
from apps.admin.views.book.book_category import admin_book_category_bp
from apps.admin.views.book.book_comment import admin_book_comment_bp


def register_book_views(app: Flask):
    app.register_blueprint(admin_book_bp)
    app.register_blueprint(admin_book_category_bp)
    app.register_blueprint(admin_book_comment_bp)
