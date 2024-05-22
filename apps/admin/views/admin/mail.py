import flask_mail
from flask import Blueprint, render_template, request, current_app
from flask_mail import Message

from core.flask_redis_token.frt_utils import FRTUtils
from pub.curd import model_to_dicts
from pub.exts.init_sqlalchemy import db
from pub.helper import ModelFilter
from pub.models.models_system import Mail
from pub.schemas.schemas_system import MailOutSchema
from pub.utils.http_utils import table_api, fail_api, success_api
from pub.utils.rights import authorize
from pub.utils.validate import str_escape

admin_mail = Blueprint('adminMail', __name__, url_prefix='/admin/mail')


# 用户管理
@admin_mail.get('/')
@authorize("admin:mail:main")
def main():
    return render_template('admin/mail/main.html')


#   用户分页查询
@admin_mail.get('/data')
@authorize("admin:mail:main")
def data():
    # 获取请求参数
    receiver = str_escape(request.args.get("receiver"))
    subject = str_escape(request.args.get('subject'))
    content = str_escape(request.args.get('content'))
    # 查询参数构造
    mf = ModelFilter()
    if receiver:
        mf.contains(field_name="receiver", value=receiver)
    if subject:
        mf.contains(field_name="subject", value=subject)
    if content:
        mf.exact(field_name="content", value=content)
    # orm查询
    mail = Mail.query.filter(mf.get_filter(Mail)).layui_paginate()
    count = mail.total
    # 返回api
    return table_api(data=model_to_dicts(schema=MailOutSchema, data=mail.items), count=count)


# 用户增加
@admin_mail.get('/add')
@authorize("admin:mail:add", log=True)
def add():
    return render_template('admin/mail/add.html')


@admin_mail.post('/save')
@authorize("admin:mail:add", log=True)
def save():
    req_json = request.get_json(force=True)
    receiver = str_escape(req_json.get("receiver"))
    subject = str_escape(req_json.get('subject'))
    content = str_escape(req_json.get('content'))
    user_id = FRTUtils.get_current_user().id

    try:
        msg = Message(subject=subject, recipients=receiver.split(";"), body=content)
        flask_mail.send(msg)
    except Exception as e:
        current_app.log_exception(e)
        return fail_api(msg="发送失败，请检查邮件配置或发送人邮箱是否写错")

    mail = Mail(receiver=receiver, subject=subject, content=content, user_id=user_id)

    db.session.add(mail)
    db.session.commit()
    return success_api(msg="增加成功")


# 删除用户
@admin_mail.delete('/remove/<int:id_>')
@authorize("admin:mail:remove", log=True)
def delete(id_):
    res = Mail.query.filter_by(id=id_).delete()
    if not res:
        return fail_api(msg="删除失败")
    db.session.commit()
    return success_api(msg="删除成功")


# 批量删除
@admin_mail.delete('/batchRemove')
@authorize("admin:mail:remove", log=True)
def batch_remove():
    ids = request.form.getlist('ids[]')
    for id_ in ids:
        res = Mail.query.filter_by(id=id_).delete()
        if not res:
            return fail_api(msg="批量删除失败")
    db.session.commit()
    return success_api(msg="批量删除成功")
