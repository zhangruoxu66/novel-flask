from datetime import datetime

import parsedatetime
from flask import Blueprint, render_template, request

from core.flask_redis_token.frt_utils import FRTUtils
from pub.curd import AutoModelTransfer
from pub.exts.init_sqlalchemy import db
from pub.models.models_business import AuthorCode
from pub.utils.http_utils import table_api, success_api, fail_api
from pub.utils.rights import authorize
from pub.utils.validate import str_escape

admin_invite_code_bp = Blueprint('admin_invite_code', __name__, url_prefix='/admin/invite_code')


@admin_invite_code_bp.get('/')
@authorize("admin:invite_code:main")
def main():
    return render_template('invite_code/main.html')


@admin_invite_code_bp.get('/data')
@authorize("admin:invite_code:main")
def data():
    # 获取请求参数
    invite_code = str_escape(request.args.get("invite_code"))
    filters = []
    if invite_code is not None:
        filters.append(AuthorCode.invite_code == invite_code)

    # orm查询
    page_data = db.session.query(
        AuthorCode
    ).filter(*filters).order_by(AuthorCode.id.desc()).layui_paginate()
    count = page_data.total
    # 返回api
    return table_api(data=AutoModelTransfer.model_2_dict(page_data.items, AuthorCode), count=count)


@admin_invite_code_bp.get('/add')
@authorize("admin:invite_code:add", log=True)
def add():
    return render_template('invite_code/add.html')


@admin_invite_code_bp.post('/save')
@authorize("admin:invite_code:add", log=True)
def save():
    req_json = request.get_json(force=True)
    invite_code = str_escape(req_json.get('invite_code'))
    validity_time = req_json.get('validity_time')

    is_exists = AuthorCode.query.filter_by(invite_code=invite_code).count()
    if is_exists > 0:
        return fail_api(msg='邀请码已存在')

    calendar = parsedatetime.Calendar()
    time_structure_start_time, parse_status_start_time = calendar.parse(validity_time)
    validity_time = datetime(*time_structure_start_time[:6])
    if (validity_time - datetime.now()).seconds / 60 < 25:
        return fail_api(msg='邀请码有效期不能早于当前时间25分钟后的时间')

    authorCode = AuthorCode(invite_code=invite_code, validity_time=validity_time,
                            create_user_id=FRTUtils.get_current_user().id)
    db.session.add(authorCode)
    db.session.commit()

    return success_api()


@admin_invite_code_bp.delete('/remove')
@authorize("admin:invite_code:remove", log=True)
def delete():
    ids = request.form.getlist('ids[]')
    for id_ in ids:
        res = AuthorCode.query.filter_by(id=id_).delete()
        if not res:
            return fail_api(msg="删除失败")
    db.session.commit()
    return success_api(msg="删除成功")
