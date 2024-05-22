from datetime import datetime

from flask import Blueprint, render_template, request, jsonify, current_app
from flask_jwt_extended import get_jwt_identity, jwt_required, set_refresh_cookies
from sqlalchemy import exists, and_, func

from apps.front.exts.init_jwt import user_login_req
from apps.front.logic.user_logic import UserLogic
from apps.front.service import book_service, jwt_service
from pub.consts import RedisKey
from pub.curd import AutoModelTransfer
from pub.exts.init_sqlalchemy import db
from pub.models.models_business import User, UserBookshelf, UserReadHistory, Book, UserFeedback, BookIndex, \
    UserBuyRecord, AuthorFollow, Author
from pub.utils import ip_utils, date_utils
from pub.utils.http_utils import fail_api, success_api, table_api
from pub.utils.redis_utils import Redis
from pub.utils.string_utils import protect_mobile
from pub.utils.validate import str_escape

user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.get('/register.html')
def register():
    return render_template('user/register.html')


@user_bp.post('/register')
def save_user():
    req_json = request.get_json(force=True)
    username = str_escape(req_json.get("username"))
    password = str_escape(req_json.get("password"))
    vel_code = str_escape(req_json.get("velCode"))

    if vel_code != Redis.get(RedisKey.VALIDATE_CODE_CACHE + ':' + ip_utils.get_real_ip()):
        return fail_api(code=1002, msg='验证码错误！')

    count = User.query.filter_by(username=username).count()
    if count > 0:
        return fail_api(code=1003, msg='该手机号已注册！')

    cur_date = datetime.now()
    user = User(
        username=username,
        nick_name=protect_mobile(username),
        create_time=cur_date,
        update_time=cur_date
    )
    user.set_password(password)

    db.session.add(user)
    db.session.flush()
    db.session.commit()

    identity = dict(
        id=user.id,
        username=user.username,
        nick_name=user.nick_name
    )

    tokens = jwt_service.gen_all_cookie(identity)
    response = jsonify(
        success=True, code=0, msg='注册成功',
        access_token=tokens.access_token, csrf_token=tokens.csrf_token,
        access_refresh_token=tokens.access_refresh_token, csrf_refresh_token=tokens.csrf_refresh_token
    )
    set_refresh_cookies(
        response, tokens.access_refresh_token, max_age=current_app.config['JWT_SESSION_COOKIE_MAX_AGE']
    )
    return response


# 使用刷新JWT来获取普通JWT
@user_bp.post('/refreshToken')
@jwt_required(refresh=True)
def refresh_token():
    identity = get_jwt_identity()
    new_tokens = jwt_service.gen_all_cookie(identity)
    response = jsonify(
        code=0,
        access_token=new_tokens.access_token, csrf_token=new_tokens.csrf_token,
        access_refresh_token=new_tokens.access_refresh_token, csrf_refresh_token=new_tokens.csrf_refresh_token,
        nickName=identity.get('nick_name')
    )
    set_refresh_cookies(
        response, new_tokens.access_refresh_token, max_age=current_app.config['JWT_SESSION_COOKIE_MAX_AGE']
    )
    return response


@user_bp.get('/login.html')
def to_login():
    return render_template('user/login.html')


@user_bp.get('/test')
@user_login_req
def test():
    return 'ok'


@user_bp.post('/login')
def login():
    req_json = request.get_json(force=True)
    username = str_escape(req_json.get("username"))
    password = str_escape(req_json.get("password"))

    if not username or not password:
        return fail_api(msg="用户名和密码不能为空")

    user = User.query.filter_by(username=username).first()

    if not user:
        return fail_api(code=1004, msg='用户不存在！')

    if not user.validate_password(password):
        return fail_api(code=1004, msg='密码错误！')

    identity = dict(
        id=user.id,
        username=user.username,
        nick_name=user.nick_name
    )

    tokens = jwt_service.gen_all_cookie(identity)

    response = jsonify(
        success=True, code=0, msg='注册成功',
        access_token=tokens.access_token, csrf_token=tokens.csrf_token,
        access_refresh_token=tokens.access_refresh_token, csrf_refresh_token=tokens.csrf_refresh_token,
        nick_name=user.nick_name
    )
    set_refresh_cookies(
        response, tokens.access_refresh_token, max_age=current_app.config['JWT_SESSION_COOKIE_MAX_AGE']
    )
    return response


