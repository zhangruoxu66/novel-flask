from flask import Blueprint, render_template, request, jsonify

from pub import curd
from pub.exts.init_sqlalchemy import db
from pub.helper import ModelFilter
from pub.models.models_system import DictType, DictData
from pub.schemas.schemas_system import DictTypeOutSchema, DictDataOutSchema
from pub.utils.http_utils import table_api, fail_api, success_api
from pub.utils.rights import authorize
from pub.utils.validate import str_escape

admin_dict = Blueprint('adminDict', __name__, url_prefix='/admin/dict')


# 数据字典
@admin_dict.get('/')
@authorize("admin:dict:main")
def main():
    return render_template('admin/dict/main.html')


@admin_dict.get('/dictType/data')
@authorize("admin:dict:main")
def dict_type_data():
    # 获取请求参数
    type_name = str_escape(request.args.get('typeName', type=str))
    # 查询参数构造
    mf = ModelFilter()
    if type_name:
        mf.vague(field_name="type_name", value=type_name)
    # orm查询
    dict_all = DictType.query.filter(mf.get_filter(DictType)).layui_paginate()
    count = dict_all.total
    data = curd.model_to_dicts(schema=DictTypeOutSchema, data=dict_all.items)
    return table_api(data=data, count=count)


@admin_dict.get('/dictType/add')
@authorize("admin:dict:add", log=True)
def dict_type_add():
    return render_template('admin/dict/add.html')


@admin_dict.post('/dictType/save')
@authorize("admin:dict:add", log=True)
def dict_type_save():
    req_json = request.get_json(force=True)
    description = str_escape(req_json.get("description"))
    enable = str_escape(req_json.get("enable"))
    type_code = str_escape(req_json.get("typeCode"))
    type_name = str_escape(req_json.get("typeName"))
    d = DictType(type_name=type_name, type_code=type_code, enable=enable, description=description)
    db.session.add(d)
    db.session.commit()
    if d.id is None:
        return fail_api(msg="增加失败")
    return success_api(msg="增加成功")


#  编辑字典类型
@admin_dict.get('/dictType/edit')
@authorize("admin:dict:edit", log=True)
def dict_type_edit():
    id_ = request.args.get('dictTypeId', type=int)
    dict_type = DictType.query.filter_by(id=id_).first()
    return render_template('admin/dict/edit.html', dict_type=dict_type)


#  编辑字典类型
@admin_dict.put('/dictType/update')
@authorize("admin:dict:edit", log=True)
def dict_type_update():
    req_json = request.get_json(force=True)
    id_ = str_escape(req_json.get("id"))
    description = str_escape(req_json.get("description"))
    enable = str_escape(req_json.get("enable"))
    type_code = str_escape(req_json.get("typeCode"))
    type_name = str_escape(req_json.get("typeName"))
    DictType.query.filter_by(id=id_).update({
        "description": description,
        "enable": enable,
        "type_code": type_code,
        "type_name": type_name
    })
    db.session.commit()
    return success_api(msg="更新成功")


# 启用字典
@admin_dict.put('/dictType/enable')
@authorize("admin:dict:edit", log=True)
def dict_type_enable():
    id_ = request.get_json(force=True).get('id')
    if id:
        res = curd.enable_status(DictType, id_)
        if not res:
            return fail_api(msg="出错啦")
        return success_api("启动成功")
    return fail_api(msg="数据错误")


# 禁用字典
@admin_dict.put('/dictType/disable')
@authorize("admin:dict:edit", log=True)
def dict_type_dis_enable():
    id_ = request.get_json(force=True).get('id')
    if id:
        res = curd.disable_status(DictType, id_)
        if not res:
            return fail_api(msg="出错啦")
        return success_api("禁用成功")
    return fail_api(msg="数据错误")


# 删除字典类型
@admin_dict.delete('/dictType/remove/<int:id_>')
@authorize("admin:dict:remove", log=True)
def dict_type_delete(id_):
    res = curd.delete_one_by_id(DictType, id_)
    if not res:
        return fail_api(msg="删除失败")
    return success_api(msg="删除成功")


