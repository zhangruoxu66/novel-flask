from flask import Blueprint, render_template, request

from core.flask_redis_token.frt_utils import FRTUtils
from pub.consts import RedisKey
from pub.consts.dict_consts import DictConsts
from pub.curd import enable_status, disable_status
from pub.exts.init_sqlalchemy import db
from pub.models.models_business import FriendLink
from pub.models.models_system import DictType
from pub.utils.http_utils import table_api, success_api, fail_api
from pub.utils.redis_utils import Redis
from pub.utils.rights import authorize
from pub.utils.validate import str_escape

admin_friend_link_bp = Blueprint('admin_friend_link', __name__, url_prefix='/admin/friend_link')


@admin_friend_link_bp.get('/')
@authorize("admin:friend_link:main")
def main():
    return render_template('friend_link/main.html')


@admin_friend_link_bp.get('/data')
@authorize("admin:friend_link:main")
def data():
    page_data = FriendLink.query.order_by(FriendLink.id.desc()).layui_paginate()
    count = page_data.total
    res = [
        {
            'id': link.id,
            'link_name': link.link_name,
            'link_url': link.link_url,
            'sort': link.sort,
            'is_open': link.is_open,
            'is_open_name': DictType.translate(DictConsts.is_enable, link.is_open)
        } for link in page_data.items
    ]
    return table_api(data=res, count=count)


@admin_friend_link_bp.get('/add')
@authorize("admin:friend_link:add", log=True)
def add():
    return render_template('friend_link/add.html')


@admin_friend_link_bp.post('/save')
@authorize("admin:friend_link:add", log=True)
def save():
    req_json = request.get_json(force=True)
    link_name = str_escape(req_json.get('link_name'))
    link_url = str_escape(req_json.get('link_url'))
    sort = str_escape(req_json.get('sort'))
    is_open = str_escape(req_json.get('is_open'))

    fl = FriendLink(link_name=link_name, link_url=link_url, sort=sort, is_open=is_open,
                    create_user_id=FRTUtils.get_current_user().id, update_user_id=FRTUtils.get_current_user().id)
    db.session.add(fl)
    db.session.commit()

    Redis.delete(RedisKey.INDEX_LINK_KEY)

    return success_api()


@admin_friend_link_bp.get('/edit')
@authorize("admin:friend_link:edit", log=True)
def edit():
    id_ = request.args.get("id")
    obj = FriendLink.query.get(id_)
    return render_template('friend_link/edit.html', data=obj)


@admin_friend_link_bp.put('/update')
@authorize("admin:friend_link:edit", log=True)
def update():
    req_json = request.get_json(force=True)
    id_ = str_escape(req_json.get('id'))
    link_name = str_escape(req_json.get('link_name'))
    link_url = str_escape(req_json.get('link_url'))
    sort = str_escape(req_json.get('sort'))
    is_open = str_escape(req_json.get('is_open'))

    FriendLink.query.filter_by(id=id_).update(
        {'link_name': link_name, 'link_url': link_url, 'sort': sort, 'is_open': is_open})
    db.session.commit()

    return success_api(msg="更新成功")


@admin_friend_link_bp.delete('/remove')
@authorize("admin:friend_link:remove", log=True)
def delete():
    ids = request.form.getlist('ids[]')
    for id_ in ids:
        res = FriendLink.query.filter_by(id=id_).delete()
        if not res:
            return fail_api(msg="删除失败")
    db.session.commit()
    return success_api(msg="删除成功")


# 启用
@admin_friend_link_bp.put('/enable')
@authorize("admin:friend_link:edit", log=True)
def enable():
    id_ = request.get_json(force=True).get('id')
    if id_:
        res = enable_status(model=FriendLink, id=id_, field="is_open")
        if not res:
            return fail_api(msg="出错啦")
        return success_api(msg="启动成功")
    return fail_api(msg="数据错误")


# 禁用
@admin_friend_link_bp.put('/disable')
@authorize("admin:friend_link:edit", log=True)
def dis_enable():
    id_ = request.get_json(force=True).get('id')
    if id_:
        res = disable_status(model=FriendLink, id=id_, field="is_open")
        if not res:
            return fail_api(msg="出错啦")
        return success_api(msg="禁用成功")
    return fail_api(msg="数据错误")