@user_bp.get('/queryIsInShelf')
@jwt_required(optional=True)
def query_is_in_shelf():
    identity = get_jwt_identity()
    if not identity or not identity.get('id'):
        return fail_api(code=1001, msg='未登录或登录失效！')

    identity = get_jwt_identity()
    user_id = identity.get('id')

    book_id = request.args.get("bookId")

    count = UserBookshelf.query.filter(
        UserBookshelf.user_id == user_id,
        UserBookshelf.book_id == book_id
    ).count()

    return jsonify(success=True, code=0, data=count > 0)


@user_bp.post('/addReadHistory')
@user_login_req
def add_read_history():
    req_json = request.get_json(force=True)
    book_id = str_escape(req_json.get("bookId"))
    pre_content_id = str_escape(req_json.get("preContentId"))

    identity = get_jwt_identity()
    user_id = identity.get('id')

    # 删除该书以前的历史记录
    UserReadHistory.query.filter(
        UserReadHistory.book_id == book_id,
        UserReadHistory.user_id == user_id
    ).delete()

    # 插入该书新的历史记录
    cur_date = datetime.now()
    user_read_history = UserReadHistory(
        book_id=book_id,
        user_id=user_id,
        pre_content_id=pre_content_id,
        create_time=cur_date,
        update_time=cur_date
    )
    db.session.add(user_read_history)

    # 更新书架的阅读历史
    UserBookshelf.query.filter(
        UserBookshelf.user_id == user_id,
        UserBookshelf.book_id == book_id
    ).update({"pre_content_id": pre_content_id, "update_time": cur_date})

    db.session.commit()

    return success_api()


@user_bp.get('/userinfo.html')
@user_login_req
def userinfo():
    return render_template('user/userinfo.html', li_userinfo=True)


@user_bp.get('/userInfo')
@user_login_req
def get_userinfo():
    identity = get_jwt_identity()
    user_info = db.session.query(
        User.username, User.nick_name, User.user_photo, User.account_balance, User.user_sex
    ).filter(
        User.id == identity.get('id')
    ).first()
    return jsonify(success=True, code=0,
                   data=AutoModelTransfer.model_2_dict(model=User, data=user_info, many=False))


@user_bp.get('/listBookShelfByPage')
@user_login_req
def list_book_shelf_by_page():
    identity = get_jwt_identity()

    page = request.args.get('page')
    page = int(page) if page else 1
    limit = request.args.get('limit')
    limit = int(limit) if limit else 10

    data = db.session.query(
        UserBookshelf, Book
    ).join(
        Book, UserBookshelf.book_id == Book.id
    ).filter(
        UserBookshelf.user_id == identity.get('id')
    ).order_by(
        UserBookshelf.create_time.desc()
    ).paginate(page=page, per_page=limit, error_out=False)

    return table_api(
        data=[
            {
                'book_id': str(shelf.book_id),
                'pre_content_id': str(shelf.pre_content_id),
                'book_name': book.book_name,
                'cat_id': book.cat_id,
                'cat_name': book.cat_name,
                'last_index_id': str(book.last_index_id),
                'last_index_name': book.last_index_name,
                'last_index_update_time': date_utils.set_timezone(book.last_index_update_time)
            } for shelf, book in data.items
        ],
        count=data.total, page=page, limit=limit)


@user_bp.get('/listReadHistoryByPage')
@user_login_req
def list_read_history_by_page():
    identity = get_jwt_identity()

    page = request.args.get('page')
    page = int(page) if page else 1
    limit = request.args.get('limit')
    limit = int(limit) if limit else 10

    data = db.session.query(
        UserReadHistory, Book
    ).join(
        Book, UserReadHistory.book_id == Book.id
    ).filter(
        UserReadHistory.user_id == identity.get('id')
    ).order_by(
        UserReadHistory.create_time.desc()
    ).paginate(page=page, per_page=limit, error_out=False)

    return table_api(
        data=[
            {
                'book_id': str(history.book_id),
                'pre_content_id': str(history.pre_content_id),
                'book_name': book.book_name,
                'cat_id': book.cat_id,
                'cat_name': book.cat_name,
                'last_index_id': str(book.last_index_id),
                'last_index_name': book.last_index_name,
                'last_index_update_time': date_utils.set_timezone(book.last_index_update_time)
            } for history, book in data.items
        ],
        count=data.total, page=page, limit=limit)


@user_bp.get('/favorites.html')
@user_login_req
def favorites():
    return render_template('user/favorites.html', li_favorites=True)


@user_bp.get('/read_history.html')
@user_login_req
def read_history():
    return render_template('user/read_history.html')


