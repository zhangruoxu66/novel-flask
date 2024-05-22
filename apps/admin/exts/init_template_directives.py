from flask import current_app

from core.flask_redis_token.frt_utils import FRTUtils


def init_template_directives(app):
    @app.template_global()
    def authorize(permission):
        if FRTUtils.get_current_user().username != current_app.config.get("SUPERADMIN"):
            return FRTUtils.has_permission(permission)
        else:
            return True
