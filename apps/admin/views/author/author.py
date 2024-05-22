from flask import Blueprint, render_template, request

from pub.consts.dict_consts import DictConsts
from pub.curd import enable_status, disable_status
from pub.helper import ModelFilter
from pub.models.models_business import Author
from pub.models.models_system import DictType
from pub.utils.http_utils import table_api, fail_api, success_api
from pub.utils.rights import authorize
from pub.utils.validate import str_escape

admin_author_bp = Blueprint('admin_author', __name__, url_prefix='/admin/author')


@admin_author_bp.get('/')
@authorize("admin:author:main")
def main():
    return render_template('author/main.html')


@admin_author_bp.get('/data')
@authorize("admin:author:main")
def data():
    # 获取请求参数
    pen_name = str_escape(request.args.get("pen_name"))

    # 查询参数构造
    mf = ModelFilter()
    if pen_name:
        mf.contains(field_name="pen_name", value=pen_name)

    page_data = Author.query.filter(
        mf.get_filter(Author)
    ).order_by(
        Author.create_time.desc()
    ).layui_paginate()
    count = page_data.total

    res = [
        {
            'id': str(author.id),
            'invite_code': author.invite_code,
            'pen_name': author.pen_name,
            'tel_phone': author.tel_phone,
            'chat_account': author.chat_account,
            'email': author.email,
            'work_direction': author.work_direction,
            'work_direction_name': DictType.translate(DictConsts.work_direction, author.work_direction),
            'create_time': author.create_time,
            'status': author.status,
            'status_name': DictType.translate(DictConsts.author_status, author.status),
            'create_time_name': author.create_time.strftime("%Y-%m-%d %H:%M:%S") if author.create_time else ''
        } for author in page_data.items
    ]
    # 返回api
    return table_api(data=res, count=count)


@admin_author_bp.put('/enable')
@authorize("admin:author:enable_disable", log=True)
def enable():
    id_ = request.get_json(force=True).get('id')
    if id_:
        res = enable_status(model=Author, id=id_, field="status", enable=0)
        if not res:
            return fail_api(msg="出错啦")
        return success_api(msg="启动成功")
    return fail_api(msg="数据错误")


# 禁用
@admin_author_bp.put('/disable')
@authorize("admin:author:enable_disable", log=True)
def dis_enable():
    id_ = request.get_json(force=True).get('id')
    if id_:
        res = disable_status(model=Author, id=id_, field="status", disable=1)
        if not res:
            return fail_api(msg="出错啦")
        return success_api(msg="禁用成功")
    return fail_api(msg="数据错误")