@user_bp.get('/comment.html')
@user_login_req
def comment():
    return render_template('user/comment.html', li_comment=True)


@user_bp.get('/listCommentByPage')
@user_login_req
def list_comment_by_page():
    identity = get_jwt_identity()

    page = request.args.get('page')
    page = int(page) if page else 1
    limit = request.args.get('limit')
    limit = int(limit) if limit else 10

    return book_service.list_comment_by_page(identity.get('id'), None, page, limit)


@user_bp.get('/feedback_list.html')
@user_login_req
def feedback_list():
    return render_template('user/feedback_list.html', li_feedback_list=True)


@user_bp.get('/listUserFeedBackByPage')
@user_login_req
def list_user_feed_back_by_page():
    identity = get_jwt_identity()

    page = request.args.get('page')
    page = int(page) if page else 1
    limit = request.args.get('limit')
    limit = int(limit) if limit else 10

    data = db.session.query(
        UserFeedback.content, UserFeedback.create_time
    ).filter(
        UserFeedback.user_id == identity.get('id')
    ).order_by(
        UserFeedback.id.desc()
    ).paginate(page=page, per_page=limit, error_out=False)

    return table_api(
        data=AutoModelTransfer.model_2_dict(model=UserFeedback, data=data.items),
        count=data.total, page=page, limit=limit
    )


@user_bp.get('/feedback.html')
@user_login_req
def feedback():
    return render_template('user/feedback.html')


@user_bp.post('/addFeedBack')
@user_login_req
def add_feed_back():
    identity = get_jwt_identity()
    req_json = request.get_json(force=True)
    content = str_escape(req_json.get("content"))

    feed_back = UserFeedback(
        user_id=identity.get('id'),
        content=content,
        create_time=datetime.now()
    )
    db.session.add(feed_back)
    db.session.commit()

    return success_api()


@user_bp.get('/buy_record.html')
@user_login_req
def buy_record():
    return render_template('user/buy_record.html', li_buy_record=True)


@user_bp.get('/listBuyRecordByPage')
@user_login_req
def list_buy_record_by_page():
    identity = get_jwt_identity()

    page = request.args.get('page')
    page = int(page) if page else 1
    limit = request.args.get('limit')
    limit = int(limit) if limit else 10

    data = db.session.query(
        UserBuyRecord.book_id, UserBuyRecord.book_name, UserBuyRecord.book_index_id, UserBuyRecord.book_index_name,
        UserBuyRecord.buy_amount, UserBuyRecord.create_time
    ).filter(
        UserBuyRecord.user_id == identity.get('id')
    ).order_by(
        UserBuyRecord.create_time.desc()
    ).paginate(page=page, per_page=limit, error_out=False)

    return table_api(
        data=[
            {
                'book_id': str(record.book_id),
                'book_name': record.book_name,
                'book_index_id': str(record.book_index_id),
                'book_index_name': record.book_index_name,
                'buy_amount': record.buy_amount,
                'create_time': date_utils.set_timezone(record.create_time)
            } for record in data.items
        ],
        count=data.total, page=page, limit=limit)


@user_bp.get('/setup.html')
@user_login_req
def setup():
    return render_template('user/setup.html', li_setup=True)


@user_bp.get('/set_<string:html>.html')
@user_login_req
def set_name(html: str):
    return render_template(f'user/set_{html}.html', li_setup=True)


@user_bp.post('/updateUserInfo')
@user_login_req
def update_user_info():
    identity = get_jwt_identity()

    req_json = request.get_json(force=True)
    nick_name = str_escape(req_json.get("nickName"))
    user_sex = str_escape(req_json.get("userSex"))
    user_photo = str_escape(req_json.get("userPhoto"))

    user = User.query.get(identity.get('id'))
    if nick_name:
        user.nick_name = nick_name
    if user_sex:
        user.user_sex = user_sex
    if user_photo:
        user.user_photo = user_photo

    db.session.add(user)
    db.session.commit()

    identity = dict(
        id=user.id,
        username=user.username,
        nick_name=user.nick_name
    )

    tokens = jwt_service.gen_all_cookie(identity)

    response = jsonify(
        success=True, code=0, msg='更新成功',
        access_token=tokens.access_token, csrf_token=tokens.csrf_token,
        access_refresh_token=tokens.access_refresh_token, csrf_refresh_token=tokens.csrf_refresh_token
    )
    set_refresh_cookies(response, tokens.access_refresh_token, max_age=current_app.config['JWT_SESSION_COOKIE_MAX_AGE'])

    return response


