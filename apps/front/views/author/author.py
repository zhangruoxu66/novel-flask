import re
from datetime import datetime

from flask import Blueprint, render_template, redirect, request, jsonify
from flask_jwt_extended import get_jwt_identity

from apps.front.exts.init_jwt import user_login_req
from apps.front.service import book_service
from pub.curd import AutoModelTransfer
from pub.exts.init_sqlalchemy import db
from pub.models.models_business import Author, AuthorCode, Book, AuthorIncomeDetail, AuthorIncome, BookIndex, \
    BookContent
from pub.utils import date_utils
from pub.utils.http_utils import table_api, fail_api, success_api
from pub.utils.validate import str_escape

author_bp = Blueprint('author', __name__, url_prefix='/author')


@author_bp.get('/index.html')
@user_login_req
def index():
    identity = get_jwt_identity()
    user_id = identity.get('id')

    count = Author.query.filter(Author.user_id == user_id).count()
    if count <= 0:
        return redirect('/author/register.html')

    return render_template('author/index.html')


# 作家注册
@author_bp.route('/register.html', methods=["GET", "POST"])
@user_login_req
def register():
    invite_code = request.args.get('inviteCode')  # 邀请码
    if invite_code:
        pen_name = request.args.get('penName')  # 笔名
        tel_phone = request.args.get('telPhone')  # 手机
        chat_account = request.args.get('chatAccount')  # 社交账号
        email = request.args.get('email')  # 邮箱
        work_direction = request.args.get('workDirection')  # 创作方向（男频/女频）

        cur_date = datetime.now()

        count = AuthorCode.query.filter(
            AuthorCode.invite_code == invite_code,
            AuthorCode.is_use == 0,
            AuthorCode.validity_time > cur_date
        ).count()

        author = Author(
            invite_code=invite_code,
            pen_name=pen_name,
            tel_phone=tel_phone,
            chat_account=chat_account,
            email=email,
            work_direction=work_direction
        )

        if count > 0:
            identity = get_jwt_identity()
            user_id = identity.get('id')
            author.user_id = user_id
            author.create_time = cur_date
            db.session.add(author)
            # 设置邀请码状态为已使用
            AuthorCode.query.filter(
                AuthorCode.invite_code == author.invite_code
            ).update({'is_use': 1})
            db.session.commit()
            return redirect('/author/index.html')

        return render_template('author/register.html', LabErr='邀请码无效！', author=author)

    return render_template('author/register.html', author=None)


@author_bp.get('/listBookByPage')
@user_login_req
def list_book_by_page():
    identity = get_jwt_identity()

    page = request.args.get('page')
    page = int(page) if page else 1
    limit = request.args.get('limit')
    limit = int(limit) if limit else 10

    author = db.session.query(
        Author.id, Author.pen_name, Author.status
    ).filter_by(
        user_id=identity.get('id')
    ).first()

    data = db.session.query(
        Book.id, Book.book_name, Book.pic_url, Book.cat_name, Book.visit_count, Book.yesterday_buy,
        Book.last_index_update_time, Book.update_time, Book.word_count, Book.last_index_name, Book.book_status,
        Book.comment_enabled
    ).filter(
        Book.author_id == author.id
    ).order_by(
        Book.create_time.desc()
    ).paginate(page=page, per_page=limit, error_out=False)

    return table_api(
        data=[
            {
                'id': str(book.id),
                'book_name': book.book_name,
                'pic_url': book.pic_url,
                'cat_name': book.cat_name,
                'visit_count': book.visit_count,
                'yesterday_buy': book.yesterday_buy,
                'last_index_update_time': date_utils.set_timezone(book.last_index_update_time),
                'update_time': date_utils.set_timezone(book.update_time),
                'word_count': book.word_count,
                'last_index_name': book.last_index_name,
                'book_status': book.book_status,
                'comment_enabled': book.comment_enabled,
            } for book in data.items
        ], count=data.total, page=page, limit=limit)


@author_bp.get('/author_income_detail.html')
@user_login_req
def author_income_detail():
    return render_template('author/author_income_detail.html')


