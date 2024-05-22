CACHE_COMMON_PREFIX = 'NovelFlask'

# 缓存存在的最小长度
OBJECT_JSON_CACHE_EXIST_LENGTH = 5
# 首页设置的小说数量
INDEX_BOOK_SETTING_NUM = 31


class RedisKey:
    SYS_CACHE = CACHE_COMMON_PREFIX + ':sys'

    BUSINESS_CACHE = CACHE_COMMON_PREFIX + ':business'

    SNOW_FLAKE_CACHE = CACHE_COMMON_PREFIX + ':snowflake'

    # 首页小说设置
    INDEX_BOOK_SETTINGS_KEY = BUSINESS_CACHE + ':indexBookSettingsKey'
    # 首页新闻
    INDEX_NEWS_KEY = BUSINESS_CACHE + ':indexNewsKey'
    # 首页点击榜单
    INDEX_CLICK_BANK_BOOK_KEY = BUSINESS_CACHE + ':indexClickBankBookKey'
    # 首页友情链接
    INDEX_LINK_KEY = BUSINESS_CACHE + ':indexLinkKey'
    # 首页新书榜单
    INDEX_NEW_BOOK_KEY = BUSINESS_CACHE + ':indexNewBookKey'
    # 首页更新榜单
    INDEX_UPDATE_BOOK_KEY = BUSINESS_CACHE + ':indexUpdateBookKey'

    VALIDATE_CODE_CACHE = CACHE_COMMON_PREFIX + ':randomValidateCodeKey'