@user_bp.post('/updatePassword')
@user_login_req
def update_password():
    identity = get_jwt_identity()

    req_json = request.get_json(force=True)
    old_password = str_escape(req_json.get("oldPassword"))
    new_password1 = str_escape(req_json.get("newPassword1"))
    new_password2 = str_escape(req_json.get("newPassword2"))

    if not (new_password1 and new_password1 == new_password2):
        return fail_api(code=1005, msg='两次输入的新密码不匹配!')

    user = User.query.get(identity.get('id'))

    if not user.validate_password(old_password):
        return fail_api(code=1006, msg='旧密码不匹配!')

    user.set_password(new_password1)
    db.session.add(user)
    db.session.commit()

    return success_api()


@user_bp.post('/addToBookShelf')
@user_login_req
def add_to_book_shelf():
    identity = get_jwt_identity()

    req_json = request.get_json(force=True)
    book_id = str_escape(req_json.get("bookId"))
    pre_content_id = str_escape(req_json.get("preContentId"))

    count = UserBookshelf.query.filter_by(user_id=identity.get('id'), book_id=book_id).count()
    if count <= 0:
        user_book_shelf = UserBookshelf()
        user_book_shelf.user_id = identity.get('id')
        user_book_shelf.book_id = book_id
        user_book_shelf.pre_content_id = pre_content_id
        user_book_shelf.create_time = datetime.now()
        db.session.add(user_book_shelf)
        db.session.commit()

    return success_api()


# 购买单章
@user_bp.post('/buyBookIndex')
@user_login_req
def buy_book_index():
    identity = get_jwt_identity()

    req_json = request.get_json(force=True)
    book_id = str_escape(req_json.get("bookId"))
    book_name = str_escape(req_json.get("bookName"))
    book_index_id = str_escape(req_json.get("bookIndexId"))
    book_index_name = str_escape(req_json.get("bookIndexName"))

    book_index = BookIndex.query.get(book_index_id)
    if book_index.is_vip != 1:
        return fail_api(code=1007, msg='非付费章节无需购买！')
    book_price = book_index.book_price

    user = User.query.get(identity.get('id'))
    if user.account_balance < book_price:
        # 余额不足
        return fail_api(code=1007, msg='用户余额不足')

    connection = db.get_engine(bind_key='ds1').connect()
    try:

        if not UserLogic.buy_one_index(connection, identity.get("id"), book_id, book_name, book_price, book_index_id,
                                       book_index_name, datetime.now().strftime("%Y-%m-%d %H:%M:%S")):
            # return fail_api()
            return fail_api(msg='余额不足')

        db.session.commit()
        connection.commit()
    except Exception as e:
        db.session.rollback()
        connection.rollback()
        raise e
    finally:
        db.session.close()
        connection.close()

    return success_api()


