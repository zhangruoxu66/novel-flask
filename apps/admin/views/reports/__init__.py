from datetime import datetime

import parsedatetime
from flask import Blueprint, render_template, request
from sqlalchemy import func, case, text, literal_column

from pub.consts.dict_consts import DictConsts
from pub.exts.init_sqlalchemy import db
from pub.models.models_business import OrderPay, Author, UserBuyRecord, Book
from pub.models.models_system import DictType
from pub.utils.http_utils import table_api
from pub.utils.rights import authorize
from pub.utils.validate import str_escape

reports_bp = Blueprint('reports', __name__, url_prefix='/admin/report')


def register_reports_views(app):
    app.register_blueprint(reports_bp)


@reports_bp.get('/recharge/')
@authorize("admin:report:recharge")
def recharge():
    return render_template('reports/recharge.html')


@reports_bp.get('/recharge/data')
@authorize("admin:report:recharge")
def recharge_data():
    # 获取请求参数
    start_date = str_escape(request.args.get('start_date'))
    end_date = str_escape(request.args.get('end_date'))
    calendar = parsedatetime.Calendar()

    # 查询参数构造
    filters = []
    if start_date:
        time_structure_start_time, parse_status_start_time = calendar.parse(start_date)
        start_date = datetime(*time_structure_start_time[:6])
        # filters.append(func.date_format(OrderPay.create_time, '%Y-%m-%d') >= start_date)
        filters.append(OrderPay.create_time >= start_date)
    if end_date:
        time_structure_end_time, parse_status_end_time = calendar.parse(end_date)
        end_date = datetime(*time_structure_end_time[:6])
        filters.append(func.date_format(OrderPay.create_time, '%Y-%m-%d') <= end_date)

    page_data = db.session.query(
        func.date_format(OrderPay.create_time, '%Y-%m-%d').label('sta_date'),
        func.sum(case((OrderPay.pay_status == 1, 1), else_=0)).label("succeed_count"),
        func.sum(case((OrderPay.pay_status == 0, 1), else_=0)).label("failed_count"),
        func.sum(case((OrderPay.pay_status == 2, 1), else_=0)).label("waiting_count"),
        func.sum(case((OrderPay.pay_status == 1, OrderPay.total_amount), else_=0)).label("succeed_amount"),
        func.sum(case((OrderPay.pay_status == 0, OrderPay.total_amount), else_=0)).label("failed_amount"),
        func.sum(case((OrderPay.pay_status == 2, OrderPay.total_amount), else_=0)).label("waiting_amount"),
    ).filter(
        *filters
    ).group_by(
        'sta_date'
    ).order_by(
        text('sta_date desc')
    ).layui_paginate()
    count = page_data.total

    res = [
        {
            'sta_date': data.sta_date,
            'succeed_count': data.succeed_count,
            'failed_count': data.failed_count,
            'waiting_count': data.waiting_count,
            'succeed_amount': data.succeed_amount,
            'failed_amount': data.failed_amount,
            'waiting_amount': data.waiting_amount,
        } for data in page_data.items
    ]

    return table_api(data=res, count=count)


@reports_bp.get('/income/')
@authorize("admin:report:income")
def income():
    return render_template('reports/income.html')


@reports_bp.get('/income/data/author')
@authorize("admin:report:income")
def author_income_data():
    # 获取请求参数
    author_name = str_escape(request.args.get('author_name'))

    # 查询参数构造
    filters = []
    if author_name:
        filters.append(Author.pen_name.contains(author_name))

    page_data = db.session.query(
        Author.pen_name,
        func.sum(UserBuyRecord.buy_amount).label('total_amount'),
    ).outerjoin(
        Book, UserBuyRecord.book_id == Book.id
    ).outerjoin(
        Author, Book.author_id == Author.id
    ).filter(
        *filters
    ).group_by(
        Author.pen_name
    ).order_by(
        text('total_amount desc')
    ).layui_paginate()
    count = page_data.total

    res = [
        {
            'author_name': data.pen_name,
            'total_amount': data.total_amount,
        } for data in page_data.items
    ]

    return table_api(data=res, count=count)


