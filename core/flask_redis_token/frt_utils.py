import datetime
import time
import uuid
from functools import wraps
from typing import Union, List

import jsonpickle
import redis
from flask import Response, request, current_app, abort, redirect, url_for

from core.flask_redis_token import Config
from pub.exts.init_cache import redis_client
from pub.utils.http_utils import is_ajax_request
from pub.utils.validate import str_escape


class RestTokenException(RuntimeError):
    def __init__(self, code: int, message: str = ''):
        self.code = code
        self.message = message


class RestNotLoginException(RestTokenException):
    pass


class RestExistsFrozenSessionException(RestTokenException):
    pass


class RestNotPermissionException(RestTokenException):
    pass


class RestCsrfException(RestTokenException):
    pass


def login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        login_id = FRTUtils.check_login()
        if not login_id:
            if is_ajax_request():
                raise RestNotLoginException(401, '请登录以访问此页面')
            else:
                login_view = FRTUtils.get_login_view()
                if not login_view:
                    abort(401)
                else:
                    return redirect(url_for(login_view, next_url=request.url))

        # flask 1.x compatibility
        # current_app.ensure_sync is only available in Flask >= 2.0
        if callable(getattr(current_app, "ensure_sync", None)):
            resp = current_app.ensure_sync(func)(*args, **kwargs)
        else:
            resp = func(*args, **kwargs)

        # 刷新csrf_token
        if isinstance(resp, Response):
            FRTUtils.refresh_csrf_token(login_id, resp)
        return resp

    return decorated_view


