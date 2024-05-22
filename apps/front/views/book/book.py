import time
from datetime import datetime

from flask import Blueprint, render_template, jsonify, request
from flask_jwt_extended import get_jwt_identity
from sqlalchemy import or_

from apps.front.dto.request import BookQueryModel
from apps.front.dto.response import BookQueryRespModel
from apps.front.exts.init_jwt import user_login_req
from apps.front.service import book_service
from pub.consts import RedisKey
from pub.curd import AutoModelTransfer
from pub.exts.init_siwadoc import siwa
from pub.exts.init_sqlalchemy import db
from pub.models.models_business import Book, BookCategory, BookIndex, BookContent, BookComment
from pub.utils.http_utils import table_api, fail_api
from pub.utils.redis_utils import Redis
from pub.utils.validate import str_escape

book_bp = Blueprint('book', __name__, url_prefix='/book')


def list_rank(_type: int, limit: int, redis_key: str):
    data = Redis.get(redis_key, default=None)
    if data:
        return jsonify(code=0, msg="", data=data)

    data = book_service.list_rank(_type, limit)

    json_data = AutoModelTransfer.model_2_json(model=Book, data=data)
    Redis.set_hot_key(redis_key, json_data)

    return jsonify(code=0, msg="", data=json_data)


@book_bp.route('/listBookSetting')
def list_book_setting():
    return render_template('index.html', navType=0)


@book_bp.route('/listClickRank')
def list_click_rank():
    return list_rank(0, 10, RedisKey.INDEX_CLICK_BANK_BOOK_KEY)


@book_bp.route('/listNewRank')
def list_new_rank():
    return list_rank(1, 10, RedisKey.INDEX_NEW_BOOK_KEY)


@book_bp.route('/listUpdateRank')
def list_update_rank():
    return list_rank(2, 23, RedisKey.INDEX_UPDATE_BOOK_KEY)


# 查询小说分类列表
@book_bp.route('/listBookCategory')
def list_book_category():
    data = db.session.query(
        BookCategory.id, BookCategory.name, BookCategory.work_direction
    ).order_by(
        BookCategory.sort.asc()
    ).all()
    return jsonify(code=0, msg="", data=AutoModelTransfer.model_2_dict(model=BookCategory, data=data))


order_search = {
    'update_time': Book.update_time.desc(),
    'word_count': Book.word_count.desc(),
    'last_index_update_time': Book.last_index_update_time.desc(),
    'visit_count': Book.visit_count.desc()
}


@book_bp.post('/searchByPage')
@siwa.doc(body=BookQueryModel, resp=BookQueryRespModel, summary="小说分页查询/搜索", tags=['小说'], group='小说')
def search_by_page(body: BookQueryModel):
    update_time_min = None
    print(body)
    if body.update_period:
        cur = int(round(time.time()))
        period = body.update_period * 24 * 3600
        time_ = cur - period
        update_time_min = time.localtime(time_)

    # 查询参数构造
    filters = []
    if body.work_direction:
        filters.append(Book.work_direction == body.work_direction)
    if body.cat_id:
        filters.append(Book.cat_id == body.cat_id)
    if body.is_vip:
        filters.append(Book.is_vip == body.is_vip)
    if body.book_status:
        filters.append(Book.book_status == body.book_status)
    if body.word_count_min:
        filters.append(Book.word_count >= body.word_count_min)
    if body.word_count_max:
        filters.append(Book.word_count <= body.word_count_max)
    if update_time_min:
        filters.append(Book.last_index_update_time >= update_time_min)
    if body.keyword:
        filters.append(or_(Book.book_name.contains(body.keyword), Book.author_name.contains(body.keyword)))
    if body.author_id:
        filters.append(Book.author_id == body.author_id)

    books = Book.query.filter(
        Book.word_count > 0,
        *filters
    ).order_by(
        order_search['update_time'] if not body.sort else order_search[body.sort]
    ).layui_paginate_from_body(body)
    # ).layui_paginate_from_json()
    count = books.total
    page = books.page
    limit = books.per_page

    return table_api(
        data=[
            {
                'id': str(book.id),
                'cat_id': book.cat_id,
                'cat_name': book.cat_name,
                'book_name': book.book_name,
                'author_id': book.author_id,
                'author_name': book.author_name,
                'word_count': book.word_count,
                'last_index_id': str(book.last_index_id),
                'last_index_name': book.last_index_name,
                'score': book.score,
                'pic_url': book.pic_url,
                'book_status': book.book_status,
                'last_index_update_time': book.last_index_update_time,
                'book_desc': book.book_desc
            } for book in books.items
        ],
        count=count, page=page, limit=limit)


