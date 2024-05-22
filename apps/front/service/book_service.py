from datetime import datetime

from apps.front.config import BookPrice, FrontConfig
from pub.exts.init_sqlalchemy import db
from pub.models.models_business import BookComment, User, Book, BookIndex, BookContent, BookSetting
from pub.utils import date_utils
from pub.utils.http_utils import table_api, fail_api
from pub.utils.snowflake import IdWorker
from pub.utils.string_utils import get_str_valid_word_count

order_type = {
    0: Book.visit_count.desc(),
    1: Book.create_time.desc(),  # 最新入库排序
    2: Book.last_index_update_time.desc(),  # 最新更新时间排序
    3: Book.comment_count.desc()  # 评论数量排序
}


def list_rank(_type: int, limit: int):
    data = db.session.query(
        Book.id, Book.cat_id, Book.cat_name, Book.book_name, Book.last_index_id, Book.last_index_name,
        Book.author_id, Book.author_name, Book.pic_url, Book.book_desc, Book.word_count,
        Book.last_index_update_time
    ).filter(
        Book.word_count > 0
    ).order_by(
        order_type[_type]
    ).offset(0).limit(limit).all()

    return data


def list_comment_by_page(user_id, book_id, page, limit):
    filters = []
    if book_id:
        filters.append(BookComment.book_id == book_id)
    if user_id:
        filters.append(BookComment.create_user_id == user_id)

    data = db.session.query(
        BookComment, User
    ).join(
        User, BookComment.create_user_id == User.id
    ).filter(
        *filters
    ).order_by(
        BookComment.create_time.desc()
    ).paginate(page=page, per_page=limit, error_out=False)

    return table_api(
        data=[
            {
                'id': book_comment.id,
                'book_id': book_comment.book_id,
                'comment_content': book_comment.comment_content,
                'reply_count': book_comment.reply_count,
                'create_time': date_utils.set_timezone(book_comment.create_time),
                # 'create_time': book_comment.create_time,

                'create_user_name': user.nick_name,
                'create_user_photo': user.user_photo
            } for book_comment, user in data.items
        ],
        count=data.total, page=page, limit=limit)


def query_id_by_name_and_author(book_name, pen_name):
    book = db.session.query(Book.id).filter(
        Book.book_name == book_name,
        Book.author_name == pen_name
    ).first()
    if not book:
        return None
    else:
        return book.id


def add_book(book: Book, author_id: int, pen_name: str):
    # 判断小说名是否存在
    if query_id_by_name_and_author(book.book_name, pen_name):
        # 该作者发布过此书名的小说
        return fail_api(code=4003, msg='已发布过同名小说！')

    # api校验：评论区状态只能是0或1
    if book.comment_enabled != 0 and book.comment_enabled != 1:
        return fail_api(code=4003, msg='错误的评论区状态！')

    book.author_name = pen_name
    book.author_id = author_id
    book.visit_count = 0
    book.word_count = 0
    book.score = 6.5
    book.last_index_name = ''
    book.create_time = datetime.now()
    book.update_time = book.create_time

    db.session.add(book)
    db.session.commit()


order_by = {
    0: BookIndex.index_num.desc()
}


def query_index_list(book_id: int, order_type: int, page: int, limit: int):
    data = db.session.query(
        BookIndex.id, BookIndex.book_id, BookIndex.index_num, BookIndex.index_name, BookIndex.update_time,
        BookIndex.is_vip
    ).filter(
        BookIndex.book_id == book_id
    ).order_by(
        order_by[order_type]
    ).paginate(page=page, per_page=limit, error_out=False)

    return table_api(
        data=[
            {
                'id': str(book_index.id),
                'book_id': str(book_index.book_id),
                'index_num': book_index.index_num,
                'index_name': book_index.index_name,
                'update_time': book_index.update_time,
                'is_vip': book_index.is_vip
            } for book_index in data.items
        ],
        count=data.total, page=page, limit=limit)


