from marshmallow import fields, post_load

from pub.exts.init_sqlalchemy import ma


class BookSettingVO(object):
    def __init__(self, id=None, book_id=None, sort=None, type=None, create_time=None, update_time=None, book_name=None,
                 pic_url=None, author_name=None, book_desc=None, score=None, cat_id=None, cat_name=None,
                 book_status=None):
        self.id = id
        self.book_id = book_id
        self.sort = sort
        self.type = type
        self.create_time = create_time
        self.update_time = update_time
        self.book_name = book_name
        self.pic_url = pic_url
        self.author_name = author_name
        self.book_desc = book_desc
        self.score = score
        self.cat_id = cat_id
        self.cat_name = cat_name
        self.book_status = book_status

    @classmethod
    def get_copy_fields(cls):
        return ('id', 'book_id', 'sort', 'type', 'create_time', 'update_time', 'book_name', 'pic_url', 'author_name',
                'book_desc', 'score', 'cat_id', 'cat_name', 'book_status')


class BookSettingVOSchema(ma.Schema):
    id = fields.Str()
    book_id = fields.Str()
    sort = fields.Integer()
    type = fields.Integer()
    create_time = fields.DateTime()
    update_time = fields.DateTime()

    book_name = fields.Str()
    pic_url = fields.Str()
    author_name = fields.Str()
    book_desc = fields.Str()
    score = fields.Float()
    cat_id = fields.Integer()
    cat_name = fields.Str()
    book_status = fields.Integer()


class BookSpVO(ma.Schema):
    keyword = fields.Str(default='')
    workDirection = fields.Integer(default=None)
    catId = fields.Integer(default=None)
    isVip = fields.Integer(default=None)
    bookStatus = fields.Integer(default=None)
    wordCountMin = fields.Integer(default=None)
    wordCountMax = fields.Integer(default=None)
    updateTimeMin = fields.Date(default=None)
    updatePeriod = fields.Integer(default=None)
    sort = fields.Str(default=None)
