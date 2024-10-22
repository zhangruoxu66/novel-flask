from flask import Blueprint, render_template, request, jsonify

from pub import curd
from pub.exts.init_sqlalchemy import db
from pub.models.models_system import Power
from pub.schemas.schemas_system import PowerOutSchema2
from pub.utils.http_utils import success_api, fail_api
from pub.utils.rights import authorize
from pub.utils.validate import str_escape

admin_power = Blueprint('adminPower', __name__, url_prefix='/admin/power')


@admin_power.get('/')
@authorize("admin:power:main")
def index():
    return render_template('admin/power/main.html')


@admin_power.post('/data')
@authorize("admin:power:main")
def data():
    power = Power.query.all()
    res = {
        "data": curd.model_to_dicts(schema=PowerOutSchema2, data=power)
    }
    return jsonify(res)


@admin_power.get('/add')
@authorize("admin:power:add", log=True)
def add():
    return render_template('admin/power/add.html')


@admin_power.get('/selectParent')
@authorize("admin:power:main", log=True)
def select_parent():
    power = Power.query.all()
    res = curd.model_to_dicts(schema=PowerOutSchema2, data=power)
    res.append({"powerId": 0, "powerName": "顶级权限", "parentId": -1})
    res = {
        "status": {"code": 200, "message": "默认"},
        "data": res

    }
    return jsonify(res)


# 增加
@admin_power.post('/save')
@authorize("admin:power:add", log=True)
def save():
    req = request.get_json(force=True)
    icon = str_escape(req.get("icon"))
    openType = str_escape(req.get("openType"))
    parentId = str_escape(req.get("parentId"))
    powerCode = str_escape(req.get("powerCode"))
    powerName = str_escape(req.get("powerName"))
    powerType = str_escape(req.get("powerType"))
    powerUrl = str_escape(req.get("powerUrl"))
    sort = str_escape(req.get("sort"))
    power = Power(
        icon=icon,
        open_type=openType,
        parent_id=parentId,
        code=powerCode,
        name=powerName,
        type=powerType,
        url=powerUrl,
        sort=sort,
        enable=1
    )
    r = db.session.add(power)
    db.session.commit()
    return success_api(msg="成功")


# 权限编辑
@admin_power.get('/edit/<int:_id>')
@authorize("admin:power:edit", log=True)
def edit(_id):
    power = curd.get_one_by_id(Power, _id)
    icon = str(power.icon).split()
    if len(icon) == 2:
        icon = icon[1]
    else:
        icon = None
    return render_template('admin/power/edit.html', power=power, icon=icon)


# 权限更新
@admin_power.put('/update')
@authorize("admin:power:edit", log=True)
def update():
    req_json = request.get_json(force=True)
    id_ = request.get_json(force=True).get("powerId")
    data_ = {
        "icon": str_escape(req_json.get("icon")),
        "open_type": str_escape(req_json.get("openType")),
        "parent_id": str_escape(req_json.get("parentId")),
        "code": str_escape(req_json.get("powerCode")),
        "name": str_escape(req_json.get("powerName")),
        "type": str_escape(req_json.get("powerType")),
        "url": str_escape(req_json.get("powerUrl")),
        "sort": str_escape(req_json.get("sort"))
    }
    res = Power.query.filter_by(id=id_).update(data_)
    db.session.commit()
    if not res:
        return fail_api(msg="更新权限失败")
    return success_api(msg="更新权限成功")


# 启用权限
@admin_power.put('/enable')
@authorize("admin:power:edit", log=True)
def enable():
    id_ = request.get_json(force=True).get('powerId')
    if id:
        res = curd.enable_status(Power, id_)
        if not res:
            return fail_api(msg="出错啦")
        return success_api(msg="启用成功")
    return fail_api(msg="数据错误")


# 禁用权限
@admin_power.put('/disable')
@authorize("admin:power:edit", log=True)
def dis_enable():
    _id = request.get_json(force=True).get('powerId')
    if id:
        res = curd.disable_status(Power, _id)
        if not res:
            return fail_api(msg="出错啦")
        return success_api(msg="禁用成功")
    return fail_api(msg="数据错误")


# 权限删除
@admin_power.delete('/remove/<int:id>')
@authorize("admin:power:remove", log=True)
def remove(id):
    power = Power.query.filter_by(id=id).first()
    power.role = []

    r = Power.query.filter_by(id=id).delete()
    db.session.commit()
    if r:
        return success_api(msg="删除成功")
    else:
        return fail_api(msg="删除失败")


# 批量删除
@admin_power.delete('/batchRemove')
@authorize("admin:power:remove", log=True)
def batch_remove():
    ids = request.form.getlist('ids[]')
    for id in ids:
        power = Power.query.filter_by(id=id).first()
        power.role = []

        r = Power.query.filter_by(id=id).delete()
        db.session.commit()
    return success_api(msg="批量删除成功")