@author_bp.get('/listIncomeDailyByPage')
@user_login_req
def list_income_daily_by_page():
    identity = get_jwt_identity()

    page = request.args.get('page')
    page = int(page) if page else 1
    limit = request.args.get('limit')
    limit = int(limit) if limit else 10
    book_id = request.args.get('bookId')
    book_id = int(book_id) if book_id else 0

    import parsedatetime
    calendar = parsedatetime.Calendar()

    start_time = request.args.get('startTime')
    if start_time:
        time_structure_start_time, parse_status_start_time = calendar.parse(start_time)
        start_time = datetime(*time_structure_start_time[:6])
    else:
        start_time = datetime(2020, 1, 1)
    end_time = request.args.get('endTime')
    if end_time:
        time_structure_end_time, parse_status_end_time = calendar.parse(end_time)
        end_time = datetime(*time_structure_end_time[:6])
    else:
        end_time = datetime(2040, 1, 1)

    data = db.session.query(
        AuthorIncomeDetail.income_date, AuthorIncomeDetail.income_account, AuthorIncomeDetail.income_count,
        AuthorIncomeDetail.income_number
    ).filter(
        AuthorIncomeDetail.user_id == identity.get('id')
        , AuthorIncomeDetail.book_id == book_id
        , AuthorIncomeDetail.income_date >= start_time
        , AuthorIncomeDetail.income_date <= end_time
    ).order_by(
        AuthorIncomeDetail.income_date.desc()
    ).paginate(page=page, per_page=limit, error_out=False)

    return table_api(data=AutoModelTransfer.model_2_dict(model=AuthorIncomeDetail, data=data.items), count=data.total,
                     page=page, limit=limit)


@author_bp.get('/author_income.html')
@user_login_req
def author_income():
    return render_template('author/author_income.html')


@author_bp.get('/listIncomeMonthByPage')
@user_login_req
def list_income_month_by_page():
    identity = get_jwt_identity()

    page = request.args.get('page')
    page = int(page) if page else 1
    limit = request.args.get('limit')
    limit = int(limit) if limit else 10
    book_id = request.args.get('bookId')
    book_id = int(book_id) if book_id else 0

    data = db.session.query(
        AuthorIncome.income_month, AuthorIncome.pre_tax_income, AuthorIncome.after_tax_income, AuthorIncome.pay_status,
        AuthorIncome.confirm_status
    ).filter(
        AuthorIncome.user_id == identity.get('id'),
        AuthorIncome.book_id == book_id
    ).order_by(
        AuthorIncome.income_month.desc()
    ).paginate(page=page, per_page=limit, error_out=False)

    return table_api(data=AutoModelTransfer.model_2_dict(model=AuthorIncome, data=data.items), count=data.total,
                     page=page, limit=limit)


@author_bp.get('/book_add.html')
@user_login_req
def book_add():
    return render_template('author/book_add.html')


def check_author(identity):
    author = db.session.query(Author.id, Author.pen_name, Author.status).filter(
        Author.user_id == identity.get('id')
    ).first()

    # 判断作者状态是否正常
    if author.status == 1:  # 封禁状态，不能发布小说
        return fail_api(code=4002, msg='作者状态异常，暂不能管理小说！')

    return author


@author_bp.post('/addBook')
@user_login_req
def add_book():
    identity = get_jwt_identity()

    req_json = request.get_json(force=True)
    work_direction = str_escape(req_json.get("workDirection"))
    cat_id = str_escape(req_json.get("catId"))
    cat_name = str_escape(req_json.get("catName"))
    book_name = str_escape(req_json.get("bookName"))
    pic_url = str_escape(req_json.get("picUrl"))
    book_desc = str_escape(req_json.get("bookDesc"))
    is_vip = str_escape(req_json.get("isVip"))
    comment_enabled = int(str_escape(req_json.get("commentEnabled")))

    book_desc = re.sub(r"(?<!\\)\n", "<br>", book_desc)
    book_desc = re.sub(r"(?<!\\)\s", "&nbsp;", book_desc)

    author = check_author(identity)

    book = Book()
    book.work_direction = work_direction
    book.cat_id = cat_id
    book.cat_name = cat_name
    book.book_name = book_name
    book.pic_url = pic_url
    book.book_desc = book_desc
    book.is_vip = is_vip
    book.comment_enabled = comment_enabled

    book_service.add_book(book, author.id, author.pen_name)

    return success_api()


@author_bp.post('/updateBookPic')
@user_login_req
def update_book_pic():
    req_json = request.get_json(force=True)
    book_id = str_escape(req_json.get("bookId"))
    book_pic = str_escape(req_json.get("bookPic"))

    Book.query.filter_by(id=book_id).update({'pic_url': book_pic, 'update_time': datetime.now()})
    db.session.commit()

    return success_api()


order_by = {
    1: BookIndex.index_num.desc()
}