@reports_bp.get('/income/data/book')
@authorize("admin:report:income")
def book_income_data():
    # 获取请求参数
    author_name = str_escape(request.args.get('author_name'))
    book_name = str_escape(request.args.get('book_name'))
    work_direction = str_escape(request.args.get('work_direction'))
    category = str_escape(request.args.get('category'))

    # 查询参数构造
    filters = []
    if author_name:
        filters.append(Book.author_name.contains(author_name))
    if book_name:
        filters.append(Book.book_name.contains(book_name))
    if work_direction:
        filters.append(Book.work_direction == work_direction)
    if category:
        filters.append(Book.cat_id == category)
    # filters.append(Book.is_vip == 1)

    page_data = db.session.query(
        Book.id, Book.book_name, Book.work_direction, Book.cat_id, Book.cat_name, Book.author_id, Book.author_name,
        func.sum(UserBuyRecord.buy_amount).label('total_amount'),
    ).outerjoin(
        Book, UserBuyRecord.book_id == Book.id
    ).filter(
        *filters
    ).group_by(
        Book.id, Book.book_name, Book.work_direction, Book.cat_id, Book.cat_name, Book.author_id, Book.author_name,
    ).having(
        text('total_amount > 0')
    ).order_by(
        text('total_amount desc')
    ).layui_paginate()
    count = page_data.total

    res = [
        {
            'book_id': data.id,
            'book_name': data.book_name,
            'work_direction': data.work_direction,
            'work_direction_name': DictType.translate(DictConsts.work_direction, data.work_direction),
            'cat_id': data.cat_id,
            'cat_name': data.cat_name,
            'author_id': data.author_id,
            'author_name': data.author_name,
            'total_amount': data.total_amount,
        } for data in page_data.items
    ]

    return table_api(data=res, count=count)


@reports_bp.get('/book_statistics/')
@authorize("admin:report:book_statistics")
def book_statistics():
    return render_template('reports/book_statistics.html')


