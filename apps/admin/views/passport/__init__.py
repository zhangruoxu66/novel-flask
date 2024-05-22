from flask import Blueprint, redirect, url_for, render_template, request, jsonify

from apps.admin.common.admin_log import login_log
from core.flask_redis_token import Config
from core.flask_redis_token.frt_utils import FRTUtils, login_required
from pub.consts import RedisKey
from pub.models.models_system import User
from pub.utils import ip_utils
from pub.utils.gen_captcha import gen_captcha
from pub.utils.http_utils import fail_api, success_api
from pub.utils.redis_utils import Redis

passport_bp = Blueprint('passport', __name__, url_prefix='/passport')


def register_passport_views(app):
    app.register_blueprint(passport_bp)


# 获取验证码
@passport_bp.get('/getCaptcha')
def get_captcha():
    resp, code = gen_captcha()
    Redis.set_and_expire(RedisKey.VALIDATE_CODE_CACHE + ':' + ip_utils.get_real_ip(), code, 60 * 5)
    return resp


# 登录
@passport_bp.get('/login')
def login():
    if FRTUtils.is_login():
        return redirect(url_for('admin.index'))
    return render_template('admin/login.html')


# 登录
@passport_bp.post('/login')
def login_post():
    req = request.form
    username = req.get('username')
    password = req.get('password')
    remember_me = req.get('remember-me') == 'on'
    code = req.get('captcha').__str__().lower()

    if not username or not password or not code:
        return fail_api(msg="用户名或密码没有输入")
    s_code = Redis.get(RedisKey.VALIDATE_CODE_CACHE + ':' + ip_utils.get_real_ip())
    Redis.delete(RedisKey.VALIDATE_CODE_CACHE + ':' + ip_utils.get_real_ip())

    if not all([code, s_code]):
        return fail_api(msg="参数错误")

    if code != s_code:
        return fail_api(msg="验证码错误")
    user = User.query.filter_by(username=username).first()

    if not user:
        return fail_api(msg="不存在的用户")

    if user.enable == 0:
        return fail_api(msg="用户被暂停使用")

    if username == user.username and user.validate_password(password):
        roles = user.role.all()
        permissions = []
        permission_codes = []
        for role in roles:
            if role.enable == 0:
                continue
            for p in role.power:
                if p.enable == 0:
                    continue
                permissions.append(p)
                permission_codes.append(p.code)

        # 登录
        cfg = Config()
        tokens = FRTUtils.login_user(user.username, user, remember_me)
        token = tokens[0] if cfg.csrf_protect else tokens
        csrf_token = tokens[1] if cfg.csrf_protect else None
        response = jsonify(success=True, msg="登录成功", code=0, data=dict(token=token, csrf_token=csrf_token, uid=user.id))
        FRTUtils.gen_token_cookie(response, token, csrf_token)

        # 权限存入session
        FRTUtils.set_session('permissions', permissions, login_id=user.username)
        FRTUtils.set_permission_list(permission_codes, login_id=user.username)

        # 记录登录日志
        login_log(request, uid=user.id, is_access=True)

        return response

    login_log(request, uid=user.id, is_access=False)
    return fail_api(msg="用户名或密码错误")


# 退出登录
@passport_bp.post('/logout')
@login_required
def logout():
    response = success_api(msg="注销成功")
    FRTUtils.logout(response)
    return response
