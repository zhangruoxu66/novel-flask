import threading
from typing import List

from flask import Blueprint, render_template, request, jsonify, copy_current_request_context
from sqlalchemy import or_

from pub.consts.dict_consts import DictConsts
from pub.curd import enable_status, disable_status
from pub.exts.init_sqlalchemy import db
from pub.helper import ModelFilter
from pub.models.models_business import Book, AuthorIncomeDetail, AuthorIncome, BookComment, BookSetting, UserBookshelf, \
    UserBuyRecord, UserReadHistory, BookIndex, BookContent
from pub.models.models_system import DictType
from pub.utils.http_utils import table_api, fail_api, success_api
from pub.utils.rights import authorize
from pub.utils.validate import str_escape

admin_book_bp = Blueprint('admin_book', __name__, url_prefix='/admin/book')

order_by_type = {
    0: Book.id.desc(),
    1: Book.create_time.desc(),  # 最新入库排序
    2: Book.last_index_update_time.desc(),  # 最新更新时间排序
    3: Book.visit_count.desc(),
    4: Book.word_count.desc(),
    5: Book.comment_count.desc(),  # 评论数量排序
    6: Book.yesterday_buy.desc()
}


@admin_book_bp.get('/')
@authorize("admin:book:main")
def main():
    return render_template('book/main.html')


@admin_book_bp.get('/data')
@authorize("admin:book:main")
def data():
    # 获取请求参数
    book_name = str_escape(request.args.get("book_name"))
    author_name = str_escape(request.args.get("author_name"))
    work_direction = str_escape(request.args.get("work_direction"))
    book_status = str_escape(request.args.get("book_status"))
    is_vip = str_escape(request.args.get("is_vip"))
    category = str_escape(request.args.get("category"))
    order_by = request.args.get("order_by", type=int)
    order_by = 0 if order_by is None or order_by not in order_by_type else order_by
    status = str_escape(request.args.get("status"))

    # 查询参数构造
    mf = ModelFilter()
    if book_name:
        mf.contains(field_name="book_name", value=book_name)
    if author_name:
        mf.contains(field_name="author_name", value=author_name)
    if work_direction:
        mf.exact(field_name="work_direction", value=work_direction)
    if book_status:
        mf.exact(field_name="book_status", value=book_status)
    if is_vip:
        mf.exact(field_name="is_vip", value=is_vip)
    if category:
        mf.exact(field_name="cat_id", value=category)
    if status:
        mf.exact(field_name="status", value=status)

    page_data = Book.query.filter(
        mf.get_filter(Book)
    ).order_by(
        order_by_type[order_by]
    ).layui_paginate()
    count = page_data.total

    res = [
        {
            'id': str(book.id),
            'book_name': book.book_name,
            'pic_url': book.pic_url,
            'work_direction': book.work_direction,
            'work_direction_name': DictType.translate(DictConsts.work_direction, book.work_direction),
            'cat_name': book.cat_name,
            'author_name': book.author_name,
            'status': book.status,
            'comment_enabled': book.comment_enabled,
            'book_status': book.book_status,
            'book_status_name': DictType.translate(DictConsts.book_status, book.book_status),
            'visit_count': book.visit_count,
            'word_count': book.word_count,
            'comment_count': book.comment_count,
            'yesterday_buy': book.yesterday_buy,
            'last_index_name': book.last_index_name,
            'last_index_update_time': book.last_index_update_time,
            'last_index_update_time_name': book.last_index_update_time.strftime(
                "%Y-%m-%d %H:%M:%S") if book.last_index_update_time else '',
            'is_vip': book.is_vip,
            'is_vip_name': DictType.translate(DictConsts.book_is_vip, book.is_vip),
            'create_time': book.create_time,
            'create_time_name': book.create_time.strftime("%Y-%m-%d %H:%M:%S") if book.create_time else ''
        } for book in page_data.items
    ]
    # 返回api
    return table_api(data=res, count=count, limit=request.args.get("limit", type=int),
                     page=request.args.get("page", type=int))


@admin_book_bp.get('/select_data')
@authorize("admin:book:main")
def select_data():
    # 获取请求参数
    keyword = str_escape(request.args.get("keyword"))
    keyword = keyword.strip() if keyword else keyword
    # 字数是否大于0，推荐小说的时候，字数必须大于0
    word_count_gt0 = request.args.get("word_count_gt0", type=int)

    # 查询参数构造
    filters = []
    if keyword:
        filters.append(
            or_(
                Book.book_name.ilike('%' + keyword + '%'),
                Book.author_name.ilike('%' + keyword + '%')
            )
        )
    if word_count_gt0:
        filters.append(Book.word_count > 0)

    page_data = db.session.query(
        Book.id, Book.book_name, Book.author_name
    ).filter(
        Book.status == 1,
        *filters
    ).order_by(
        Book.id.desc()
    ).layui_paginate()
    count = page_data.total

    res = [
        {
            'id': str(book.id),
            'book_name': book.book_name,
            'author_name': book.author_name,
        } for book in page_data.items
    ]
    # 返回api
    return table_api(data=res, count=count, limit=request.args.get("limit", type=int),
                     page=request.args.get("page", type=int))


