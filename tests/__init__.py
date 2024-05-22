import datetime
from collections import namedtuple

import jsonpickle
import pandas


def a() -> (int, str):
    return 1, '2'


class User(object):
    def __init__(self, u, p):
        self.uName = u
        self.uPwd = p

    # def __str__(self):
    #     return "%s--%s" % (self.uName, self.uPwd)
    #
    # # get方法
    # def __getstate__(self):
    #     data = self.__dict__.copy()
    #     del data['uPwd']
    #     return data


def test1():
    u = User('张三', '123')
    print(jsonpickle.encode(u))
    print(jsonpickle.encode(u, unpicklable=False))  # 打印的时候不显示包名，打包信息


def test2():
    u = User('张三', '123')
    data = dict(
        user=u,
        cur_user=u,
        date=datetime.datetime.now()
    )
    obj1 = jsonpickle.encode(data)
    obj2 = jsonpickle.encode(data, unpicklable=False)
    decoded_obj1 = jsonpickle.decode(obj1)
    decoded_obj2 = jsonpickle.decode(obj2)
    print(decoded_obj1)
    print(decoded_obj2)
    print(decoded_obj1.get('user').uName)
    print(decoded_obj2.get('user')['uName'])


def test3():
    a = (
        f'select sum(a.book_price) as total_amount '
        f'from novel_flask.book_index a '
        f'where a.book_id = 6 '
        f'and not exists '
        f'('
        f'select 1 from novel_flask.user_buy_record b '
        f'where b.book_id = a.book_id and b.book_index_id = a.id'
        f')'
    )
    print(type(a))


def test4():
    data = [['a', '1'],
            ['a', '2'],
            ['a', '3'],
            ['b', '4'],
            ['b', '5'],
            ['a', '6'],
            ['a', '7'],
            ['c', '8'],
            ['c', '9'],
            ['b', '10'],
            ['b', '11']
            ]
    df = pandas.DataFrame(data, columns=['key', 'value'])
    col = df['key']
    df['token'] = (col != col.shift()).cumsum()
    data = df.groupby(['token']).aggregate(lambda x: set(x))
    data['key'] = data['key'].apply(lambda set: set.pop())
    data['value'] = data['value'].apply(lambda set: ','.join(set))
    print(data)


def test5():
    lst = [1, 2, 3]
    tpl = (4, 5, 6)
    lst.extend(tpl)
    print(lst)


def get_page_and_limit(page: int, limit: int, total_count):
    page = 1 if (not page or page < 1) else page
    limit = 10 if (not limit or limit < 1) else limit

    # 计算总页数
    if total_count:
        total_page = (total_count + limit - 1) // limit
        page = total_page if page > total_page else page

    page_info = namedtuple('page_info', ['page', 'limit'])
    return page_info(page=page, limit=limit)


if __name__ == '__main__':
    result = get_page_and_limit(800, 10, 266)
    print(result.page, result.limit)
    # test5()
    # test4()
    # test2()
    # a, b = (1, 2)
    # print(a, b)
    # b = a()
    # print(b)
    # json = '{"id": 1, "name": "张三"}'
    # print(jsonpickle.decode(json))
    # print(None in [1, 2, '3'])