@author_bp.get('/index_list.html')
@user_login_req
def index_list():
    return render_template('author/index_list.html')


@author_bp.get('/content_add.html')
@user_login_req
def content_add():
    return render_template('author/content_add.html')


@author_bp.post('/addBookContent')
@user_login_req
def add_book_content():
    identity = get_jwt_identity()
    author = check_author(identity)

    req_json = request.get_json(force=True)
    book_id = str_escape(req_json.get("bookId"))
    index_name = str_escape(req_json.get("indexName"))
    content = str_escape(req_json.get("content"))
    is_vip = str_escape(req_json.get("isVip"))

    content = re.sub(r"(?<!\\)\n", "<br>", content)
    content = re.sub(r"(?<!\\)\s", "&nbsp;", content)

    book_service.add_book_content(book_id, index_name, content, is_vip, author.id)

    return success_api()


@author_bp.get('/content_update.html')
@user_login_req
def content_update():
    return render_template('author/content_update.html')


@author_bp.get('/queryIndexContent/<int:index_id>')
@user_login_req
def query_index_content(index_id):
    identity = get_jwt_identity()
    author = check_author(identity)

    content = book_service.query_index_content(index_id, author.id).replace("<br>", "\n").replace("&nbsp;", " ")

    return jsonify(code=0, data=content)


@author_bp.post('/updateBookContent')
@user_login_req
def update_book_content():
    identity = get_jwt_identity()
    author = check_author(identity)

    req_json = request.get_json(force=True)
    index_id = str_escape(req_json.get("indexId"))
    index_name = str_escape(req_json.get("indexName"))
    content = str_escape(req_json.get("content"))

    content = re.sub(r"(?<!\\)\n", "<br>", content)
    content = re.sub(r"(?<!\\)\s", "&nbsp;", content)

    book_service.update_book_content(index_id, index_name, content, author.id)

    return success_api()


@author_bp.delete('/deleteIndex/<int:index_id>')
@user_login_req
def delete_index(index_id: int):
    identity = get_jwt_identity()
    author = check_author(identity)

    book_index = BookIndex.query.get(index_id)
    book = Book.query.get(book_index.book_id)

    word_count = book.word_count
    # 作者ID相同，表明该小说是登录用户发布，可以删除
    if book.author_id == author.id:
        BookIndex.query.filter_by(id=index_id).delete()
        model = BookContent.model(book_id=book.id, index_id=index_id)
        model.query.filter(model.index_id == index_id).delete()
        # 更新总字数
        word_count -= book_index.word_count
        # 更新最新章节
        last_index_id = None
        last_index_name = None
        last_index_update_time = None
        last_book_index = BookIndex.query.filter(
            BookIndex.book_id == book_index.book_id
        ).order_by(
            BookIndex.index_num.desc()
        ).first()
        if last_book_index:
            last_index_id = last_book_index.id
            last_index_name = last_book_index.index_name
            last_index_update_time = last_book_index.create_time
        # 更新小说主表信息
        book.word_count = word_count
        book.update_time = datetime.now()
        book.last_index_id = last_index_id
        book.last_index_name = last_index_name
        book.last_index_update_time = last_index_update_time
        db.session.add(book)

        db.session.commit()

    return success_api()


@author_bp.post('/updateBookStatus')
@user_login_req
def update_book_status():
    req_json = request.get_json(force=True)
    book_id = str_escape(req_json.get("bookId"))
    book_status = int(req_json.get("bookStatus"))

    book = Book.query.filter_by(id=book_id).update({"book_status": book_status})
    db.session.commit()

    if not book:
        return fail_api(msg="操作失败")
    return success_api(msg="操作成功")


@author_bp.post('/commentOpenClose')
@user_login_req
def comment_open_close():
    req_json = request.get_json(force=True)
    book_id = str_escape(req_json.get("bookId"))
    comment_enabled = int(req_json.get("commentEnabled"))

    # api校验：评论区状态只能是0或1
    if comment_enabled != 0 and comment_enabled != 1:
        return fail_api(code=4003, msg='错误的评论区状态！')

    # 管理员关闭的评论区，作家无权开启
    book = Book.query.get(book_id)
    if book.comment_enabled == 2:
        return fail_api(msg="该评论区已被管理员关闭，无权操作！")

    # book = Book.query.filter_by(id=book_id).update({"comment_enabled": comment_enabled})
    book.comment_enabled = comment_enabled
    db.session.add(book)
    db.session.commit()

    if not book:
        return fail_api(msg="操作失败")
    return success_api(msg="操作成功")