@book_bp.get('/queryBookIndexAbout')
def query_book_index_about():
    book_id = request.args.get('bookId')
    last_book_index_id = request.args.get('lastBookIndexId')

    book_index_count = BookIndex.query.filter(
        BookIndex.book_id == book_id
    ).count()

    if last_book_index_id:
        model = BookContent.model(book_id=book_id, index_id=last_book_index_id)
        last_book_content = db.session.query(model.id, model.content).filter(
            model.index_id == last_book_index_id
        ).first()
        content = (
            last_book_content.content if len(last_book_content.content) <= 42 else last_book_content.content[0:42]) \
            if last_book_content else None
    else:
        content = None

    res_data = dict(
        bookIndexCount=book_index_count,
        lastBookContent=content
    )

    return jsonify(code=0, msg="", data=res_data)


@book_bp.post('/addVisitCount')
def add_visit_count():
    req_json = request.get_json(force=True)
    book_id = str_escape(req_json.get("bookId"))

    book = Book.query.get(book_id)
    book.visit_count += 1
    db.session.commit()

    return jsonify(code=0, msg="")


@book_bp.get('/listRank')
def get_books_ranking():
    type_ = request.args.get('type', type=int)
    limit = request.args.get('limit', type=int)

    data = book_service.list_rank(type_, limit)

    data = [
        {
            'id': str(book.id),
            'cat_id': str(book.cat_id),
            'cat_name': book.cat_name,
            'book_name': book.book_name,
            'last_index_id': str(book.last_index_id),
            'last_index_name': book.last_index_name,
            'author_id': book.author_id,
            'author_name': book.author_name,
            'pic_url': book.pic_url,
            'book_desc': book.book_desc,
            'word_count': book.word_count,
            'last_index_update_time': book.last_index_update_time
        } for book in data
    ]

    return jsonify(code=0, msg="", data=data)


@book_bp.post('/addBookComment')
@user_login_req
def add_book_comment():
    identity = get_jwt_identity()

    req_json = request.get_json(force=True)
    book_id = str_escape(req_json.get("bookId"))
    comment_content = str_escape(req_json.get("commentContent"))

    book = Book.query.get(book_id)
    if book.comment_enabled != 1:
        return fail_api(code=3001, msg='该书评论区已关闭！')

    count = BookComment.query.filter(
        BookComment.create_user_id == identity.get('id'),
        BookComment.book_id == book_id
    ).count()

    if count > 0:
        return fail_api(code=3001, msg='已评价过该书籍！')

    comment = BookComment(book_id=book_id, comment_content=comment_content, create_user_id=identity.get('id'),
                          create_time=datetime.now())

    book.comment_count += 1

    db.session.add(comment)
    db.session.add(book)
    db.session.commit()

    return jsonify(code=0, msg="")


@book_bp.get('/listCommentByPage')
def list_comment_by_page():
    book_id = request.args.get('bookId')
    page = request.args.get('page')
    page = int(page) if page else 1
    limit = request.args.get('limit')
    limit = int(limit) if limit else 10

    book = Book.query.get(book_id)
    if book.comment_enabled != 1:
        return table_api(data=[], count=0, page=page, limit=limit)

    return book_service.list_comment_by_page(None, book_id, page, limit)


@book_bp.get('/queryIndexList')
def query_index_list():
    book_id = int(request.args.get('bookId'))
    page = request.args.get('page')
    page = int(page) if page else 1
    limit = request.args.get('limit')
    limit = int(limit) if limit else 5
    order_by = request.args.get('orderBy')
    order_by = int(order_by) if order_by else 0

    return book_service.query_index_list(book_id, order_by, page, limit)
