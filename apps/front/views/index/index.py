import threading
from collections import namedtuple
from datetime import datetime
from itertools import groupby

from flask import Blueprint, render_template, copy_current_request_context
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import func

from apps.front.service import book_service, author_service
from pub import consts, executor, context_wrap
from pub.consts import RedisKey
from pub.curd import AutoModelTransfer, model_to_json, json_to_model
from pub.exts.init_sqlalchemy import db
from pub.helper import ModelFilter
from pub.models.models_business import BookSetting, Book, News, BookComment, User, BookIndex, BookContent, \
    UserBuyRecord, Author, UserReadHistory
from pub.schemas.schemas_business import BookSettingVOSchema, BookSettingVO
from pub.utils.obj_utils import copy_some
from pub.utils.redis_utils import Redis

index_bp = Blueprint('Index', __name__, url_prefix='/')


def init_index_book_setting():
    now = datetime.now()
    books = db.session.query(
        Book.id, Book.book_name, Book.author_name, Book.pic_url, Book.book_desc, Book.score,
        Book.cat_id, Book.cat_name, Book.book_status
    ).filter(
        Book.word_count > 0
    ).order_by(
        Book.score.asc(), func.random()
    ).limit(consts.INDEX_BOOK_SETTING_NUM).all()

    if len(books) == consts.INDEX_BOOK_SETTING_NUM:
        book_setting_list = []
        book_setting_vo_list = []
        for i in range(len(books)):
            book = books[i]
            _type = 4
            if i < 4:
                _type = 0
            elif i < 14:
                _type = 1
            elif i < 19:
                _type = 2
            elif i < 25:
                _type = 3
            book_setting_vo = BookSettingVO()
            book_setting = BookSetting(
                type=_type,
                sort=i,
                book_id=book.id,
                create_time=now,
                update_time=now
            )
            book_setting_list.append(book_setting)
            db.session.add(book_setting)
            db.session.flush()

            copy_some(book, book_setting_vo, book_setting_vo.get_copy_fields())
            copy_some(book_setting, book_setting_vo, book_setting_vo.get_copy_fields())
            book_setting_vo_list.append(book_setting_vo)

        db.session.commit()

        return book_setting_vo_list

    return []


def get_book_setting():
    data = Redis.get(RedisKey.INDEX_BOOK_SETTINGS_KEY, default=None)
    if data and len(data) >= consts.OBJECT_JSON_CACHE_EXIST_LENGTH:
        data = json_to_model(schema=BookSettingVOSchema, data=data)
        data.sort(key=lambda x: (x['type']), reverse=False)
        return groupby(data, key=lambda x: (x['type']))

    data = book_service.get_index_book_setting()
    data.sort(key=lambda x: x.type)

    if len(data) == 0:
        # 如果首页小说没有被设置，则初始化首页小说设置
        data = init_index_book_setting()

    Redis.set(RedisKey.INDEX_BOOK_SETTINGS_KEY, model_to_json(schema=BookSettingVOSchema, data=data))

    return groupby(data, key=lambda x: x.type)


def list_index_news():
    data = Redis.get(RedisKey.INDEX_NEWS_KEY, default=None)
    if data:
        data = AutoModelTransfer.json_2_dict(model=News, data=data)
        return data

    data = db.session.query(
        News.id, News.cat_name, News.cat_id, News.title, News.create_time
    ).order_by(
        News.create_time.desc()
    ).limit(2).all()
    Redis.set(RedisKey.INDEX_NEWS_KEY, AutoModelTransfer.model_2_json(model=News, data=data))
    return data


@index_bp.route('/')
def index():
    book_map = executor.submit(context_wrap(get_book_setting)).result()
    news_list = executor.submit(context_wrap(list_index_news)).result()

    book_map = {k: tuple(v) for k, v in book_map}

    return render_template('index.html', navType=0, bookMap=book_map, newsList=news_list)


@index_bp.route('/book/bookclass.html')
def book_class():
    return render_template('book/bookclass.html', navType=1)


def query_book_detail(book_id) -> Book:
    book = Book.query.get_or_404(book_id)
    return book