@admin_dict.get('/dictData/data')
@authorize("admin:dict:main", log=True)
def dict_code_data():
    type_code = str_escape(request.args.get('typeCode', type=str))
    dict_data = DictData.query.filter_by(type_code=type_code).layui_paginate()
    count = dict_data.total
    data = curd.model_to_dicts(schema=DictDataOutSchema, data=dict_data.items)
    return table_api(data=data, count=count)


@admin_dict.get('/dictData/get')
@authorize("admin:dict:main")
def get_dict_data():
    dictKey = str_escape(request.args.get('dictKey', type=str))
    dict_data = DictType.get_dict(dictKey)
    return jsonify(success=True, msg="", data=dict_data)


# 增加字典数据
@admin_dict.get('/dictData/add')
@authorize("admin:dict:add", log=True)
def dict_data_add():
    type_code = request.args.get('typeCode', type=str)
    return render_template('admin/dict/data/add.html', type_code=type_code)


# 增加字典数据
@admin_dict.post('/dictData/save')
@authorize("admin:dict:add", log=True)
def dict_data_save():
    req_json = request.get_json(force=True)
    data_label = str_escape(req_json.get("dataLabel"))
    data_value = str_escape(req_json.get("dataValue"))
    enable = str_escape(req_json.get("enable"))
    remark = str_escape(req_json.get("remark"))
    type_code = str_escape(req_json.get("typeCode"))
    d = DictData(data_label=data_label, data_value=data_value, enable=enable, remark=remark, type_code=type_code)
    db.session.add(d)
    db.session.commit()
    if not d.id:
        return jsonify(success=False, msg="增加失败")
    return jsonify(success=True, msg="增加成功")


#  编辑字典数据
@admin_dict.get('/dictData/edit')
@authorize("admin:dict:edit", log=True)
def dict_data_edit():
    id_ = request.args.get('dataId', type=str)
    dict_data = curd.get_one_by_id(DictData, id_)
    return render_template('admin/dict/data/edit.html', dict_data=dict_data)


#  编辑字典数据
@admin_dict.put('/dictData/update')
@authorize("admin:dict:edit", log=True)
def dict_data_update():
    req_json = request.get_json(force=True)
    id_ = req_json.get("dataId")
    DictData.query.filter_by(id=id_).update({
        "data_label": str_escape(req_json.get("dataLabel")),
        "data_value": str_escape(req_json.get("dataValue")),
        "enable": str_escape(req_json.get("enable")),
        "remark": str_escape(req_json.get("remark")),
        "type_code": str_escape(req_json.get("typeCode"))
    })
    db.session.commit()
    return success_api(msg="更新成功")


# 启用字典数据
@admin_dict.put('/dictData/enable')
@authorize("admin:dict:edit", log=True)
def dict_data_enable():
    id_ = request.get_json(force=True).get('dataId')
    if id_:
        res = curd.enable_status(model=DictData, id=id_)
        if not res:
            return fail_api(msg="出错啦")
        return success_api(msg="启动成功")
    return fail_api(msg="数据错误")


# 禁用字典数据
@admin_dict.put('/dictData/disable')
@authorize("admin:dict:edit", log=True)
def dict_data_disenable():
    id_ = request.get_json(force=True).get('dataId')
    if id_:
        res = curd.disable_status(model=DictData, id=id_)
        if not res:
            return fail_api(msg="出错啦")
        return success_api(msg="禁用成功")
    return fail_api(msg="数据错误")


# 删除字典类型
@admin_dict.delete('dictData/remove/<int:id_>')
@authorize("admin:dict:remove", log=True)
def dict_data_delete(id_):
    res = curd.delete_one_by_id(model=DictData, id=id_)
    if not res:
        return fail_api(msg="删除失败")
    return success_api(msg="删除成功")
