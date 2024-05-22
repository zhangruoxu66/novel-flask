from datetime import datetime

from flask import Blueprint, render_template, jsonify
from sqlalchemy import text
from sqlalchemy.sql.functions import count
from sqlalchemy.sql.functions import func

from core.flask_redis_token.frt_utils import login_required, FRTUtils
from pub.exts.init_sqlalchemy import db
from pub.models.models_business import User, Author, Book, OrderPay
from pub.utils.date_utils import get_date_list

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


# 首页
@admin_bp.get('/')
@login_required
def index():
    user = FRTUtils.get_current_user()
    return render_template('admin/index.html', user=user)


# 控制台页面
@admin_bp.get('/welcome')
@login_required
def welcome():
    book_visit_count_rank_list = db.session.query(
        Book.book_name, Book.visit_count
    ).order_by(
        Book.visit_count.desc()
    ).offset(0).limit(8).all()

    author_visit_count_rank_list = db.session.query(
        Author.pen_name, func.sum(Book.visit_count).label('visit_count')
    ).join(
        Book, Author.id == Book.author_id
    ).group_by(
        Author.id
    ).order_by(
        text('visit_count desc')
    ).offset(0).limit(8).all()

    return render_template('admin/console/console.html', book_visit_count_rank_list=book_visit_count_rank_list,
                           author_visit_count_rank_list=author_visit_count_rank_list)


@admin_bp.get('/stat/countSta')
@login_required
def count_sta():
    user_count = User.query.count()
    author_count = Author.query.count()
    book_count = Book.query.count()
    order_count = OrderPay.query.count()
    return jsonify(code=0, user_count=user_count, author_count=author_count, book_count=book_count,
                   order_count=order_count)


@admin_bp.get('/stat/tableSta')
@login_required
def table_sta():
    date_list = get_date_list(7, datetime.now())
    min_date = datetime.strptime(date_list[0], '%Y-%m-%d').date()

    user_table_sta = db.session.query(
        func.date_format(User.create_time, '%Y-%m-%d').label('staDate'),
        count(1).label('userCount')
    ).filter(
        User.create_time >= min_date
    ).group_by(
        'staDate'
    ).order_by(
        'staDate'
    ).all()
    user_table_sta = {x[0]: x[1] for x in user_table_sta}

    book_table_sta = db.session.query(
        func.date_format(Book.create_time, '%Y-%m-%d').label('staDate'),
        count(1).label('bookCount')
    ).filter(
        Book.create_time >= min_date
    ).group_by(
        'staDate'
    ).order_by(
        'staDate'
    ).all()
    book_table_sta = {x[0]: x[1] for x in book_table_sta}

    author_table_sta = db.session.query(
        func.date_format(Author.create_time, '%Y-%m-%d').label('staDate'),
        count(1).label('authorCount')
    ).filter(
        Author.create_time >= min_date
    ).group_by(
        'staDate'
    ).order_by(
        'staDate'
    ).all()
    author_table_sta = {x[0]: x[1] for x in author_table_sta}

    order_table_sta = db.session.query(
        func.date_format(OrderPay.create_time, '%Y-%m-%d').label('staDate'),
        count(1).label('orderCount')
    ).filter(
        OrderPay.create_time >= min_date
    ).group_by(
        'staDate'
    ).order_by(
        'staDate'
    ).all()
    order_table_sta = {x[0]: x[1] for x in order_table_sta}

    return jsonify(code=0, dateList=date_list, userTableSta=user_table_sta, bookTableSta=book_table_sta,
                   authorTableSta=author_table_sta, orderTableSta=order_table_sta)
