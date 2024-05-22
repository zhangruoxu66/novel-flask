from flask import Blueprint, render_template
from sqlalchemy import desc

from pub.curd import model_to_dicts
from pub.models.models_system import AdminLog
from pub.schemas.schemas_system import LogOutSchema
from pub.utils.http_utils import table_api
from pub.utils.rights import authorize

admin_log = Blueprint('adminLog', __name__, url_prefix='/admin/log')


# 日志管理
@admin_log.get('/')
@authorize("admin:log:main")
def index():
    return render_template('admin/admin_log/main.html')


# 登录日志
@admin_log.get('/loginLog')
@authorize("admin:log:main")
def login_log():
    log = AdminLog.query.filter_by(url='/passport/login').order_by(desc(AdminLog.create_time)).layui_paginate()
    count = log.total
    return table_api(data=model_to_dicts(schema=LogOutSchema, data=log.items), count=count)


# 操作日志
@admin_log.get('/operateLog')
@authorize("admin:log:main")
def operate_log():
    log = AdminLog.query.filter(
        AdminLog.url != '/passport/login').order_by(
        desc(AdminLog.create_time)).layui_paginate()
    count = log.total
    return table_api(data=model_to_dicts(schema=LogOutSchema, data=log.items), count=count)
