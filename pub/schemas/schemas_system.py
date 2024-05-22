from marshmallow import fields, validate

from pub.exts.init_sqlalchemy import ma
from pub.models.models_system import User


class DeptInSchema(ma.Schema):
    parentId = fields.Integer(required=True)
    deptName = fields.Str(required=True)
    leader = fields.Str(required=True)
    phone = fields.Str(required=True)
    email = fields.Str(validate=validate.Email())
    address = fields.Str()
    status = fields.Str(validate=validate.OneOf(["0", "1"]))
    sort = fields.Integer()


class DeptOutSchema(ma.Schema):
    deptId = fields.Integer(attribute="id")
    parentId = fields.Integer(attribute="parent_id")
    deptName = fields.Str(attribute="dept_name")
    leader = fields.Str()
    phone = fields.Str()
    email = fields.Str(validate=validate.Email())
    address = fields.Str()
    status = fields.Str(validate=validate.OneOf(["0", "1"]))
    sort = fields.Integer()


class DictTypeOutSchema(ma.Schema):
    id = fields.Str(attribute="id")
    typeName = fields.Str(attribute="type_name")
    typeCode = fields.Str(attribute="type_code")
    description = fields.Str(attribute="description")
    createTime = fields.Str(attribute="create_time")
    updateName = fields.Str(attribute="update_time")
    remark = fields.Str()
    enable = fields.Str()


class DictDataOutSchema(ma.Schema):
    dataId = fields.Str(attribute="id")
    dataLabel = fields.Str(attribute="data_label")
    dataValue = fields.Str(attribute="data_value")
    remark = fields.Str()
    enable = fields.Str()


class LogOutSchema(ma.Schema):
    id = fields.Integer()
    method = fields.Str()
    uid = fields.Str()
    url = fields.Str()
    desc = fields.Str()
    ip = fields.Str()
    user_agent = fields.Str()
    success = fields.Bool()
    create_time = fields.DateTime()


# 用户models的序列化类
class MailOutSchema(ma.Schema):
    id = fields.Integer()
    receiver = fields.Str()
    subject = fields.Str()
    content = fields.Str()
    realname = fields.Method("get_realname")
    create_at = fields.DateTime()

    def get_realname(self, obj):
        if obj.user_id != None:
            return User.query.filter_by(id=obj.user_id).first().realname
        else:
            return None


class PhotoOutSchema(ma.Schema):
    id = fields.Integer()
    name = fields.Str()
    href = fields.Str()
    mime = fields.Str()
    size = fields.Str()
    ext = fields.Str()
    create_time = fields.DateTime()


# 权限models序列化类
class PowerOutSchema(ma.Schema):
    id = fields.Integer()
    title = fields.Str(attribute="name")
    type = fields.Str()
    code = fields.Str()
    href = fields.Str(attribute="url")
    openType = fields.Str(attribute="open_type")
    parent_id = fields.Integer()
    icon = fields.Str()
    sort = fields.Integer()
    # create_time = fields.DateTime()
    # update_time = fields.DateTime()
    enable = fields.Integer()


class PowerOutSchema2(ma.Schema):  # 序列化类
    powerId = fields.Str(attribute="id")
    powerName = fields.Str(attribute="name")
    powerType = fields.Str(attribute="type")
    powerUrl = fields.Str(attribute="url")
    openType = fields.Str(attribute="open_type")
    parentId = fields.Str(attribute="parent_id")
    icon = fields.Str()
    sort = fields.Integer()
    create_time = fields.DateTime()
    update_time = fields.DateTime()
    enable = fields.Integer()


class RoleOutSchema(ma.Schema):
    id = fields.Integer()
    roleName = fields.Str(attribute="name")
    roleCode = fields.Str(attribute="code")
    enable = fields.Str()
    remark = fields.Str()
    details = fields.Str()
    sort = fields.Integer()
    create_at = fields.DateTime()
    update_at = fields.DateTime()
