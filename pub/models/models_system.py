import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from pub.consts import RedisKey
from pub.curd import AutoModelTransfer
from pub.exts.init_sqlalchemy import db
from pub.utils.redis_utils import Redis


class Dept(db.Model):
    __tablename__ = 'admin_dept'
    id = db.Column(db.Integer, primary_key=True, comment="部门ID")
    parent_id = db.Column(db.Integer, comment="父级编号")
    dept_name = db.Column(db.String(50), comment="部门名称")
    sort = db.Column(db.Integer, comment="排序")
    leader = db.Column(db.String(50), comment="负责人")
    phone = db.Column(db.String(20), comment="联系方式")
    email = db.Column(db.String(50), comment="邮箱")
    status = db.Column(db.Integer, comment='状态(1开启,0关闭)')
    remark = db.Column(db.Text, comment="备注")
    address = db.Column(db.String(255), comment="详细地址")
    create_at = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    update_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now,
                          comment='创建时间')


class DictType(db.Model):
    __tablename__ = 'admin_dict_type'
    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(255), comment='字典类型名称')
    type_code = db.Column(db.String(255), comment='字典类型标识')
    description = db.Column(db.String(255), comment='字典类型描述')
    enable = db.Column(db.Integer, comment='是否开启')
    create_time = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    update_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now,
                            comment='更新时间')

    @staticmethod
    def load_dicts():
        dict_types = DictType.query.all()
        for dict_type in dict_types:
            dict_items = DictData.query.filter_by(type_code=dict_type.type_code).all()
            json_dict_items = AutoModelTransfer.model_2_json(model=DictData, data=dict_items)
            Redis.hset(RedisKey.SYS_CACHE + ':Dict', dict_type.type_code, json_dict_items)

    @staticmethod
    def get_dict(type_code, load_instance=False):
        data = Redis.hget(RedisKey.SYS_CACHE + ':Dict', type_code)
        if data:
            data = AutoModelTransfer.json_2_model(model=DictData, data=data) \
                if load_instance else AutoModelTransfer.json_2_dict(model=DictData, data=data)
            return data

        data = DictData.query.filter_by(type_code=type_code).all()
        json_data = AutoModelTransfer.model_2_json(model=DictData, data=data)
        Redis.hset(RedisKey.SYS_CACHE + ':Dict', type_code, json_data)
        ret_data = AutoModelTransfer.model_2_dict(model=DictData, data=data)
        return ret_data

    @staticmethod
    def get_dict_data(type_code, data_value):
        dict_datas = DictType.get_dict(type_code, load_instance=True)
        for dict_data in dict_datas:
            if dict_data.data_value == str(data_value):
                return dict_data
        return None

    @staticmethod
    def translate(type_code, data_value):
        if data_value is not None:
            dict_data = DictType.get_dict_data(type_code, data_value)
            if not dict_data:
                return str(data_value) + '：' + str(data_value)
            return str(data_value) + '：' + dict_data.data_label
        return ''


class DictData(db.Model):
    __tablename__ = 'admin_dict_data'
    id = db.Column(db.Integer, primary_key=True)
    data_label = db.Column(db.String(255), comment='字典类型名称')
    data_value = db.Column(db.String(255), comment='字典类型标识')
    type_code = db.Column(db.String(255), comment='字典类型描述')
    is_default = db.Column(db.Integer, default=0, comment='是否默认')
    enable = db.Column(db.Integer, comment='是否开启')
    remark = db.Column(db.String(255), default='', comment='备注')
    create_time = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    update_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now,
                            comment='更新时间')

    @classmethod
    def after_add_edit_del(cls, type_code):
        data = cls.query.filter_by(type_code=type_code).all()
        json_data = AutoModelTransfer.model_2_json(model=DictData, data=data)
        Redis.hset(RedisKey.SYS_CACHE + ':Dict', type_code, json_data)


