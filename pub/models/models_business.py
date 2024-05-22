from datetime import datetime
from typing import Type

from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash

from pub.consts.dict_consts import DictConsts
from pub.exts.init_sqlalchemy import db
from pub.models.models_system import DictType


class Author(db.Model):
    __bind_key__ = 'ds1'
    __tablename__ = 'author'

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger)
    invite_code = db.Column(db.String(20))
    pen_name = db.Column(db.String(20))
    tel_phone = db.Column(db.String(20))
    chat_account = db.Column(db.String(50))
    email = db.Column(db.String(50))
    work_direction = db.Column(db.Integer)
    status = db.Column(db.Integer, server_default=db.FetchedValue())
    create_time = db.Column(db.DateTime)


class AuthorCode(db.Model):
    __bind_key__ = 'ds1'
    __tablename__ = 'author_code'

    id = db.Column(db.BigInteger, primary_key=True)
    invite_code = db.Column(db.String(100), unique=True)
    validity_time = db.Column(db.DateTime)
    is_use = db.Column(db.Integer, server_default=db.FetchedValue())
    create_time = db.Column(db.DateTime, default=datetime.now)
    create_user_id = db.Column(db.BigInteger)


class AuthorIncome(db.Model):
    __bind_key__ = 'ds1'
    __tablename__ = 'author_income'

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, nullable=False)
    author_id = db.Column(db.BigInteger, nullable=False)
    book_id = db.Column(db.BigInteger, nullable=False)
    income_month = db.Column(db.Date, nullable=False)
    pre_tax_income = db.Column(db.BigInteger, nullable=False, server_default=db.FetchedValue())
    after_tax_income = db.Column(db.BigInteger, nullable=False, server_default=db.FetchedValue())
    pay_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    confirm_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    detail = db.Column(db.String(255))
    create_time = db.Column(db.DateTime)


class AuthorIncomeDetail(db.Model):
    __bind_key__ = 'ds1'
    __tablename__ = 'author_income_detail'

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, nullable=False)
    author_id = db.Column(db.BigInteger, nullable=False)
    book_id = db.Column(db.BigInteger, nullable=False, server_default=db.FetchedValue())
    income_date = db.Column(db.Date, nullable=False)
    income_account = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    income_count = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    income_number = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    create_time = db.Column(db.DateTime)


class Book(db.Model):
    __bind_key__ = 'ds1'
    __tablename__ = 'book'
    __table_args__ = (
        db.Index('key_uq_bookName_authorName', 'book_name', 'author_name'),
    )

    id = db.Column(db.BigInteger, primary_key=True)
    work_direction = db.Column(db.Integer)
    cat_id = db.Column(db.Integer)
    cat_name = db.Column(db.String(50))
    pic_url = db.Column(db.String(200), nullable=False)
    book_name = db.Column(db.String(50), nullable=False)
    author_id = db.Column(db.BigInteger)
    author_name = db.Column(db.String(50), nullable=False)
    book_desc = db.Column(db.String(2000), nullable=False)
    score = db.Column(db.Float, nullable=False)
    book_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    visit_count = db.Column(db.BigInteger, server_default=db.FetchedValue())
    word_count = db.Column(db.Integer)
    comment_count = db.Column(db.Integer, server_default=db.FetchedValue())
    yesterday_buy = db.Column(db.Integer, server_default=db.FetchedValue())
    last_index_id = db.Column(db.BigInteger)
    last_index_name = db.Column(db.String(50))
    last_index_update_time = db.Column(db.DateTime, index=True)
    is_vip = db.Column(db.Integer, server_default=db.FetchedValue())
    status = db.Column(db.Integer, server_default=db.FetchedValue())
    update_time = db.Column(db.DateTime, nullable=False)
    create_time = db.Column(db.DateTime, index=True)
    crawl_source_id = db.Column(db.Integer)
    crawl_book_id = db.Column(db.String(32))
    crawl_last_time = db.Column(db.DateTime)
    crawl_is_stop = db.Column(db.Integer, server_default=db.FetchedValue())
    comment_enabled = db.Column(db.Integer, server_default=db.FetchedValue())


class BookAuthor(db.Model):
    __bind_key__ = 'ds1'
    __tablename__ = 'book_author'

    id = db.Column(db.BigInteger, primary_key=True)
    invite_code = db.Column(db.String(20))
    pen_name = db.Column(db.String(20))
    tel_phone = db.Column(db.String(20))
    chat_account = db.Column(db.String(50))
    email = db.Column(db.String(50))
    work_direction = db.Column(db.Integer)
    status = db.Column(db.Integer)
    create_time = db.Column(db.DateTime)
    create_user_id = db.Column(db.BigInteger)
    update_time = db.Column(db.DateTime)
    update_user_id = db.Column(db.BigInteger)