@reports_bp.get('/book_statistics/data')
@authorize("admin:report:book_statistics")
def book_statistics_data():
    page = request.args.get("page", type=int)
    limit = request.args.get("limit", type=int)
    start = (page - 1) * limit

    # query_obj = text(
    #     f'select a.* from '
    #     f'('
    #
    #     f'('
    #     f'select '
    #     f'0 as statistics_type, '
    #     f'"" as work_direction, '
    #     f'"" as cat_name, '
    #     f'count(*) as total_book_count, '
    #     f'sum(word_count) as total_word_count, '
    #     f'sum(visit_count) as total_visit_count, '
    #     f'sum(comment_count) as total_comment_count '
    #     f'from novel_flask.book '
    #     f') '
    #
    #     f'union all '
    #
    #     f'('
    #     f'select '
    #     f'1 as statistics_type, '
    #     f'"男频" as work_direction, '
    #     f'"" as cat_name, '
    #     f'count(*) as total_book_count, '
    #     f'sum(word_count) as total_word_count, '
    #     f'sum(visit_count) as total_visit_count, '
    #     f'sum(comment_count) as total_comment_count '
    #     f'from novel_flask.book '
    #     f'where work_direction = 0 '
    #     f') '
    #
    #     f'union all '
    #
    #     f'('
    #     f'select '
    #     f'3 as statistics_type, '
    #     f'"男频" as work_direction, '
    #     f'cat_name, '
    #     f'count(*) as total_book_count, '
    #     f'sum(word_count) as total_word_count, '
    #     f'sum(visit_count) as total_visit_count, '
    #     f'sum(comment_count) as total_comment_count '
    #     f'from novel_flask.book '
    #     f'where work_direction = 0 '
    #     f'group by cat_id, cat_name '
    #     f'order by cat_id '
    #     f') '
    #
    #     f'union all '
    #
    #     f'('
    #     f'select '
    #     f'2 as statistics_type, '
    #     f'"女频" as work_direction, '
    #     f'"" as cat_name, '
    #     f'count(*) as total_book_count, '
    #     f'sum(word_count) as total_word_count, '
    #     f'sum(visit_count) as total_visit_count, '
    #     f'sum(comment_count) as total_comment_count '
    #     f'from novel_flask.book '
    #     f'where work_direction = 1 '
    #     f') '
    #
    #     f'union all '
    #
    #     f'('
    #     f'select '
    #     f'4 as statistics_type, '
    #     f'"女频" as work_direction, '
    #     f'cat_name, '
    #     f'count(*) as total_book_count, '
    #     f'sum(word_count) as total_word_count, '
    #     f'sum(visit_count) as total_visit_count, '
    #     f'sum(comment_count) as total_comment_count '
    #     f'from novel_flask.book '
    #     f'where work_direction = 1 '
    #     f'group by cat_id, cat_name '
    #     f'order by cat_id '
    #     f') '
    #
    #     f') a '
    #     f'limit {start}, {limit}'
    # )
    # page_data = db.session.execute(query_obj).fetchall()

    # 基本统计（所有书籍）
    base_statistics = db.session.query(
        literal_column("0").label("statistics_type"),
        literal_column("''").label("work_direction"),
        literal_column("''").label("cat_name"),
        func.count(Book.id).label("total_book_count"),
        func.sum(Book.word_count).label("total_word_count"),
        func.sum(Book.visit_count).label("total_visit_count"),
        func.sum(Book.comment_count).label("total_comment_count")
    ).select_from(Book)

    # 男频书籍统计
    male_statistics = db.session.query(
        literal_column("1").label("statistics_type"),
        literal_column("'男频'").label("work_direction"),
        literal_column("''").label("cat_name"),
        func.count(Book.id).label("total_book_count"),
        func.sum(Book.word_count).label("total_word_count"),
        func.sum(Book.visit_count).label("total_visit_count"),
        func.sum(Book.comment_count).label("total_comment_count")
    ).select_from(Book).filter(Book.work_direction == 0)

    # 男频分类书籍统计
    male_cat_statistics = db.session.query(
        literal_column("3").label("statistics_type"),
        literal_column("'男频'").label("work_direction"),
        Book.cat_name.label("cat_name"),
        func.count(Book.id).label("total_book_count"),
        func.sum(Book.word_count).label("total_word_count"),
        func.sum(Book.visit_count).label("total_visit_count"),
        func.sum(Book.comment_count).label("total_comment_count")
    ).select_from(Book).filter(Book.work_direction == 0).group_by(Book.cat_id, Book.cat_name).order_by(Book.cat_id)

    # 女频书籍统计
    female_statistics = db.session.query(
        literal_column("2").label("statistics_type"),
        literal_column("'女频'").label("work_direction"),
        literal_column("''").label("cat_name"),
        func.count(Book.id).label("total_book_count"),
        func.sum(Book.word_count).label("total_word_count"),
        func.sum(Book.visit_count).label("total_visit_count"),
        func.sum(Book.comment_count).label("total_comment_count")
    ).select_from(Book).filter(Book.work_direction == 1)

    # 女频分类书籍统计
    female_cat_statistics = db.session.query(
        literal_column("4").label("statistics_type"),
        literal_column("'女频'").label("work_direction"),
        Book.cat_name.label("cat_name"),
        func.count(Book.id).label("total_book_count"),
        func.sum(Book.word_count).label("total_word_count"),
        func.sum(Book.visit_count).label("total_visit_count"),
        func.sum(Book.comment_count).label("total_comment_count")
    ).select_from(Book).filter(Book.work_direction == 1).group_by(Book.cat_id, Book.cat_name).order_by(Book.cat_id)

    # 将所有查询组合成一个联合查询
    union_all_query = base_statistics.union_all(
        male_statistics,
        male_cat_statistics,
        female_statistics,
        female_cat_statistics
    )

    page_data = union_all_query.offset(start).limit(limit).all()

    res = [
        {
            'statistics_type': data.statistics_type,
            'work_direction': data.work_direction,
            'cat_name': data.cat_name,
            'total_book_count': data.total_book_count,
            'total_word_count': data.total_word_count,
            'total_visit_count': data.total_visit_count,
            'total_comment_count': data.total_comment_count,
        } for data in page_data
    ]

    return table_api(data=res, count=len(page_data))
