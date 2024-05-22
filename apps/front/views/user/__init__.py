from . import user
from .user import user_bp


def register_user_views(app):
    """
    初始化蓝图

    """

    app.register_blueprint(user_bp)
