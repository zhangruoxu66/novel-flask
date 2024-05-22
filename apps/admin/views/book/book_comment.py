from flask import Blueprint, render_template, request, jsonify

from pub.consts.dict_consts import DictConsts
from pub.exts.init_sqlalchemy import db
from pub.models.models_business import BookComment, Book, User
from pub.models.models_system import DictType
from pub.utils.http_utils import table_api, fail_api, success_api
from pub.utils.rights import authorize
from pub.utils.string_utils import protect_mobile
from pub.utils.validate import str_escape

admin_book_comment_bp = Blueprint('admin_book_comment', __name__, url_prefix='/admin/book_comment')


@admin_book_comment_bp.get('/')
@authorize("admin:book_comment:main")
def main():
    return render_template('book_comment/main.html')


@admin_book_comment_bp.get('/data')
@authorize("admin:book_comment:main")
def data():
    # 获取请求参数
    book_name = str_escape(request.args.get("book_name"))
    author_name = str_escape(request.args.get("author_name"))
    username = str_escape(request.args.get("username"))
    nick_name = str_escape(request.args.get("nick_name"))
    work_direction = str_escape(request.args.get("work_direction"))
    category = str_escape(request.args.get("category"))

    # 查询参数构造
    filters = []
    if book_name:
        filters.append(Book.book_name.ilike('%' + book_name + '%'))
    if author_name:
        filters.append(Book.author_name.ilike('%' + author_name + '%'))
    if username:
        filters.append(User.username.ilike('%' + username + '%'))
    if nick_name:
        filters.append(User.nick_name.ilike('%' + nick_name + '%'))
    if work_direction:
        filters.append(Book.work_direction == work_direction)
    if category:
        filters.append(Book.cat_id == category)

    page_data = db.session.query(
        BookComment, Book, User
    ).outerjoin(
        Book, BookComment.book_id == Book.id
    ).outerjoin(
        User, BookComment.create_user_id == User.id
    ).filter(
        *filters
    ).order_by(
        BookComment.id.desc()
    ).layui_paginate()
    count = page_data.total

    res = [
        {
            'id': str(comment.id),
            'book_id': str(book.id),
            'book_name': book.book_name,
            'author_name': book.author_name,
            'user_id': str(user.id),
            'username': protect_mobile(user.username),
            'nick_name': protect_mobile(user.nick_name) if user.nick_name == user.username else user.nick_name,
            'comment_content': comment.comment_content,
            'reply_count': comment.reply_count,
            'audit_status': comment.audit_status,
            'audit_status_name': DictType.translate(DictConsts.audit_status, comment.audit_status),

            'create_time': comment.create_time,
            'create_time_name': comment.create_time.strftime("%Y-%m-%d %H:%M:%S") if comment.create_time else ''
        } for comment, book, user in page_data.items
    ]
    # 返回api
    return table_api(data=res, count=count)


@admin_book_comment_bp.delete('/remove')
@authorize("admin:book_comment:remove", log=True)
def delete():
    ids = request.form.getlist('ids[]')
    for id_ in ids:
        res = BookComment.query.filter_by(id=id_).delete()
        if not res:
            return fail_api(msg="删除失败")
    db.session.commit()
    return success_api(msg="删除成功")


@admin_book_comment_bp.get('/detail')
@authorize("admin:book_comment:detail")
def detail():
    return render_template('book_comment/detail_new.html')


@admin_book_comment_bp.get('/get_detail')
@authorize("admin:book_comment:detail")
def get_detail():
    id_ = request.args.get("id")
    comment, book, user = db.session.query(
        BookComment, Book, User
    ).outerjoin(
        Book, BookComment.book_id == Book.id
    ).outerjoin(
        User, BookComment.create_user_id == User.id
    ).filter(
        BookComment.id == id_
    ).order_by(
        BookComment.id.desc()
    ).first()
    res = {
        'id': str(comment.id),
        'book_id': str(book.id),
        'book_name': book.book_name,
        'author_name': book.author_name,
        'user_id': str(user.id),
        'username': protect_mobile(user.username),
        'nick_name': protect_mobile(user.nick_name) if user.nick_name == user.username else user.nick_name,
        'comment_content': comment.comment_content,
        'reply_count': comment.reply_count,
        'audit_status': comment.audit_status,
        'audit_status_name': DictType.translate(DictConsts.audit_status, comment.audit_status),

        'create_time': comment.create_time,
        'create_time_name': comment.create_time.strftime("%Y-%m-%d %H:%M:%S") if comment.create_time else ''
    }
    return jsonify(code=0, data=res)
