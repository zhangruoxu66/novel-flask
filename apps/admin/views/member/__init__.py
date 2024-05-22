from apps.admin.views.member.member import member_bp
from apps.admin.views.member.member_feedback import member_feedback_bp


def register_member_views(app):
    """
    初始化蓝图

    """

    app.register_blueprint(member_bp)
    app.register_blueprint(member_feedback_bp)