def list_comment_by_page(user_id, book_id, page, page_size):
    # 查询参数构造
    mf = ModelFilter()
    if book_id:
        mf.exact(field_name="book_id", value=book_id)
    if user_id:
        mf.exact(field_name="create_user_id", value=user_id)

    data = db.session.query(
        BookComment.book_id, BookComment.book_id, BookComment.comment_content, BookComment.reply_count,
        BookComment.create_time,
        User.nick_name.label('create_user_name'), User.user_photo.label('create_user_photo')
    ).join(
        User, BookComment.create_user_id == User.id
    ).filter(
        mf.get_filter(BookComment)
    ).order_by(
        BookComment.create_time.desc()
    ).paginate(page=page, per_page=page_size, error_out=False)
    count = data.total
    return data, count


def query_first_book_index_info(book_id: int, identity) -> namedtuple:
    """
    查询小说详情页“点击阅读”按钮应跳转的章节id
    注意：此章节id（first_book_index_id）不一定是该小说的第一个章节，需分情况讨论，情况如下：
    （1）用户未登录，则跳转至小说第一章
    （2）用户已登录，但是此前为阅读过该小说（即阅读历史表查不到该用户关于该本小说的记录），则同样跳转至小说第一章
    （3）用户已登录，且此前阅读过该小说，则跳转至最新阅读过的章节

    :param book_id: 小说id
    :param identity: JWT身份认证信息

    :return: 包含首章节id（first_book_index_id）和阅读按钮文本信息（read_button_text）的namedtuple，结构如下：
            {first_book_index_id: 1, read_button_text: '开始阅读'}，访问时直接使用.属性名即可，例如result.read_button_text
    """
    result = namedtuple(
        'result', ['first_book_index_id', 'read_button_text']
    )

    if identity and identity.get('id'):
        data = db.session.query(
            UserReadHistory.pre_content_id
        ).filter(
            UserReadHistory.user_id == identity.get('id'),
            UserReadHistory.book_id == book_id
        ).order_by(
            UserReadHistory.create_time.desc()
        ).first()
        if data and data.pre_content_id:
            return result(first_book_index_id=data.pre_content_id, read_button_text='继续阅读')

    data = db.session.query(BookIndex.id).filter(
        BookIndex.book_id == book_id
    ).order_by(
        BookIndex.index_num.asc()
    ).first()
    return result(first_book_index_id=data.id if data else None, read_button_text='开始阅读')


def list_rec_book_by_cat_id(cat_id: int, book_id: int):
    data = db.session.query(Book.id, Book.pic_url, Book.book_name, Book.book_desc).filter(
        Book.cat_id == cat_id, Book.id != book_id
    ).order_by(func.random()).limit(4).all()
    return data


def get_author_avatar(author_id):
    author = db.session.query(Author.user_id).filter_by(id=author_id).first()
    if not author:
        return None
    user_id = author.user_id

    user = db.session.query(User.user_photo).filter_by(id=user_id).first()
    return user.user_photo if user else None


@index_bp.get('/book/<int:book_id>.html')
@jwt_required(optional=True)
def load_book(book_id):
    identity = get_jwt_identity()

    # 加载小说基本信息线程
    book = query_book_detail(book_id)

    # 加载小说评论列表线程
    page_comments, count = executor.submit(context_wrap(list_comment_by_page), None, book_id, 1, 5).result()
    # 加载小说首章信息线程，该线程在加载小说基本信息线程执行完毕后才执行
    first_book_index_info = executor.submit(context_wrap(query_first_book_index_info), book_id, identity).result()
    # 加载随机推荐小说线程，该线程在加载小说基本信息线程执行完毕后才执行
    rec_books = executor.submit(context_wrap(list_rec_book_by_cat_id), book.cat_id, book_id).result()
    # 加载作者头像
    author_avatar = executor.submit(context_wrap(get_author_avatar), book.author_id).result()
    # 加载关注状态
    follow_status = executor.submit(context_wrap(author_service.get_follow_status), book.author_id, identity).result()

    # 增加用户访问关注的作家次数
    @copy_current_request_context
    def runner(author_id: int, jwt_identity):
        author_service.add_author_visit_count(author_id, jwt_identity)
    job = threading.Thread(target=runner, args=(book.author_id, identity))
    job.start()

    return render_template('book/book_detail.html',
                           book=book, first_book_index_info=first_book_index_info, rec_books=rec_books,
                           page_comments=page_comments, comments_count=count, author_avatar=author_avatar,
                           follow_status=follow_status)