class BookCategory(db.Model):
    __bind_key__ = 'ds1'
    __tablename__ = 'book_category'

    id = db.Column(db.Integer, primary_key=True)
    work_direction = db.Column(db.Integer)
    name = db.Column(db.String(20), nullable=False)
    sort = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    create_user_id = db.Column(db.BigInteger)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_user_id = db.Column(db.BigInteger)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class BookComment(db.Model):
    __bind_key__ = 'ds1'
    __tablename__ = 'book_comment'
    __table_args__ = (
        db.Index('key_uq_bookid_userid', 'book_id', 'create_user_id'),
    )

    id = db.Column(db.BigInteger, primary_key=True)
    book_id = db.Column(db.BigInteger)
    comment_content = db.Column(db.String(512))
    reply_count = db.Column(db.Integer, server_default=db.FetchedValue())
    audit_status = db.Column(db.Integer, server_default=db.FetchedValue())
    create_time = db.Column(db.DateTime)
    create_user_id = db.Column(db.BigInteger)


class BookCommentReply(db.Model):
    __bind_key__ = 'ds1'
    __tablename__ = 'book_comment_reply'

    id = db.Column(db.BigInteger, primary_key=True)
    comment_id = db.Column(db.BigInteger)
    reply_content = db.Column(db.String(512))
    audit_status = db.Column(db.Integer, server_default=db.FetchedValue())
    create_time = db.Column(db.DateTime)
    create_user_id = db.Column(db.BigInteger)


# class BookContent(db.Model):
#     __bind_key__ = 'ds1'
#     __tablename__ = 'book_content'
#
#     id = db.Column(db.BigInteger, primary_key=True)
#     index_id = db.Column(db.BigInteger, unique=True)
#     content = db.Column(db.String)


class BookContent(object):
    _mapper = {}

    @staticmethod
    def model(book_id=None, index_id=None) -> Type[db.Model]:
        """
        获取分库分表切片的模型类
        :param book_id: 书（小说）id
        :param index_id: 章节id
        :return: 分库分表切片的模型类
        """

        # 确定数据源
        if not current_app.config.get('DATABASE_SHARDING_ENABLE') or not book_id:
            data_source = 'ds1'
        else:
            data_source = f'ds{int(book_id) % 10}'

        # 确定模型类名
        if not current_app.config.get('TABLE_SHARDING_ENABLE') or not index_id:
            class_name = 'BookContent'
            table_name = 'book_content'
        else:
            table_id = int(index_id) % 10
            class_name = f'BookContent{table_id}'
            table_name = f'book_content{table_id}'

        ModelClass = BookContent._mapper.get(class_name, None)
        if ModelClass is None:
            ModelClass = type(class_name, (db.Model,), {
                '__moduel__': __name__,
                '__name__': class_name,
                '__bind_key__': data_source,
                '__tablename__': table_name,

                'id': db.Column(db.BigInteger, primary_key=True),
                'index_id': db.Column(db.BigInteger, unique=True),
                'content': db.Column(db.String),
            })
            BookContent._mapper[class_name] = ModelClass

        return ModelClass


class BookIndex(db.Model):
    __bind_key__ = 'ds1'
    __tablename__ = 'book_index'
    __table_args__ = (
        db.Index('key_uq_bookId_indexNum', 'book_id', 'index_num'),
    )

    id = db.Column(db.BigInteger, primary_key=True)
    book_id = db.Column(db.BigInteger, nullable=False, index=True)
    index_num = db.Column(db.Integer, nullable=False, index=True)
    index_name = db.Column(db.String(100))
    word_count = db.Column(db.Integer)
    is_vip = db.Column(db.Integer, server_default=db.FetchedValue())
    book_price = db.Column(db.Integer, server_default=db.FetchedValue())
    storage_type = db.Column(db.String(10), nullable=False, server_default=db.FetchedValue())
    create_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime)


class BookScreenBullet(db.Model):
    __bind_key__ = 'ds1'
    __tablename__ = 'book_screen_bullet'

    id = db.Column(db.BigInteger, primary_key=True)
    content_id = db.Column(db.BigInteger, nullable=False, index=True)
    screen_bullet = db.Column(db.String(512), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)


class BookSetting(db.Model):
    __bind_key__ = 'ds1'
    __tablename__ = 'book_setting'

    id = db.Column(db.BigInteger, primary_key=True)
    book_id = db.Column(db.BigInteger)
    sort = db.Column(db.Integer)
    type = db.Column(db.Integer)
    create_time = db.Column(db.DateTime, default=datetime.now())
    create_user_id = db.Column(db.BigInteger)
    update_time = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    update_user_id = db.Column(db.BigInteger)


class FriendLink(db.Model):
    __bind_key__ = 'ds1'
    __tablename__ = 'friend_link'

    id = db.Column(db.Integer, primary_key=True)
    link_name = db.Column(db.String(50), nullable=False)
    link_url = db.Column(db.String(100), nullable=False)
    sort = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    is_open = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    create_user_id = db.Column(db.BigInteger)
    create_time = db.Column(db.DateTime, default=datetime.now())
    update_user_id = db.Column(db.BigInteger)
    update_time = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())