def permission_required(permission: str):
    def decorator(func):
        @login_required
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not FRTUtils.has_permission(permission):
                if is_ajax_request():
                    raise RestNotPermissionException(403, '权限不足!')
                else:
                    abort(403)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def with_redis_lock(timeout: int = 5, blocking: bool = True, sleep: float = 0.1, blocking_timeout: int = 10):
    """
    此装饰器主要用于先读取，再修改，后写入的操作：
    session = get_session()
    data = session.get(foo)
    data.operate(*args, **kwargs)
    set_session(foo, data)
    例如：
    1.当系统允许多处登录时，登录时会把登录设备信息、每个设备的token信息存入到一个列表中，其结构大概是这样的：
    "login_devices": [
        {"device": "Firefox", "token": "001"},
        {"device": "chrome", "token": "002"},
        {"device": "edge", "token": "003"},
        {"device": "safari", "token": "004"},
        {"device": "Android", "token": "005"}
    ]
    多端登录，会并发修改该列表，如果不加redis锁，会导致后面的操作覆盖前面的操作，从而导致列表中只保留了最后一个设备信息
    2.动态添加、修改、删除权限、角色时，如果不加锁，会使之前的写操作被覆盖掉
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = FRTUtils.get_token()
            if not token:
                return func(*args, **kwargs)

            with redis_client.lock(f'flask_redis_token_{token}', timeout=timeout, blocking=blocking,
                                   sleep=sleep, blocking_timeout=blocking_timeout):
                return func(*args, **kwargs)

        return wrapper

    return decorator


class FRTUtils:
    _config = Config()
    _redis_client = None
    _REDIS_PREFIX = 'FlaskRedisToken'
    _USER_SESSION_KEY = 'USER_SESSION'

    @classmethod
    @with_redis_lock()
    def check_login(cls):
        # 登录校验
        ret = cls.is_login()
        if not ret:
            return None

        session, login_id = ret
        cls.last_and_active(login_id, session)

        return login_id

    @classmethod
    def is_login(cls):
        token = cls.get_token()
        login_id = cls.get_login_id_by_token(token)
        if not token:
            return None

        session = cls.get_session(token=token)
        if not session:
            return None

        if not cls.get_current_user():
            return None

        if not cls.get_session().get('is_authenticated'):
            if is_ajax_request():
                raise RestNotPermissionException(403, f'会话已被冻结，无权访问！')
            else:
                abort(403)

        cls.check_csrf_token(session)

        return session, login_id

    @classmethod
    def check_csrf_token(cls, session: dict):
        if cls._config.csrf_protect and request.method in cls._config.csrf_methods:
            csrf_token = cls.get_csrf_token()
            if not csrf_token:
                raise RestCsrfException(401, f'请求头中缺少CSRF保护令牌（{cls._config.csrf_header_name}）')
            if not session.get(cls._config.csrf_field_name):
                raise RestCsrfException(401, f'CSRF保护令牌"{csrf_token}"不存在或已过期，请重新登录以获取新的令牌')
            if session.get(cls._config.csrf_field_name) != csrf_token:
                raise RestCsrfException(401, f'CSRF保护令牌错误')

    @classmethod
    def refresh_csrf_token(cls, login_id, response: Response):
        if cls._config.csrf_protect:
            new_csrf_token = uuid.uuid4().hex
            session = cls.get_session()
            if not session:
                return
            cls.set_session('CSRF_TOKEN', new_csrf_token, session, login_id)
            response.headers[cls._config.csrf_field_name] = new_csrf_token

    @classmethod
    def last_and_active(cls, login_id: Union[int, str], session: dict = None):
        session = cls.get_session(login_id=login_id) if not session else session
        cls.active(session, login_id)
        # 自动续期
        cls.auto_last(session, login_id)

    @classmethod
    def auto_last(cls, session: dict, login_id):
        if cls._config.redis_ex is None or session.get('remember_me'):
            return
        cls.__get_redis_client().expire(f'{cls._REDIS_PREFIX}:token:{session.get("token")}',
                                        cls._config.redis_ex.seconds)
        cls.__get_redis_client().expire(f'{cls._REDIS_PREFIX}:session:{login_id}', cls._config.redis_ex.seconds)

    @classmethod
    def active(cls, session: dict, login_id):
        """
        这里不能调用set_session
        因为set_session加了redis锁
        而该函数被last_and_active调用，last_and_active又被check_login调用
        check_login也加了redis锁，会导致请求很慢
        """
        session['last_activity'] = datetime.datetime.now()
        cls.write_session(session, login_id)

        cls.__get_redis_client().zrem(f'{cls._REDIS_PREFIX}:loginid_set', login_id)
        cls.__get_redis_client().zadd(f'{cls._REDIS_PREFIX}:loginid_set', {login_id: time.time()})

    @classmethod
    def get_session_list(cls, keyword: str = None, start: int = 0, end: int = -1) -> List[dict]:
        ret = []

        if not keyword:
            session_list = cls.__get_redis_client().zrange(f'{cls._REDIS_PREFIX}:loginid_set', start, end)
            for login_id in session_list:
                decoded_login_id = login_id.decode('utf-8')
                session = cls.get_session(decoded_login_id)
                if session:  # 会存在loginid_set和实际会话数据不同步问题
                    ret.append(session)
                else:  # loginid_set中的元素如果找不到对应的会话信息，则将其移除
                    cls.__get_redis_client().zrem(f'{cls._REDIS_PREFIX}:loginid_set', decoded_login_id)
        else:
            keys = cls.__get_redis_client().keys(f'{cls._REDIS_PREFIX}:session:*{keyword}*')
            keys = keys[start:end + 1] if end >= 0 else keys[start:]
            for k in keys:
                decoded_login_id = k.decode('utf-8').split(':')[-1]
                session = cls.get_session(decoded_login_id)
                if session:  # 会存在loginid_set和实际会话数据不同步问题
                    ret.append(session)
                else:  # loginid_set中的元素如果找不到对应的会话信息，则将其移除
                    cls.__get_redis_client().zrem(f'{cls._REDIS_PREFIX}:loginid_set', decoded_login_id)

        return ret

    @classmethod
    def has_permission(cls, permission: str):
        return permission in cls.get_permission_list()

    @classmethod
    def get_login_view(cls):
        return cls._config.login_view

    @classmethod
    def __get_redis_client(cls):
        if not cls._redis_client:
            cls._redis_client = redis.StrictRedis(host=cls._config.redis_host, port=cls._config.redis_port,
                                                  db=cls._config.redis_db)
        return cls._redis_client

    @classmethod
    def __get_redis_key(cls, key: str, default=''):
        value = cls.__get_redis_client().get(key)
        if value:
            return value.decode('utf-8')
        else:
            return default

    @classmethod
    def __clear_old_token(cls, login_id: Union[int, str]):
        """
        用于清理以前残留的token
        当用户登录时选择记住我，而后又将浏览器cookie或localStorage里的token删除掉，那就相当于没登录，
        后期再登录的时候，login id由于相同，会覆盖原来的，但token是随机生成的，因而需要先清空
        """
        session = cls.get_session(login_id)
        # 判断是否存在被冻结的session，存在则无法清空，且不能继续进行登录操作
        if cls.has_frozen_session(login_id, session):
            raise RestExistsFrozenSessionException(code=401, message='当前账号存在被冻结的会话，请先联系管理员解冻！')
        if session and session.get('token'):
            cls.__get_redis_client().delete(f'{cls._REDIS_PREFIX}:token:{session.get("token")}')

    @classmethod
    def has_frozen_session(cls, login_id: Union[int, str], session: dict = None) -> bool:
        session = cls.get_session(login_id) if not session else session
        if not session or session.get('is_authenticated'):
            return False
        return True

    @classmethod
    @with_redis_lock()
    def login(cls, login_id: Union[int, str], remember_me: bool = False):
        if not isinstance(login_id, (int, str)):
            raise TypeError('login_id只能是int或str')

        cls.__clear_old_token(login_id)

        token = uuid.uuid4().hex
        if cls._config.redis_ex is None or remember_me:
            cls.__get_redis_client().set(f'{cls._REDIS_PREFIX}:token:{token}', login_id)
        else:
            cls.__get_redis_client().set(f'{cls._REDIS_PREFIX}:token:{token}', login_id,
                                         ex=cls._config.redis_ex.seconds)
        session = dict(
            token=token,
            is_authenticated=True,
            remember_me=remember_me,
            last_activity=datetime.datetime.now()
        )
        csrf_token = None
        if cls._config.csrf_protect:
            csrf_token = uuid.uuid4().hex
            session['CSRF_TOKEN'] = csrf_token
        if cls._config.redis_ex is None or remember_me:
            cls.__get_redis_client().set(f'{cls._REDIS_PREFIX}:session:{login_id}', jsonpickle.encode(session))
        else:
            cls.__get_redis_client().set(f'{cls._REDIS_PREFIX}:session:{login_id}',
                                         jsonpickle.encode(session), ex=cls._config.redis_ex.seconds)

        cls.__get_redis_client().zadd(f'{cls._REDIS_PREFIX}:loginid_set', {login_id: time.time()})

        return token, csrf_token if csrf_token else token

    @classmethod
    def login_user(cls, login_id: int, user: dict, remember_me=False):
        tokens = cls.login(login_id, remember_me=remember_me)
        cls.set_session_user(user, login_id)

        return tokens

    @classmethod
    def logout(cls, response: Response = None):
        token = cls.get_token()
        login_id = cls.get_login_id_by_token(token)
        cls.__remove_token_and_session(token, login_id)

        if response:
            response.delete_cookie(cls._config.token_cookie_name)

    @classmethod
    def __remove_token_and_session(cls, token: str, login_id: Union[int, str]):
        cls.__get_redis_client().delete(f'{cls._REDIS_PREFIX}:session:{login_id}')
        cls.__get_redis_client().delete(f'{cls._REDIS_PREFIX}:token:{token}')

        cls.__get_redis_client().zrem(f'{cls._REDIS_PREFIX}:loginid_set', login_id)

    @classmethod
    def freeze_session(cls, login_id: Union[int, str]):
        cls.set_session('is_authenticated', False, session=None, login_id=login_id)

    @classmethod
    def unfreeze_session(cls, login_id: Union[int, str]):
        cls.set_session('is_authenticated', True, session=None, login_id=login_id)

    @classmethod
    def kickout(cls, login_id):
        token = cls.get_token_by_login_id(login_id)
        cls.__remove_token_and_session(token, login_id)

    @classmethod
    def get_token(cls):
        token = None
        if cls._config.token_in_cookies:
            token = request.cookies.get(cls._config.token_cookie_name)
        if token is None and cls._config.token_in_query_string and request.args:
            token = request.args.get(cls._config.token_field_name)
        if token is None and cls._config.token_in_json and request.headers.get('Content-Type') == 'application/json':
            req_json = request.get_json(force=True)
            token = req_json.get(cls._config.token_field_name) if req_json else None
        if token is None and cls._config.token_in_headers:
            token = request.headers.get(cls._config.header_name)

        return str_escape(token)

    @classmethod
    def get_csrf_token(cls):
        return request.headers.get(cls._config.csrf_header_name)

    @classmethod
    def __get_login_id(cls, login_id=None, token: str = None):
        if login_id is None:
            login_id = cls.__get_redis_key(f'{cls._REDIS_PREFIX}:token:{token if token else cls.get_token()}')
        return login_id

    @classmethod
    def get_login_id_by_token(cls, token: str):
        return cls.__get_redis_key(f'{cls._REDIS_PREFIX}:token:{token}')

    @classmethod
    def get_token_by_login_id(cls, login_id: Union[int, str]):
        return cls.get_session(login_id).get('token')

    @classmethod
    def get_session(cls, login_id=None, token: str = None) -> dict:
        session = cls.__get_redis_key(f'{cls._REDIS_PREFIX}:session:{cls.__get_login_id(login_id, token)}')
        if not session:
            return {}
        return jsonpickle.decode(session)

    @classmethod
    def get_permission_list(cls, login_id=None, token: str = None) -> list:
        return cls.get_session(login_id, token).get('permission_codes')

    @classmethod
    def get_current_user(cls):
        return cls.get_session().get(cls._USER_SESSION_KEY)

    @classmethod
    def set_session_user(cls, user, login_id=None):
        cls.set_session(cls._USER_SESSION_KEY, user, login_id=login_id)

    @classmethod
    @with_redis_lock()
    def set_session(cls, key: str, value, session: dict = None, login_id=None):
        session = cls.get_session(login_id) if not session else session
        session[key] = value
        cls.write_session(session, login_id)

    @classmethod
    def write_session(cls, session: dict, login_id: Union[int, str]):
        if cls._config.redis_ex is None or session.get('remember_me'):
            cls.__get_redis_client().set(f'{cls._REDIS_PREFIX}:session:{cls.__get_login_id(login_id)}',
                                         jsonpickle.encode(session))
        else:
            cls.__get_redis_client().set(f'{cls._REDIS_PREFIX}:session:{cls.__get_login_id(login_id)}',
                                         jsonpickle.encode(session), ex=cls._config.redis_ex.seconds)

    @classmethod
    def set_permission_list(cls, permission_list: List[str], login_id=None):
        cls.set_session('permission_codes', permission_list, login_id=login_id)

    @classmethod
    def gen_token_cookie(cls, response: Response, token: str, csrf_token: str = None, max_age: int = None,
                         domain: str = None):
        response.set_cookie(
            cls._config.token_cookie_name,
            value=token,
            max_age=max_age or cls._config.cookie_max_age,
            secure=cls._config.cookie_secure,
            httponly=True,
            domain=domain or cls._config.cookie_domain,
            path=cls._config.token_cookie_path,
            samesite=cls._config.cookie_samesite,
        )

        if cls._config.csrf_protect:
            if not csrf_token:
                raise RuntimeError('csrf_token不能为空')
            response.headers[cls._config.csrf_field_name] = csrf_token
