from flask import Blueprint

from pub.consts import RedisKey
from pub.utils import ip_utils
from pub.utils.gen_captcha import gen_captcha
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
