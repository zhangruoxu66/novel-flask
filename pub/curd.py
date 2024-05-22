import datetime

from marshmallow import Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from pub.exts.init_sqlalchemy import db, ma


class LogicalDeleteMixin(object):
    """
    class Test(db.Model,LogicalDeleteMixin):
    __tablename__ = 'admin_test'
    id = db.Column(db.Integer, primary_key=True, comment='角色ID')

    Test.query.filter_by(id=1).soft_delete()
    Test.query.logic_all()
    """
    create_at = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    update_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now,
                          comment='创建时间')
    delete_at = db.Column(db.DateTime, comment='删除时间')


BLACK_FIELDS = 'BLACK_FIELDS'
WHITE_FIELDS = 'WHITE_FIELDS'


class AutoModelTransfer(object):

    @classmethod
    def __auto_model_jsonify_model(cls, data, model: db.Model, many=True, is_model_to_json=True, load_instance=True,
                                   to_dict=True, input_json=True, use_exclude_fields=True):
        """
        不需要建立schemas，直接使用orm的定义模型进行序列化
        基本功能，待完善
        示例
        power_data = curd.auto_model_jsonify_model(model=Dept, data=dept)

        :param data: 需要处理的数据，如果是序列化，则为模型对象（单个对象，或者可迭代对象（对象元组/列表等））；如果是反序列化，则为json字符串
        :param model: 数据序列化/反序列化基于的模型类
        :param many: 是否多条数据，默认True多条（传入的是装有模型类对象的元组），单挑则为False，传入单个模型对象
        :param is_model_to_json: 序列化/转换方向，默认model_to_json=True（正向/序列化，即模型（元组）对象转json对象），为False则为反序列化
        :param load_instance: 反序列化时返回模型对象还是字典，True返回模型对象，False返回字典，默认True
        :param to_dict: 序列化时返回字典（dump）还是json字符串（dumps），默认True：返回字典
        :param input_json: 反序列化时输入是字典还是json字符串，True：json字符串，False字典，默认True：json字符串
        :param use_exclude_fields: 是否使用排除属性（黑名单），模型类下就会有一个get_exclude_keys方法，返回的是不需要序列化的属性列表，use_exclude_keys来决定是否使用，默认True使用，即不序列化排除的属性

        :return: 序列化后的对象（字典/json字符串） if model_to_json=True else 反序列化后的对象（字典/模型对象）
        """

        def get_model():
            return model

        def get_load_instance():
            return load_instance

        def get_exclude_fields():
            if use_exclude_fields:
                return model.get_exclude_fields() if callable(getattr(model, "get_exclude_fields", None)) else []
            return []

        class AutoSchema(SQLAlchemyAutoSchema):
            class Meta(Schema):
                model = get_model()
                # 黑名单字段，序列化器中不使用的字段，与白名单互斥，设置了该属性，则剩余字段就是全部使用的了
                exclude = get_exclude_fields()  # 构造器禁用的字段列表
                include_fk = True  # 序列化阶段是否也一并返回主键,也就是是否返回ID
                include_relationships = True  # 输出模型对象时同时对外键，是否也一并进行处理
                load_instance = get_load_instance()  # 反序列化阶段时，True会直接返回模型对象，False会返回字典
                sqla_session = db.session  # 当前数据库连接的session会话对象

        common_schema = AutoSchema(many=many)  # 用已继承ma.ModelSchema类的自定制类生成序列化类
        if is_model_to_json:
            output = common_schema.dump(data) if to_dict else common_schema.dumps(data)
        else:
            output = common_schema.loads(data) if input_json else common_schema.load(data)

        return output

    @classmethod
    def model_2_json(cls, data, model: db.Model, many=True, use_exclude_fields=True):
        """
        模型类转json字符串
        :param data:
        :param model:
        :param many:
        :param use_exclude_fields:
        :return:
        """
        return cls.__auto_model_jsonify_model(data, model, many=many, is_model_to_json=True, to_dict=False,
                                              use_exclude_fields=use_exclude_fields)

    @classmethod
    def model_2_dict(cls, data, model: db.Model, many=True, use_exclude_fields=True):
        """
        模型类转字典
        :param data:
        :param model:
        :param many:
        :param use_exclude_fields:
        :return:
        """
        return cls.__auto_model_jsonify_model(data, model, many=many, is_model_to_json=True, to_dict=True,
                                              use_exclude_fields=use_exclude_fields)

    @classmethod
    def json_2_model(cls, data, model: db.Model, many=True, use_exclude_fields=True):
        """
        json字符串转模型类
        :param data:
        :param model:
        :param many:
        :param use_exclude_fields:
        :return:
        """
        return cls.__auto_model_jsonify_model(data, model, many=many, is_model_to_json=False, load_instance=True,
                                              use_exclude_fields=use_exclude_fields)

    @classmethod
    def json_2_dict(cls, data, model: db.Model, many=True, use_exclude_fields=True):
        """
        json字符串转字典
        :param data:
        :param model:
        :param many:
        :param use_exclude_fields:
        :return:
        """
        return cls.__auto_model_jsonify_model(data, model, many=many, is_model_to_json=False, load_instance=False,
                                              use_exclude_fields=use_exclude_fields)


def model_to_dicts(schema: ma.Schema, data):
    """
    :param schema: schema类
    :param data: sqlalchemy查询结果
    :return: 返回单个查询结果
    """
    # 如果是分页器返回，需要传入model.items
    common_schema = schema(many=True)  # 用已继承ma.ModelSchema类的自定制类生成序列化类
    output = common_schema.dump(data)  # 生成可序列化对象
    return output


def model_to_json(schema: ma.Schema, data):
    """
    :param schema: schema类
    :param data: sqlalchemy查询结果
    :return: 返回单个查询结果
    """
    # 如果是分页器返回，需要传入model.items
    common_schema = schema(many=True)  # 用已继承ma.ModelSchema类的自定制类生成序列化类
    output = common_schema.dumps(data)  # 生成可序列化对象
    return output


def json_to_model(schema: ma.Schema, data):
    # 如果是分页器返回，需要传入model.items
    common_schema = schema(many=True)
    output = common_schema.loads(data)
    return output


def get_one_by_id(model: db.Model, id):
    """
    :param model: 模型类
    :param id: id
    :return: 返回单个查询结果
    """
    return model.query.filter_by(id=id).first()


def delete_one_by_id(model: db.Model, id):
    """
    :param model: 模型类
    :param id: id
    :return: 返回单个查询结果
    """
    r = model.query.filter_by(id=id).delete()
    db.session.commit()
    return r


# 启动状态
def enable_status(model: db.Model, id, field="enable", enable=1):
    role = model.query.filter_by(id=id).update({field: enable})
    if role:
        db.session.commit()
        return True
    return False


# 停用状态
def disable_status(model: db.Model, id, field="enable", disable=0):
    role = model.query.filter_by(id=id).update({field: disable})
    if role:
        db.session.commit()
        return True
    return False
