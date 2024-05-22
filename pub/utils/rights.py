from functools import wraps

from flask import abort, request, current_app

from apps.admin.common.admin_log import admin_log
from core.flask_redis_token.frt_utils import FRTUtils, login_required, RestNotPermissionException
from pub.utils.http_utils import is_ajax_request


def authorize(permission: str, log: bool = False):
    """用户权限判断，用于判断目前会话用户是否拥有访问权限

    :param permission: 权限标识
    :type permission: str
    :param log: 是否记录日志, defaults to False
    :type log: bool, optional
    """

    def decorator(func):
        @login_required
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 定义管理员的id为1
            # if FRTUtils.get_current_user().get('username') == current_app.config.get("SUPERADMIN"):
            if FRTUtils.get_current_user().username == current_app.config.get("SUPERADMIN"):
                return func(*args, **kwargs)
            if not FRTUtils.has_permission(permission):
                if log:
                    admin_log(request=request, is_access=False)
                if is_ajax_request():
                    raise RestNotPermissionException(403, '权限不足!')
                else:
                    abort(403)
            if log:
                admin_log(request=request, is_access=True)
            return func(*args, **kwargs)

        return wrapper

    return decorator