def query_pre_book_index_id(book_id, index_num):
    data = db.session.query(BookIndex.id).filter(
        BookIndex.book_id == book_id,
        BookIndex.index_num < index_num
    ).order_by(
        BookIndex.index_num.desc()
    ).first()
    if not data:
        return 0
    return data.id


def query_next_book_index_id(book_id, index_num):
    data = db.session.query(BookIndex.id).filter(
        BookIndex.book_id == book_id,
        BookIndex.index_num > index_num
    ).order_by(
        BookIndex.index_num.asc()
    ).first()
    if not data:
        return 0
    return data.id


def query_book_content(book_id, book_index_id):
    model = BookContent.model(book_id=book_id, index_id=book_index_id)
    book_content = db.session.query(model.id, model.content).filter(
        model.index_id == book_index_id
    ).first()

    return book_content


def get_need_buy(book_id, book_index, book_index_id: int, identity, author_id: int):
    if book_index.is_vip and book_index.is_vip == 1:
        if not identity or not identity.get('id'):
            # 未登录，需要购买
            return True
        # 作者可以免费看自己的书
        author = Author.query.get(author_id)
        if author and author.user_id == identity.get('id'):
            return False

        is_buy = UserBuyRecord.query.filter(
            UserBuyRecord.user_id == identity.get('id'),
            UserBuyRecord.book_id == book_id,
            UserBuyRecord.book_index_id == book_index_id
        ).count() > 0
        if not is_buy:
            return True

    return False


@index_bp.get('/book/<int:book_id>/<int:book_index_id>.html')
@jwt_required(optional=True)
def load_book_content(book_id, book_index_id):
    identity = get_jwt_identity()

    book = Book.query.get_or_404(book_id)

    book_index = db.session.query(
        BookIndex.id, BookIndex.book_id, BookIndex.index_num, BookIndex.index_name, BookIndex.word_count,
        BookIndex.book_price, BookIndex.update_time, BookIndex.is_vip, BookIndex.storage_type
    ).filter(
        BookIndex.id == book_index_id
    ).first_or_404()

    # 查询上一章节目录ID线程
    pre_book_index_id = executor.submit(context_wrap(query_pre_book_index_id), book_id, book_index.index_num).result()

    # 查询下一章目录ID线程
    next_book_index_id = executor.submit(context_wrap(query_next_book_index_id), book_id, book_index.index_num).result()

    # 查询内容线程
    book_content = executor.submit(context_wrap(query_book_content), book_id, book_index_id).result()

    # 判断用户是否需要购买线程
    need_buy = executor.submit(context_wrap(get_need_buy), book_id, book_index, book_index_id, identity,
                               book.author_id).result()

    # 增加用户访问关注的作家次数
    @copy_current_request_context
    def runner(author_id: int, jwt_identity):
        author_service.add_author_visit_count(author_id, jwt_identity)

    job = threading.Thread(target=runner, args=(book.author_id, identity))
    job.start()

    return render_template('book/book_content.html', book=book, bookIndex=book_index, preBookIndexId=pre_book_index_id,
                           nextBookIndexId=next_book_index_id, bookContent=book_content, needBuy=need_buy, navType=10)


@index_bp.get('/book/indexList-<int:book_id>.html')
def index_list(book_id):
    book = Book.query.get(book_id)
    book_index_list = db.session.query(
        BookIndex.id, BookIndex.book_id, BookIndex.index_num, BookIndex.index_name, BookIndex.update_time,
        BookIndex.is_vip
    ).filter(
        BookIndex.book_id == book_id
    ).all()
    return render_template('book/book_index.html', book=book, bookIndexList=book_index_list,
                           bookIndexCount=len(book_index_list))


@index_bp.get('/book/book_ranking')
def book_rank():
    return render_template('book/book_ranking.html', navType=2)


@index_bp.get('/book/comment-<int:book_id>.html')
@jwt_required(optional=True)
def comment_list(book_id: int):
    book = Book.query.get(book_id)
    # 加载关注状态
    follow_status = author_service.get_follow_status(book.author_id, get_jwt_identity())
    return render_template('book/book_comment.html', book=book, follow_status=follow_status)