def deep_func_runner(ids):
    for id_ in ids:
        AuthorIncome.query.filter_by(book_id=id_).delete()
        AuthorIncomeDetail.query.filter_by(book_id=id_).delete()
        BookComment.query.filter_by(book_id=id_).delete()
        BookSetting.query.filter_by(book_id=id_).delete()
        UserBookshelf.query.filter_by(book_id=id_).delete()
        UserBuyRecord.query.filter_by(book_id=id_).delete()
        UserReadHistory.query.filter_by(book_id=id_).delete()

        book_indexes = db.session.query(BookIndex.id).filter_by(book_id=id_).all()
        for book_index in book_indexes:
            model = BookContent.model(index_id=book_index.id)
            model.query.filter_by(index_id=book_index.id).delete()
        BookIndex.query.filter_by(book_id=id_).delete()

    db.session.commit()


@admin_book_bp.delete('/remove')
@authorize("admin:book:remove", log=True)
def delete():
    @copy_current_request_context
    def runner(id_list: List[int]):
        deep_func_runner(id_list)

    ids = request.form.getlist('ids[]')
    for id_ in ids:
        res = Book.query.filter_by(id=id_).delete()
        if not res:
            return fail_api(msg="删除失败")
    db.session.commit()

    job = threading.Thread(target=runner, args=(ids,))
    job.start()

    return success_api(msg="删除成功")


@admin_book_bp.get('/detail')
@authorize("admin:book:detail")
def detail():
    return render_template('book/detail_new.html')


@admin_book_bp.get('/get_detail')
@authorize("admin:book:detail")
def get_detail():
    id_ = request.args.get("id")
    book = Book.query.get(id_)
    res = {
        'id': str(book.id),
        'book_name': book.book_name,
        'pic_url': book.pic_url,
        'work_direction': book.work_direction,
        'work_direction_name': DictType.translate(DictConsts.work_direction, book.work_direction),
        'cat_name': book.cat_name,
        'author_name': book.author_name,
        'book_status': book.book_status,
        'status_name': DictType.translate(DictConsts.book_status, book.book_status),
        'visit_count': book.visit_count,
        'word_count': book.word_count,
        'comment_count': book.comment_count,
        'yesterday_buy': book.yesterday_buy,
        'last_index_name': book.last_index_name,
        'last_index_update_time': book.last_index_update_time,
        'last_index_update_time_name': book.last_index_update_time.strftime(
            "%Y-%m-%d %H:%M:%S") if book.last_index_update_time else '',
        'is_vip': book.is_vip,
        'is_vip_name': DictType.translate(DictConsts.book_is_vip, book.is_vip),
        'create_time': book.create_time,
        'create_time_name': book.create_time.strftime("%Y-%m-%d %H:%M:%S") if book.create_time else ''
    }
    return jsonify(code=0, data=res)


@admin_book_bp.put('/enable')
@authorize("admin:book:edit", log=True)
def enable():
    id_ = request.get_json(force=True).get('id')
    if id_:
        res = enable_status(model=Book, id=id_, field="status")
        if not res:
            return fail_api(msg="出错啦")
        return success_api(msg="上架成功")
    return fail_api(msg="数据错误")


# 禁用
@admin_book_bp.put('/disable')
@authorize("admin:book:edit", log=True)
def dis_enable():
    id_ = request.get_json(force=True).get('id')
    if id_:
        res = disable_status(model=Book, id=id_, field="status")
        if not res:
            return fail_api(msg="出错啦")
        return success_api(msg="下架成功")
    return fail_api(msg="数据错误")


# 打开评论区
@admin_book_bp.put('/openComment')
@authorize("admin:book:edit", log=True)
def open_comment():
    id_ = request.get_json(force=True).get('id')
    if id_:
        book = Book.query.get(id_)
        # 管理员不能替作家开启评论区
        # 作家关闭的评论区，管理员无权开启；管理员关闭的评论区，作家也无权开启
        if book.comment_enabled == 0:
            return fail_api(msg="作家关闭的评论区，管理员无权开启！")

        res = enable_status(model=Book, id=id_, field="comment_enabled")
        if not res:
            return fail_api(msg="出错啦")
        return success_api(msg="开启评论区成功")
    return fail_api(msg="数据错误")


# 关闭评论区
@admin_book_bp.put('/closeComment')
@authorize("admin:book:edit", log=True)
def close_comment():
    id_ = request.get_json(force=True).get('id')
    if id_:
        book = Book.query.get(id_)
        # 如果评论区此前已被作家关闭，则不能重复关闭
        if book.comment_enabled == 0:
            return success_api(msg="关闭评论区成功")

        res = disable_status(model=Book, id=id_, field="comment_enabled", disable=2)
        if not res:
            return fail_api(msg="出错啦")
        return success_api(msg="关闭评论区成功")
    return fail_api(msg="数据错误")


def do_clear_comments(ids):
    for id_ in ids:
        BookComment.query.filter_by(book_id=id_).delete()

    db.session.commit()


# 清空评论
@admin_book_bp.delete('/clearComments')
@authorize("admin:book:edit", log=True)
def clear_comments():
    @copy_current_request_context
    def runner(id_list: List[int]):
        do_clear_comments(id_list)

    ids = request.form.getlist('ids[]')
    job = threading.Thread(target=runner, args=(ids,))
    job.start()

    return success_api(msg="操作正在后台进行，您稍后可自行查看结果")
