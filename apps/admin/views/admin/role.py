from flask import Blueprint, render_template, request, jsonify

from pub.curd import model_to_dicts, get_one_by_id, enable_status, disable_status
from pub.exts.init_sqlalchemy import db
from pub.models.models_system import Role, Power
from pub.schemas.schemas_system import RoleOutSchema, PowerOutSchema2
from pub.utils.http_utils import table_api, success_api, fail_api
from pub.utils.rights import authorize
from pub.utils.validate import str_escape

admin_role = Blueprint('adminRole', __name__, url_prefix='/admin/role')


# 用户管理
@admin_role.get('/')
@authorize("admin:role:main")
def main():
    return render_template('admin/role/main.html')


# 表格数据
@admin_role.get('/data')
@authorize("admin:role:main")
def table():
    role_name = str_escape(request.args.get('roleName', type=str))
    role_code = str_escape(request.args.get('roleCode', type=str))
    filters = []
    if role_name:
        filters.append(Role.name.contains(role_name))
    if role_code:
        filters.append(Role.code.contains(role_code))
    roles = Role.query.filter(*filters).layui_paginate()
    return table_api(data=model_to_dicts(schema=RoleOutSchema, data=roles.items), count=roles.total)


# 角色增加
@admin_role.get('/add')
@authorize("admin:role:add", log=True)
def add():
    return render_template('admin/role/add.html')


# 角色增加
@admin_role.post('/save')
@authorize("admin:role:add", log=True)
def save():
    req = request.get_json(force=True)
    details = str_escape(req.get("details"))
    enable = str_escape(req.get("enable"))
    roleCode = str_escape(req.get("roleCode"))
    roleName = str_escape(req.get("roleName"))
    sort = str_escape(req.get("sort"))
    role = Role(
        details=details,
        enable=enable,
        code=roleCode,
        name=roleName,
        sort=sort
    )
    db.session.add(role)
    db.session.commit()
    return success_api(msg="成功")


# 角色授权
@admin_role.get('/power/<int:_id>')
@authorize("admin:role:power", log=True)
def power(_id):
    return render_template('admin/role/power.html', id=_id)


# 获取角色权限
@admin_role.get('/getRolePower/<int:id>')
@authorize("admin:role:main", log=True)
def get_role_power(id):
    role = Role.query.filter_by(id=id).first()
    check_powers = role.power
    check_powers_list = []
    for cp in check_powers:
        check_powers_list.append(cp.id)
    powers = Power.query.all()
    power_schema = PowerOutSchema2(many=True)  # 用已继承ma.ModelSchema类的自定制类生成序列化类
    output = power_schema.dump(powers)  # 生成可序列化对象
    for i in output:
        if int(i.get("powerId")) in check_powers_list:
            i["checkArr"] = "1"
        else:
            i["checkArr"] = "0"
    res = {
        "data": output,
        "status": {"code": 200, "message": "默认"}
    }
    return jsonify(res)


# 保存角色权限
@admin_role.put('/saveRolePower')
@authorize("admin:role:edit", log=True)
def save_role_power():
    req_form = request.form
    power_ids = req_form.get("powerIds")
    power_list = power_ids.split(',')
    role_id = req_form.get("roleId")
    role = Role.query.filter_by(id=role_id).first()

    powers = Power.query.filter(Power.id.in_(power_list)).all()
    role.power = powers

    db.session.commit()
    return success_api(msg="授权成功")


# 角色编辑
@admin_role.get('/edit/<int:id_>')
@authorize("admin:role:edit", log=True)
def edit(id_):
    r = get_one_by_id(model=Role, id=id_)
    return render_template('admin/role/edit.html', role=r)


# 更新角色
@admin_role.put('/update')
@authorize("admin:role:edit", log=True)
def update():
    req_json = request.get_json(force=True)
    id = req_json.get("roleId")
    data = {
        "code": str_escape(req_json.get("roleCode")),
        "name": str_escape(req_json.get("roleName")),
        "sort": str_escape(req_json.get("sort")),
        "enable": str_escape(req_json.get("enable")),
        "details": str_escape(req_json.get("details"))
    }
    role = Role.query.filter_by(id=id).update(data)
    db.session.commit()
    if not role:
        return fail_api(msg="更新角色失败")
    return success_api(msg="更新角色成功")


# 启用用户
@admin_role.put('/enable')
@authorize("admin:role:edit", log=True)
def enable():
    id = request.get_json(force=True).get('roleId')
    if id:
        res = enable_status(Role, id)
        if not res:
            return fail_api(msg="出错啦")
        return success_api(msg="启动成功")
    return fail_api(msg="数据错误")


# 禁用用户
@admin_role.put('/disable')
@authorize("admin:role:edit", log=True)
def dis_enable():
    _id = request.get_json(force=True).get('roleId')
    if _id:
        res = disable_status(Role, _id)
        if not res:
            return fail_api(msg="出错啦")
        return success_api(msg="禁用成功")
    return fail_api(msg="数据错误")


# 角色删除
@admin_role.delete('/remove/<int:id>')
@authorize("admin:role:remove", log=True)
def remove(id):
    role = Role.query.filter_by(id=id).first()
    # 删除该角色的权限和用户
    role.power = []
    role.user = []

    r = Role.query.filter_by(id=id).delete()
    db.session.commit()
    if not r:
        return fail_api(msg="角色删除失败")
    return success_api(msg="角色删除成功")


# 批量删除
@admin_role.delete('/batchRemove')
@authorize("admin:role:remove", log=True)
def batch_remove():
    ids = request.form.getlist('ids[]')
    for id_ in ids:
        role = Role.query.filter_by(id=id_).first()
        # 删除该角色的权限和用户
        role.power = []
        role.user = []

        r = Role.query.filter_by(id=id_).delete()
        db.session.commit()
    return success_api(msg="批量删除成功")
