from . import index
from .index import index_bp


def register_index_views(app):
    """
    初始化蓝图

    """

    app.register_blueprint(index_bp)
