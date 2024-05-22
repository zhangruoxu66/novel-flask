from . import book
from .book import book_bp


def register_book_views(app):
    """
    初始化蓝图

    """

    app.register_blueprint(book_bp)