def add_book_content(book_id: int, index_name: str, content: str, is_vip: int, author_id: int):
    book = Book.query.get(book_id)
    if author_id != book.author_id:
        # 并不是更新自己的小说
        return
    old_last_index_id = book.last_index_id
    last_index_id = IdWorker(FrontConfig.SNOWFLAKE_DATACENTER_ID, FrontConfig.SNOWFLAKE_WORKER_ID,
                             FrontConfig.SNOWFLAKE_SEQUENCE).get_id()
    current_date = datetime.now()
    word_count = get_str_valid_word_count(content)

    # 更新小说主表信息
    book.last_index_id = last_index_id
    book.last_index_name = index_name
    book.last_index_update_time = current_date
    book.word_count += word_count
    db.session.add(book)

    # 计算价格
    # TODO 这里应该不能直接这么计算，后续修改
    book_price = int(word_count * BookPrice.value / BookPrice.word_count)

    # 更新小说目录表
    index_num = 0
    if old_last_index_id:
        book_index = BookIndex.query.get(old_last_index_id)
        index_num = book_index.index_num + 1
    last_book_index = BookIndex()
    last_book_index.id = last_index_id
    last_book_index.word_count = word_count
    last_book_index.index_name = index_name
    last_book_index.index_num = index_num
    last_book_index.book_id = book_id
    last_book_index.is_vip = is_vip
    last_book_index.book_price = book_price
    last_book_index.create_time = current_date
    last_book_index.update_time = current_date
    db.session.add(last_book_index)

    # 更新小说内容表
    model = BookContent.model(book_id=book.id, index_id=last_index_id)
    book_content = model()
    book_content.index_id = last_index_id
    book_content.content = content
    db.session.add(book_content)

    db.session.commit()


def update_book_content(index_id: int, index_name: str, content: str, author_id: int):
    book_index = BookIndex.query.get(index_id)
    if book_index:
        book_id = book_index.book_id
        # 查询小说表信息
        book = Book.query.get(book_id)
        # 作者ID相同，表明该小说是登录用户发布，可以修改
        if book.author_id == author_id:
            cur_date = datetime.now()
            word_count = get_str_valid_word_count(content)
            # TODO 这里应该不能直接这么计算，后续修改
            book_price = int(word_count * BookPrice.value / BookPrice.word_count)

            # 更新小说目录表
            book_index.index_name = index_name
            book_index.word_count = word_count
            book_index.book_price = book_price
            book_index.update_time = cur_date
            db.session.add(book_index)

            # 更新小说内容表
            model = BookContent.model(book_id=book.id, index_id=index_id)
            model.query.filter(
                model.index_id == index_id
            ).update({'content': content})

            db.session.commit()


def query_index_content(index_id: int, author_id: int):
    book_index = BookIndex.query.get(index_id)

    if book_index:
        # 获取小说ID
        book_id = book_index.book_id
        # 查询小说表信息
        book = Book.query.get(book_id)
        if book and book.author_id == author_id:
            model = BookContent.model(book_id=book_id, index_id=index_id)
            book_content = db.session.query(model.content).filter(
                model.index_id == index_id
            ).first()
            return book_content.content

    return ''


def get_book_setting_sub_query(setting_type: int = 0, limit_num: int = 10):
    sub_query = db.session.query(
        BookSetting.book_id, BookSetting.type, BookSetting.sort,
        Book.book_name, Book.author_name, Book.pic_url, Book.book_desc, Book.score, Book.cat_id, Book.cat_name,
        Book.book_status
    ).join(
        Book, BookSetting.book_id == Book.id
    ).filter(
        BookSetting.type == setting_type
    ).order_by(
        BookSetting.sort.asc(),
        BookSetting.id.asc()
    ).limit(limit_num)

    return sub_query


def get_index_book_setting():
    # 轮播图，限制4个
    sub_query_0 = get_book_setting_sub_query(setting_type=0, limit_num=4)

    # 顶部小说栏，限制10个
    sub_query_1 = get_book_setting_sub_query(setting_type=1, limit_num=10)

    # 本周强推，限制5个
    sub_query_2 = get_book_setting_sub_query(setting_type=2, limit_num=5)

    # 热门推荐，限制6个
    sub_query_3 = get_book_setting_sub_query(setting_type=3, limit_num=6)

    # 精品推荐，限制6个
    sub_query_4 = get_book_setting_sub_query(setting_type=4, limit_num=6)

    query_obj = sub_query_0.union_all(sub_query_1).union_all(sub_query_2).union_all(sub_query_3).union_all(sub_query_4)

    return query_obj.all()
