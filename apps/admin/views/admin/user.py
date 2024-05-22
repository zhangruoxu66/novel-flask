from flask import Blueprint, render_template, request
from sqlalchemy import desc

from apps.admin.dto.request import AdminUserQueryModel, AdminUserAddModel, AdminUserUpdateModel
from apps.admin.dto.response import UserDataRespModel
from core.flask_redis_token.frt_utils import login_required, FRTUtils
from pub import curd
from pub.curd import enable_status, disable_status
from pub.dto.response import BaseTableRespModel
from pub.exts.init_siwadoc import siwa
from pub.exts.init_sqlalchemy import db
from pub.models.models_system import User, Dept, Role, AdminLog
from pub.utils.http_utils import table_api, fail_api, success_api
from pub.utils.rights import authorize
from pub.utils.validate import str_escape

admin_user = Blueprint('adminUser', __name__, url_prefix='/admin/user')


# 用户管理
@admin_user.get('/')
@authorize("admin:user:main")
def main():
    return render_template('admin/user/main.html')


#   用户分页查询
@admin_user.get('/data')
@siwa.doc(query=AdminUserQueryModel, resp=BaseTableRespModel[UserDataRespModel], summary="用户列表分页查询", tags=["用户管理"], group="admin")
@authorize("admin:user:main")
def data(query: AdminUserQueryModel):
    filters = []
    if query.real_name:
        filters.append(User.realname.contains(query.real_name))
    if query.username:
        filters.append(User.realname.contains(query.username))
    if query.dept_id:
        filters.append(User.realname == query.dept_id)

    query = db.session.query(
        User,
        Dept
    ).filter(*filters).outerjoin(Dept, User.dept_id == Dept.id).layui_paginate()

    return table_api(
        data=[{
            'id': user.id,
            'username': user.username,
            'realname': user.realname,
            'enable': user.enable,
            'create_at': user.create_at,
            'update_at': user.update_at,
            'dept_name': dept.dept_name if dept else None
        } for user, dept in query.items],
        count=query.total)


# 用户增加
@admin_user.get('/add')
@authorize("admin:user:add", log=True)
def add():
    roles = Role.query.all()
    return render_template('admin/user/add.html', roles=roles)


@admin_user.post('/save')
@siwa.doc(body=AdminUserAddModel, summary="保存用户", tags=["用户管理"], group="admin")
@authorize("admin:user:add", log=True)
def save(body: AdminUserAddModel):
    role_ids = body.role_ids.split(',')

    if not body.username or not body.real_name or not body.password:
        return fail_api(msg="账号姓名密码不得为空")

    if bool(User.query.filter_by(username=body.username).count()):
        return fail_api(msg="用户已经存在")
    user = User(username=body.username, realname=body.real_name)
    user.set_password(body.password)
    db.session.add(user)
    roles = Role.query.filter(Role.id.in_(role_ids)).all()
    for r in roles:
        user.role.append(r)
    db.session.commit()
    return success_api(msg="增加成功")


# 删除用户
@admin_user.delete('/remove/<int:id_>')
@authorize("admin:user:remove", log=True)
def delete(id_):
    user = User.query.filter_by(id=id_).first()
    user.role = []

    res = User.query.filter_by(id=id_).delete()
    db.session.commit()
    if not res:
        return fail_api(msg="删除失败")
    return success_api(msg="删除成功")


#  编辑用户
@admin_user.get('/edit/<int:id_>')
@authorize("admin:user:edit", log=True)
def edit(id_):
    user = curd.get_one_by_id(User, id_)
    roles = Role.query.all()
    checked_roles = []
    for r in user.role:
        checked_roles.append(r.id)
    return render_template('admin/user/edit.html', user=user, roles=roles, checked_roles=checked_roles)


#  编辑用户
@admin_user.put('/update')
@siwa.doc(body=AdminUserUpdateModel, summary="修改用户", tags=["用户管理"], group="admin")
@authorize("admin:user:edit", log=True)
def update(body: AdminUserUpdateModel):
    role_ids = body.role_ids.split(',')
    User.query.filter_by(id=body.user_id).update(
        {'username': body.username, 'realname': body.real_name, 'dept_id': body.dept_id}
    )
    u = User.query.filter_by(id=body.user_id).first()

    roles = Role.query.filter(Role.id.in_(role_ids)).all()
    u.role = roles

    db.session.commit()
    return success_api(msg="更新成功")


# 个人中心
@admin_user.get('/center')
@login_required
def center():
    user_info = FRTUtils.get_current_user()
    user_logs = AdminLog.query.filter_by(url='/passport/login').filter_by(uid=FRTUtils.get_current_user().id).order_by(
        desc(AdminLog.create_time)).limit(10)
    return render_template('admin/user/center.html', user_info=user_info, user_logs=user_logs)


# 修改头像
@admin_user.get('/profile')
@login_required
def profile():
    return render_template('admin/user/profile.html')


# 修改头像
@admin_user.put('/updateAvatar')
@login_required
def update_avatar():
    url = request.get_json(force=True).get("avatar").get("src")
    r = User.query.filter_by(id=FRTUtils.get_current_user().id).update({"avatar": url})
    db.session.commit()
    if not r:
        return fail_api(msg="出错啦")
    return success_api(msg="修改成功")


# 修改当前用户信息
@admin_user.put('/updateInfo')
@login_required
def update_info():
    req_json = request.get_json(force=True)
    r = User.query.filter_by(id=FRTUtils.get_current_user().id).update(
        {"realname": req_json.get("realName"), "remark": req_json.get("details")})
    db.session.commit()
    if not r:
        return fail_api(msg="出错啦")
    return success_api(msg="更新成功")


# 修改当前用户密码
@admin_user.get('/editPassword')
@login_required
def edit_password():
    return render_template('admin/user/edit_password.html')


# 修改当前用户密码
@admin_user.put('/editPassword')
@login_required
def edit_password_put():
    res_json = request.get_json(force=True)
    if res_json.get("newPassword") == '':
        return fail_api("新密码不得为空")
    if res_json.get("newPassword") != res_json.get("confirmPassword"):
        return fail_api("俩次密码不一样")
    user = FRTUtils.get_current_user()
    is_right = user.validate_password(res_json.get("oldPassword"))
    if not is_right:
        return fail_api("旧密码错误")
    user.set_password(res_json.get("newPassword"))
    db.session.add(user)
    db.session.commit()
    return success_api("更改成功")


# 启用用户
@admin_user.put('/enable')
@authorize("admin:user:edit", log=True)
def enable():
    _id = request.get_json(force=True).get('userId')
    if _id:
        res = enable_status(model=User, id=_id)
        if not res:
            return fail_api(msg="出错啦")
        return success_api(msg="启动成功")
    return fail_api(msg="数据错误")


# 禁用用户
@admin_user.put('/disable')
@authorize("admin:user:edit", log=True)
def dis_enable():
    _id = request.get_json(force=True).get('userId')
    if _id:
        res = disable_status(model=User, id=_id)
        if not res:
            return fail_api(msg="出错啦")
        return success_api(msg="禁用成功")
    return fail_api(msg="数据错误")


# 批量删除
@admin_user.delete('/batchRemove')
@authorize("admin:user:remove", log=True)
def batch_remove():
    ids = request.form.getlist('ids[]')
    for id_ in ids:
        user = User.query.filter_by(id=id_).first()
        user.role = []

        res = User.query.filter_by(id=id_).delete()
        db.session.commit()
    return success_api(msg="批量删除成功")
