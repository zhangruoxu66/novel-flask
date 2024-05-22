from flask import Blueprint, render_template, request, current_app

from apps.admin.exts.init_websocket import kickout_notice, freeze_notice
from core.flask_redis_token.frt_utils import FRTUtils
from pub.models.models_system import User
from pub.utils.http_utils import table_api, success_api, fail_api
from pub.utils.rights import authorize
from pub.utils.validate import str_escape

admin_session_bp = Blueprint('admin_session', __name__, url_prefix='/admin/session')


@admin_session_bp.get('/')
@authorize("admin:session:main")
def main():
    return render_template('admin/session/main.html')


@admin_session_bp.get('/data')
@authorize("admin:session:main")
def data():
    # 获取请求参数
    username = str_escape(request.args.get("username"))
    page = request.args.get("page", type=int)
    limit = request.args.get("limit", type=int)
    if not username:
        username = ''

    start = (page - 1) * limit
    end = start + limit - 1
    page_data = FRTUtils.get_session_list(username, start, end)

    res = [
        {
            'username': session.get('USER_SESSION').username,
            'token': session.get('token'),
            'status': session.get('is_authenticated'),
            'last_activity': session.get('last_activity').strftime("%Y-%m-%d %H:%M:%S")
        } for session in page_data
    ]

    return table_api(data=res, count=len(page_data))


@admin_session_bp.put('/unfreeze')
@authorize("admin:session:unfreeze", log=True)
def unfreeze():
    usernames = request.form.getlist('usernames[]')

    for username in usernames:
        if username == current_app.config.get("SUPERADMIN"):
            return fail_api(msg=f"不能操作超级管理员【{username}】的会话")
        if FRTUtils.get_current_user().username == username:
            return fail_api(msg="不能操作自己的会话")

        FRTUtils.unfreeze_session(username)

    return success_api(msg="解冻成功")


# 禁用
@admin_session_bp.put('/freeze')
@authorize("admin:session:edit", log=True)
def freeze():
    usernames = request.form.getlist('usernames[]')

    for username in usernames:
        if username == current_app.config.get("SUPERADMIN"):
            return fail_api(msg=f"不能操作超级管理员【{username}】的会话")
        if FRTUtils.get_current_user().username == username:
            return fail_api(msg="不能操作自己的会话")

        FRTUtils.freeze_session(username)

        freeze_notice(User.query.filter_by(username=username).first().id)

    return success_api(msg="冻结成功")


# 踢下线
@admin_session_bp.put('/kickout')
@authorize("admin:session:kickout", log=True)
def kickout():
    usernames = request.form.getlist('usernames[]')

    for username in usernames:
        if username == current_app.config.get("SUPERADMIN"):
            return fail_api(msg=f"不能操作超级管理员【{username}】的会话")
        if FRTUtils.get_current_user().username == username:
            return fail_api(msg="不能操作自己的会话")

        FRTUtils.kickout(username)

        kickout_notice(User.query.filter_by(username=username).first().id)

    return success_api(msg="剔除成功")
