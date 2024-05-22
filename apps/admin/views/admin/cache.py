from flask import Blueprint, render_template, request

from pub.consts import RedisKey
from pub.utils.http_utils import table_api, success_api
from pub.utils.redis_utils import Redis
from pub.utils.rights import authorize
from pub.utils.validate import str_escape

admin_cache_bp = Blueprint('adminCache', __name__, url_prefix='/admin/cache')


def get_business_key(key: str):
    return RedisKey.BUSINESS_CACHE + ':' + key


# 缓存
@admin_cache_bp.get('/')
@authorize("admin:cache:main")
def main():
    return render_template('admin/cache/main.html')


# 缓存分页查询
@admin_cache_bp.get('/data')
@authorize("admin:cache:main")
def data():
    # 获取请求参数
    prefix = str_escape(request.args.get("prefix"))
    if not prefix:
        prefix = ''

    caches = Redis.caches(get_business_key(prefix) + '*')
    caches.sort(key=lambda i: (len(i['key']), i['key']))

    return table_api(data=caches, count=len(caches))


# 缓存增加
@admin_cache_bp.get('/add')
@authorize("admin:cache:add", log=True)
def add():
    return render_template('admin/cache/add.html')


# 保存缓存
@admin_cache_bp.post('/save')
@authorize("admin:cache:add", log=True)
def save():
    req_json = request.get_json(force=True)
    key = str_escape(req_json.get("key"))
    value = str_escape(req_json.get('value'))
    expire = int(str_escape(req_json.get('expire')))

    Redis.set_and_expire(get_business_key(key), value, expire)

    return success_api(msg="增加成功")


# 修改缓存
@admin_cache_bp.get('/edit')
@authorize("admin:cache:edit", log=True)
def edit():
    key = request.args.get("key")
    value = Redis.get(key)
    expire = Redis.get_expire(key)
    if not value:
        value = ''
        expire = None
    res = dict(key=key, value=value, expire=expire)
    return render_template('admin/cache/edit.html', data=res)


@admin_cache_bp.put('/update')
@authorize("admin:cache:edit", log=True)
def update():
    req_json = request.get_json(force=True)
    key = str_escape(req_json.get("key"))
    value = str_escape(req_json.get('value'))
    expire = int(str_escape(req_json.get('expire')))

    # 是否已过期
    expired = str_escape(req_json.get('expired'))
    if not expire or '0' == expire:
        key = get_business_key(key)

    Redis.set_and_expire(key, value, expire)

    return success_api(msg="更新成功")


@admin_cache_bp.delete('/remove')
@authorize("admin:cache:remove", log=True)
def delete():
    names = request.form.getlist('names[]')
    Redis.delete(names)

    return success_api(msg="删除成功")
