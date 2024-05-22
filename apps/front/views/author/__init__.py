from . import author
from .author import author_bp


def register_author_views(app):
    """
    初始化蓝图

    """

    app.register_blueprint(author_bp)