class News(db.Model):
    __bind_key__ = 'ds1'
    __tablename__ = 'news'

    id = db.Column(db.BigInteger, primary_key=True)
    cat_id = db.Column(db.Integer)
    cat_name = db.Column(db.String(50))
    source_name = db.Column(db.String(50))
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    read_count = db.Column(db.BigInteger, nullable=False, server_default=db.FetchedValue())
    create_time = db.Column(db.DateTime, default=datetime.now())
    create_user_id = db.Column(db.BigInteger)
    update_time = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    update_user_id = db.Column(db.BigInteger)


class NewsCategory(db.Model):
    __bind_key__ = 'ds1'
    __tablename__ = 'news_category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    sort = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    create_user_id = db.Column(db.BigInteger)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_user_id = db.Column(db.BigInteger)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class OrderPay(db.Model):
    __bind_key__ = 'ds1'
    __tablename__ = 'order_pay'

    id = db.Column(db.BigInteger, primary_key=True)
    out_trade_no = db.Column(db.BigInteger, nullable=False)
    trade_no = db.Column(db.String(64))
    pay_channel = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    total_amount = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.BigInteger, nullable=False)
    pay_status = db.Column(db.Integer, server_default=db.FetchedValue())
    create_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime)


class User(db.Model):
    __bind_key__ = 'ds1'
    __tablename__ = 'user'

    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    nick_name = db.Column(db.String(50))
    user_photo = db.Column(db.String(100))
    user_sex = db.Column(db.Integer)
    account_balance = db.Column(db.BigInteger, nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    create_time = db.Column(db.DateTime, nullable=False)
    update_time = db.Column(db.DateTime, nullable=False)

    @property
    def user_sex_translation(self):
        if self.user_sex is not None:
            dict_data = DictType.get_dict_data(DictConsts.SEX, self.user_sex)
            if not dict_data:
                return str(self.user_sex) + '：' + str(self.user_sex)
            return str(self.user_sex) + '：' + dict_data.data_label
        return ''

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password, password)


class UserBookshelf(db.Model):
    __bind_key__ = 'ds1'
    __tablename__ = 'user_bookshelf'
    __table_args__ = (
        db.Index('key_uq_userid_bookid', 'user_id', 'book_id'),
    )

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, nullable=False)
    book_id = db.Column(db.BigInteger, nullable=False)
    pre_content_id = db.Column(db.BigInteger)
    create_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime)


class UserBuyRecord(db.Model):
    __bind_key__ = 'ds1'
    __tablename__ = 'user_buy_record'
    __table_args__ = (
        db.Index('key_userId_indexId', 'user_id', 'book_index_id'),
    )

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, nullable=False)
    book_id = db.Column(db.BigInteger)
    book_name = db.Column(db.String(50))
    book_index_id = db.Column(db.BigInteger)
    book_index_name = db.Column(db.String(100))
    buy_amount = db.Column(db.Integer)
    create_time = db.Column(db.DateTime)

    def __init__(self, user_id, book_id, book_name, book_index_id, book_index_name, buy_amount, create_time):
        self.user_id = user_id
        self.book_id = book_id
        self.book_name = book_name
        self.book_index_id = book_index_id
        self.book_index_name = book_index_name
        self.buy_amount = buy_amount
        self.create_time = create_time if create_time else datetime.now()


class UserFeedback(db.Model):
    __bind_key__ = 'ds1'
    __tablename__ = 'user_feedback'

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger)
    content = db.Column(db.String(512))
    create_time = db.Column(db.DateTime)


class UserReadHistory(db.Model):
    __bind_key__ = 'ds1'
    __tablename__ = 'user_read_history'
    __table_args__ = (
        db.Index('key_uq_userid_bookid', 'user_id', 'book_id'),
    )

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, nullable=False)
    book_id = db.Column(db.BigInteger, nullable=False)
    pre_content_id = db.Column(db.BigInteger)
    create_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime)


class WebsiteInfo(db.Model):
    __bind_key__ = 'ds1'
    __tablename__ = 'website_info'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    domain = db.Column(db.String(50), nullable=False)
    keyword = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(512), nullable=False)
    qq = db.Column(db.String(20), nullable=False)
    logo = db.Column(db.String(200), nullable=False)
    logo_dark = db.Column(db.String(200), nullable=False)
    create_time = db.Column(db.DateTime)
    create_user_id = db.Column(db.BigInteger)
    update_time = db.Column(db.DateTime)
    update_user_id = db.Column(db.BigInteger)


class AuthorFollow(db.Model):
    __bind_key__ = 'ds1'
    __tablename__ = 'author_follow'
    __table_args__ = (
        db.Index('key_uq_authorid_userid', 'author_id', 'user_id'),
    )

    id = db.Column(db.BigInteger, primary_key=True)
    author_id = db.Column(db.BigInteger)
    user_id = db.Column(db.BigInteger)
    visit_count = db.Column(db.Integer, server_default=db.FetchedValue())
    create_time = db.Column(db.DateTime)