# 批量购买章节
@user_bp.post('/batchBuyBookIndex')
@user_login_req
def batch_buy_book_indexes():
    identity = get_jwt_identity()

    req_json = request.get_json(force=True)
    book_id = str_escape(req_json.get("bookId"))
    book_name = str_escape(req_json.get("bookName"))
    begin_index_id = req_json.get("beginBookIndexId")
    buy_count = req_json.get("buyCount")

    # total_amount_sql = (
    #     f'select sum(a.book_price) as total_amount '
    #     f'from novel_flask.book_index a '
    #     f'where a.book_id = {book_id} '
    #     f'and a.is_vip = 1 '
    #     f'and a.id >= {begin_index_id} '
    #     f'and not exists '
    #     f'('
    #     f'select 1 from novel_flask.user_buy_record b '
    #     f'where b.user_id = {identity.get("id")} and b.book_index_id = a.id'
    #     f') '
    # )
    # if buy_count > 0:
    #     total_amount_sql += f'limit {buy_count} '
    # total_amount = db.session.execute(text(
    #     total_amount_sql
    # )).fetchone().total_amount

    # 创建一个子查询，用于检查用户是否已经购买了这本书
    subquery = exists().where(and_(
        UserBuyRecord.user_id == identity.get("id"),  # 用户ID为2
        UserBuyRecord.book_index_id == BookIndex.id
    ))
    # 主查询，使用func.sum来求和
    total_amount_query = BookIndex.query.with_entities(func.sum(BookIndex.book_price).label('total_amount')).filter(
        and_(
            BookIndex.book_id == book_id,  # 使用参数化的book_id
            BookIndex.is_vip == 1,
            BookIndex.id >= begin_index_id,
            ~subquery  # 使用~来表示NOT EXISTS
        )
    )
    if buy_count > 0:
        total_amount_query = total_amount_query.limit(buy_count)
    total_amount = total_amount_query.scalar()  # scalar()方法用于获取单个结果值

    user = User.query.get(identity.get('id'))
    if user.account_balance < total_amount:
        # 余额不足
        return fail_api(code=1007, msg='用户余额不足')

    # indexes_sql = (
    #     f'select a.id, a.index_name, a.book_price '
    #     f'from novel_flask.book_index a '
    #     f'where a.book_id = {book_id} '
    #     f'and a.is_vip = 1 '
    #     f'and a.id >= {begin_index_id} '
    #     f'and not exists '
    #     f'('
    #     f'select 1 from novel_flask.user_buy_record b '
    #     f'where b.user_id = {identity.get("id")} and b.book_index_id = a.id'
    #     f') '
    #     f'order by a.id asc '
    # )
    # if buy_count > 0:
    #     indexes_sql += f'limit {buy_count} '
    # need_buy_indexes = db.session.execute(text(
    #     indexes_sql
    # )).fetchall()

    # 创建一个子查询，用于检查用户是否已经购买了这本书
    subquery = exists().where(and_(
        UserBuyRecord.user_id == identity.get("id"),
        UserBuyRecord.book_index_id == BookIndex.id
    ))
    indexes_sql = BookIndex.query.filter(
        and_(
            BookIndex.book_id == book_id,
            BookIndex.is_vip == 1,
            BookIndex.id >= begin_index_id,
            ~subquery  # 使用~来表示NOT EXISTS
        )
    ).order_by(BookIndex.id.asc())
    if buy_count > 0:
        indexes_sql = indexes_sql.limit(buy_count)
    need_buy_indexes = indexes_sql.all()

    cur_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    connection = db.get_engine(bind_key='ds1').connect()
    try:
        for one in need_buy_indexes:
            if not UserLogic.buy_one_index(connection, identity.get("id"), book_id, book_name, one.book_price, one.id,
                                           one.index_name, cur_time):
                return fail_api(msg='余额不足')

        db.session.commit()
        connection.commit()
    except Exception as e:
        db.session.rollback()
        connection.rollback()

        raise e
    finally:
        db.session.close()
        connection.close()

    return success_api()


# 关注作家
@user_bp.post('/followAuthor')
@user_login_req
def follow_author():
    identity = get_jwt_identity()

    req_json = request.get_json(force=True)
    author_id = str_escape(req_json.get("authorId"))
    operation = str_escape(req_json.get("operation"))

    if operation != '0' and operation != '1':
        return fail_api(msg='错误的操作码')

    if operation == '1':
        count = AuthorFollow.query.filter(
            AuthorFollow.author_id == author_id,
            AuthorFollow.user_id == identity.get('id')
        ).count()
        if count > 0:
            return fail_api(msg='已关注，无需重复关注！')
        # 不能关注自己
        author = Author.query.get(author_id)
        if author and author.user_id == identity.get('id'):
            return fail_api(msg='不能关注自己！')
        author_follow = AuthorFollow(author_id=author_id, user_id=identity.get('id'), create_time=datetime.now())
        db.session.add(author_follow)
    elif operation == '0':
        AuthorFollow.query.filter_by(author_id=author_id, user_id=identity.get('id')).delete()

    db.session.commit()

    return success_api()


@user_bp.get('/my_follow_list.html')
@user_login_req
def my_follow_list():
    return render_template('user/my_follow_list.html', li_my_follow_list=True)


@user_bp.get('/listFollowListByPage')
@user_login_req
def list_follow_list_by_page():
    identity = get_jwt_identity()

    page = request.args.get('page')
    page = int(page) if page else 1
    limit = request.args.get('limit')
    limit = int(limit) if limit else 10
    order_by = request.args.get("orderBy")

    page_data = UserLogic.get_follow_list_by_user(page, limit, identity.get('id'), order_by)

    return table_api(
        data=[
            {
                'author_id': item.author_id,
                'pen_name': item.pen_name,
                'user_photo': item.user_photo,
                'book_id': str(item.book_id),
                'book_name': item.book_name,
                'last_index_id': str(item.last_index_id),
                'last_index_name': item.last_index_name,
            } for item in page_data
        ],
        count=len(page_data), page=page, limit=limit)
