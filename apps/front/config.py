from datetime import timedelta

from pub.config import BaseConfig


class FrontConfig(BaseConfig):
    PORT = 8080

    SYSTEM_NAME = 'Novel Flask'

    SECRET_KEY = "novel-flask-fgdafgbfdg*52626216"

    JWT_SECRET_KEY = 'jwt-secret-key-1256sdf4564156'
    # 设置普通JWT过期时间
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=10)
    # 设置刷新JWT过期时间
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    # 设置cookie的过期时间
    JWT_SESSION_COOKIE_MAX_AGE = 691200  # 8 days
    # 是否开启CSRF保护
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_TOKEN_LOCATION = ["headers", "cookies", "json", "query_string"]
    JWT_COOKIE_SECURE = True

    # Snowflake ID Worker 参数
    SNOWFLAKE_DATACENTER_ID = 0
    SNOWFLAKE_WORKER_ID = 0
    SNOWFLAKE_SEQUENCE = 0

    # 热点数据是否过期
    HOT_DATA_EXPIRE = True
    # 热点数据默认过期时间
    HOT_DATA_EXPIRE_TIME = 5 * 60
    # 是否处理缓存雪崩，在热点数据允许过期的情况下，是否为过期时间增加一个随机增量
    DEAL_WITH_CACHE_AVALANCHE = True


class Website:
    name = '小说精品屋'
    domain = 'localhost'
    keyword = f'{name},小说,小说CMS,原创文学系统,开源小说系统,免费小说建站程序'
    description = f'{name}是一个多端（PC、WAP）阅读、功能完善的原创文学CMS系统，' \
                  f'由前台门户系统、作家后台管理系统、平台后台管理系统、爬虫管理系统等多个子系统构成，' \
                  f'支持会员充值、订阅模式、新闻发布和实时统计报表等功能，新书自动入库，老书自动更新。'
    qq = ''
    logo = 'https://youdoc.gitee.io/resource/images/logo/logo.png'


class BookPrice:
    # 字数
    word_count = 1000
    # 价值(屋币)
    value = 5
