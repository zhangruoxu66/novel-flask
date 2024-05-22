from sqlalchemy import and_, Connection
from sqlalchemy import text, func

from pub.exts.init_sqlalchemy import db
from pub.models.models_business import AuthorFollow, Author, User, Book, UserBuyRecord, BookIndex


class UserLogic:
    @classmethod
    def _get_data_by_sql(cls, start: int, limit: int, user_id: int, order_by: str):
        return db.session.execute(text(
            f'SELECT af.author_id, a.pen_name, u.user_photo, '
            f'       book.id AS book_id, book.book_name, book.last_index_id, book.last_index_name '
            f'FROM novel_flask.author_follow af '
            f'LEFT JOIN novel_flask.author a ON af.author_id = a.id '
            f'LEFT JOIN novel_flask.user u ON a.user_id = u.id '
            f'LEFT JOIN '
            f'  ('
            f'  SELECT * FROM novel_flask.book b '
            f'  LEFT JOIN '
            f'      ('
            f'      SELECT MAX(id) AS max_id FROM novel_flask.book '
            f'      WHERE status = 1 '
            f'      GROUP BY author_id'
            f'      ) AS t ON b.id = t.max_id '
            f'  WHERE t.max_id IS NOT NULL '
            f'  ) AS book '
            f'  ON book.author_id = a.id '
            f'WHERE af.user_id = {user_id} and a.status = 0 '
            f'ORDER BY {"af.visit_count desc" if order_by is not None and order_by == "0" else "af.create_time desc"} '
            f'LIMIT {start}, {limit}'
        )).fetchall()

    @classmethod
    def _get_data_by_orm(cls, start: int, limit: int, user_id: int, order_by: str):
        max_id_subquery = db.session.query(
            func.max(Book.id).label('max_id')
        ).filter(Book.status == 1).group_by(Book.author_id).subquery()

        book_subquery = db.session.query(Book).outerjoin(max_id_subquery, Book.id == max_id_subquery.c.max_id
                                                         ).filter(max_id_subquery.c.max_id != None).subquery()

        return db.session.query(
            AuthorFollow.author_id,
            Author.pen_name,
            User.user_photo,
            book_subquery.c.id.label('book_id'),
            book_subquery.c.book_name,
            book_subquery.c.last_index_id,
            book_subquery.c.last_index_name
        ).select_from(AuthorFollow
                      ).outerjoin(Author, AuthorFollow.author_id == Author.id
                                  ).outerjoin(User, Author.user_id == User.id
                                              ).outerjoin(book_subquery, book_subquery.c.author_id == Author.id
                                                          ).filter(AuthorFollow.user_id == user_id
                                                                   ).filter(Author.status == 0
                                                                            ).order_by(
            AuthorFollow.visit_count if order_by is not None and order_by == "0" else AuthorFollow.create_time.desc()
        ).offset(start).limit(limit).all()

    @classmethod
    def get_follow_list_by_user(cls, page: int, limit: int, user_id: int, order_by: str):
        """
        获取用户关注的作家列表
        """
        start = (page - 1) * limit
        return cls._get_data_by_orm(start, limit, user_id, order_by)

    @classmethod
    def buy_one_index(cls, connection: Connection, user_id: int, book_id: int, book_name: str, book_price: float,
                      book_index_id: int,
                      book_index_name: str, cur_time: str) -> bool:
        # 生成购买记录
        # rowcount = db.session.execute(text(
        #     f'INSERT INTO '
        #     f'novel_flask.user_buy_record(user_id, book_id, book_name, book_index_id, book_index_name, buy_amount, create_time) '
        #     f'SELECT {user_id}, {book_id}, "{book_name}", {book_index_id}, "{book_index_name}", {book_price}, "{cur_time}" '
        #     f'FROM DUAL '
        #     f'WHERE NOT EXISTS '
        #     f'('
        #     f'SELECT 1 FROM novel_flask.user_buy_record where user_id = {user_id} and book_index_id = {book_index_id}'
        #     f')'
        # )).rowcount
        # 查询是否已存在对应记录
        exists_query = UserBuyRecord.query.filter(
            and_(UserBuyRecord.user_id == user_id, UserBuyRecord.book_index_id == book_index_id)
        ).exists()
        # 插入记录
        insert_query = UserBuyRecord.__table__.insert().from_select(
            ['user_id', 'book_id', 'book_name', 'book_index_id', 'book_index_name', 'buy_amount', 'create_time'],
            db.session.query(
                text(f'{user_id}'), text(f'{book_id}'), text(f'"{book_name}"'), text(f'{book_index_id}'),
                text(f'"{book_index_name}"'), text(f'{book_price}'), text(f'"{cur_time}"')
            ).filter(~exists_query)
        )
        # 执行插入操作
        # rowcount = db.session.execute(insert_query).rowcount
        # connection = db.get_engine(bind_key='ds1').connect()
        rowcount = connection.execute(insert_query).rowcount
        # connection.commit()
        if rowcount <= 0:
            return True

        # 减少用户余额
        # rowcount = db.session.execute(text(
        #     f'update novel_flask.user a '
        #     f'set a.account_balance = a.account_balance - {book_price} '
        #     f'where a.id = {user_id} and a.account_balance >= {book_price} '
        #     # f'and exists (select 1 from novel_flask.book_index b where b.id = {book_index_id}) '  # 鸡肋的判断
        # )).rowcount
        rowcount = db.session.query(User).filter(
            User.id == user_id,
            User.account_balance >= book_price,
            BookIndex.query.filter(
                BookIndex.id == book_index_id
            ).exists()
        ).update({User.account_balance: User.account_balance - book_price}, synchronize_session=False)
        return rowcount > 0
