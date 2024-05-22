from flask import Blueprint, render_template, request, jsonify

from core.flask_redis_token.frt_utils import FRTUtils
from pub.consts.dict_consts import DictConsts
from pub.exts.init_sqlalchemy import db
from pub.models.models_business import BookSetting, Book, Author
from pub.models.models_system import DictType
from pub.utils.http_utils import table_api, success_api, fail_api
from pub.utils.rights import authorize
from pub.utils.validate import str_escape

admin_book_setting_bp = Blueprint('admin_book_setting', __name__, url_prefix='/admin/book_setting')


@admin_book_setting_bp.get('/')
@authorize("admin:book_setting:main")
def main():
    return render_template('book_setting/main.html')


@admin_book_setting_bp.get('/data')
@authorize("admin:book_setting:main")
def data():
    # 获取请求参数
    book_id = str_escape(request.args.get("book_id"))
    type_ = str_escape(request.args.get("type"))
    create_user_id = str_escape(request.args.get("create_user_id"))
    update_user_id = str_escape(request.args.get("update_user_id"))
    # 查询参数构造
    filters = []
    if book_id:
        filters.append(BookSetting.book_id == book_id)
    if type_:
        filters.append(BookSetting.type == type_)
    if create_user_id:
        filters.append(BookSetting.create_user_id == create_user_id)
    if update_user_id:
        filters.append(BookSetting.update_user_id == update_user_id)
    # orm查询
    page_data = db.session.query(
        BookSetting.id, BookSetting.type, BookSetting.sort, Book.id.label('book_id'), Book.book_name, Author.pen_name
    ).outerjoin(
        Book, BookSetting.book_id == Book.id
    ).outerjoin(
        Author, Book.author_id == Author.id
    ).filter(*filters).order_by(BookSetting.id.desc()).layui_paginate()
    count = page_data.total
    res = [
        {
            'id': record.id,
            'book_id': str(record.book_id),
            'book_name': record.book_name,
            'author': record.pen_name,
            'type': DictType.translate(DictConsts.book_rec_type, record.type),
            'sort': record.sort
        } for record in page_data.items
    ]
    # 返回api
    return table_api(data=res, count=count)


@admin_book_setting_bp.get('/add')
@authorize("admin:book_setting:add", log=True)
def add():
    return render_template('book_setting/add_new.html')


@admin_book_setting_bp.post('/save')
@authorize("admin:book_setting:add", log=True)
def save():
    req_json = request.get_json(force=True)
    book_id = str_escape(req_json.get('book_id'))
    sort = str_escape(req_json.get('sort'))
    type_ = str_escape(req_json.get('type'))

    bs = BookSetting(book_id=book_id, sort=sort, type=type_, create_user_id=FRTUtils.get_current_user().id,
                     update_user_id=FRTUtils.get_current_user().id)
    db.session.add(bs)
    db.session.commit()

    return success_api()


@admin_book_setting_bp.get('/batch_add')
@authorize("admin:book_setting:batch_add", log=True)
def batch_add():
    return render_template('book_setting/batch_add.html')


@admin_book_setting_bp.post('/batch_save')
@authorize("admin:book_setting:batch_add", log=True)
def batch_save():
    req_json = request.get_json(force=True)
    book_ids = list(req_json.get('bookIds'))
    sorts = list(req_json.get('sorts'))
    types = list(req_json.get('types'))

    for i in range(len(book_ids)):
        bs = BookSetting(book_id=book_ids[i], sort=sorts[i], type=types[i], create_user_id=FRTUtils.get_current_user().id,
                         update_user_id=FRTUtils.get_current_user().id)
        db.session.add(bs)
    db.session.commit()

    return success_api()


@admin_book_setting_bp.get('/edit')
@authorize("admin:book_setting:edit", log=True)
def edit():
    return render_template('book_setting/edit_new.html')


@admin_book_setting_bp.put('/update')
@authorize("admin:book_setting:edit", log=True)
def update():
    req_json = request.get_json(force=True)
    id_ = str_escape(req_json.get('id'))
    book_id = str_escape(req_json.get('book_id'))
    sort = str_escape(req_json.get('sort'))
    type_ = str_escape(req_json.get('type'))

    BookSetting.query.filter_by(id=id_).update({'book_id': book_id, 'sort': sort, 'type': type_})
    db.session.commit()

    return success_api(msg="更新成功")


@admin_book_setting_bp.delete('/remove')
@authorize("admin:book_setting:remove", log=True)
def delete():
    ids = request.form.getlist('ids[]')
    for id_ in ids:
        res = BookSetting.query.filter_by(id=id_).delete()
        if not res:
            return fail_api(msg="删除失败")
    db.session.commit()
    return success_api(msg="删除成功")


@admin_book_setting_bp.get('/get_detail')
@authorize("admin:book_setting:detail")
def get_detail():
    id_ = request.args.get("id")
    obj = BookSetting.query.get(id_)
    res = {
        'id': obj.id,
        'book_id': str(obj.book_id),
        'sort': obj.sort,
        'type': obj.type
    }
    return jsonify(code=0, data=res)