class AdminLog(db.Model):
    __tablename__ = 'admin_admin_log'
    id = db.Column(db.Integer, primary_key=True)
    method = db.Column(db.String(10))
    uid = db.Column(db.Integer)
    url = db.Column(db.String(255))
    desc = db.Column(db.Text)
    ip = db.Column(db.String(255))
    success = db.Column(db.Integer)
    user_agent = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)


class Mail(db.Model):
    __tablename__ = 'admin_mail'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='邮件编号')
    receiver = db.Column(db.String(1024), comment='收件人邮箱')
    subject = db.Column(db.String(128), comment='邮件主题')
    content = db.Column(db.Text(), comment='邮件正文')
    user_id = db.Column(db.Integer, comment='发送人id')
    create_at = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')


class Photo(db.Model):
    __tablename__ = 'admin_photo'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    href = db.Column(db.String(255))
    mime = db.Column(db.CHAR(50), nullable=False)
    size = db.Column(db.CHAR(30), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)


class Power(db.Model):
    __tablename__ = 'admin_power'
    id = db.Column(db.Integer, primary_key=True, comment='权限编号')
    name = db.Column(db.String(255), comment='权限名称')
    type = db.Column(db.String(1), comment='权限类型')
    code = db.Column(db.String(30), comment='权限标识')
    url = db.Column(db.String(255), comment='权限路径')
    open_type = db.Column(db.String(10), comment='打开方式')
    parent_id = db.Column(db.Integer, comment='父类编号')
    icon = db.Column(db.String(128), comment='图标')
    sort = db.Column(db.Integer, comment='排序')
    create_time = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    update_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now,
                            comment='更新时间')
    enable = db.Column(db.Integer, comment='是否开启')


class Role(db.Model):
    __tablename__ = 'admin_role'
    id = db.Column(db.Integer, primary_key=True, comment='角色ID')
    name = db.Column(db.String(255), comment='角色名称')
    code = db.Column(db.String(255), comment='角色标识')
    enable = db.Column(db.Integer, comment='是否启用')
    remark = db.Column(db.String(255), comment='备注')
    details = db.Column(db.String(255), comment='详情')
    sort = db.Column(db.Integer, comment='排序')
    create_time = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    update_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now,
                            comment='更新时间')
    power = db.relationship('Power', secondary="admin_role_power", backref=db.backref('role'))


# 创建中间表
role_power = db.Table(
    "admin_role_power",  # 中间表名称
    db.Column("id", db.Integer, primary_key=True, autoincrement=True, comment='标识'),  # 主键
    db.Column("power_id", db.Integer, db.ForeignKey("admin_power.id"), comment='用户编号'),  # 属性 外键
    db.Column("role_id", db.Integer, db.ForeignKey("admin_role.id"), comment='角色编号'),  # 属性 外键
)


class User(db.Model):
    __tablename__ = 'admin_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='用户ID')
    username = db.Column(db.String(20), comment='用户名')
    realname = db.Column(db.String(20), comment='真实名字')
    avatar = db.Column(db.String(255), comment='头像', default="/static/admin/admin/images/avatar.jpg")
    remark = db.Column(db.String(255), comment='备注')
    password_hash = db.Column(db.String(128), comment='哈希密码')
    enable = db.Column(db.Integer, default=0, comment='启用')
    dept_id = db.Column(db.Integer, comment='部门id')
    create_at = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    update_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now,
                          comment='创建时间')
    role = db.relationship('Role', secondary="admin_user_role", backref=db.backref('user'), lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def get_exclude_fields(cls):
        return ['password_hash']


# 创建中间表
user_role = db.Table(
    "admin_user_role",  # 中间表名称
    db.Column("id", db.Integer, primary_key=True, autoincrement=True, comment='标识'),  # 主键
    db.Column("user_id", db.Integer, db.ForeignKey("admin_user.id"), comment='用户编号'),  # 属性 外键
    db.Column("role_id", db.Integer, db.ForeignKey("admin_role.id"), comment='角色编号'),  # 属性 外键
)
