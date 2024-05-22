from functools import wraps

from flask import current_app

from pub.exts.init_cache import redis_client
import random


def with_redis_lock(lock_name: str, timeout: int = 5, blocking: bool = True, sleep: float = 0.1,
                    blocking_timeout: int = 10):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with redis_client.lock(lock_name, timeout=timeout, blocking=blocking, sleep=sleep,
                                   blocking_timeout=blocking_timeout):
                return func(*args, **kwargs)

        return wrapper

    return decorator


class Redis(object):
    @classmethod
    def set(cls, key: str, value):
        redis_client.set(key, value)

    @classmethod
    def set_and_expire(cls, key: str, value, expire: int, random_beg=None, random_end=None, random_base_expire=False):
        """
        设置key并指定过期时间
        :param key: 键
        :param value: 值
        :param expire: 过期时间
        :param random_beg: 过期随机增量最小值（起始值），用于防止缓存雪崩情况的出现
        :param random_end: 过期随机增量最大值（终止值），用于防止缓存雪崩情况的出现
        :param random_base_expire: （在未指定random_beg和/或random_end的情况下）过期随机增量是否根据expire生成，用于防止缓存雪崩情况的出现
        :return:
        """
        time_delta = 0
        if random_beg is None:
            if random_end is None:
                time_delta = random.randint(0, expire) if random_base_expire else 0
            else:
                time_delta = random.randint(0, random_end) if random_end > 0 else 0
        else:
            if random_end is None:
                time_delta = random.randint(random_beg, expire) if random_base_expire and random_beg <= expire else 0
            else:
                time_delta = random.randint(random_beg if random_beg >= 0 else 0, random_end) \
                    if (random_end >= random_beg) else 0

        expire += time_delta

        if expire <= 0:
            expire = None
        redis_client.set(key, value, ex=expire)

    @classmethod
    def set_hot_key(cls, redis_key: str, json_data):
        if not current_app.config['HOT_DATA_EXPIRE']:
            Redis.set(redis_key, json_data)
        else:
            expire = current_app.config['HOT_DATA_EXPIRE_TIME'] if current_app.config[
                'HOT_DATA_EXPIRE_TIME'] else 5 * 60
            if current_app.config['DEAL_WITH_CACHE_AVALANCHE']:
                Redis.set_and_expire(redis_key, json_data, expire, random_base_expire=True)
            else:
                Redis.set_and_expire(redis_key, json_data, expire)

    @classmethod
    def get(cls, key: str, default=''):
        value = redis_client.get(key)
        if value:
            return value.decode('utf-8')
        else:
            return default

    @classmethod
    def get_expire(cls, key: str):
        return redis_client.ttl(key)

    @classmethod
    def delete(cls, names):
        if isinstance(names, int) or isinstance(names, str) or isinstance(names, float):
            redis_client.delete(names)
        elif isinstance(names, tuple) or isinstance(names, list) or isinstance(names, set):
            redis_client.delete(*names)
        else:
            raise TypeError("类型错误，仅支持传入int、str、float、tuple、list、set类型")

    @classmethod
    def keys(cls, pattern: str):
        if not pattern.endswith('*'):
            pattern += '*'

        keys = redis_client.keys(pattern)

        return keys

    @classmethod
    def keys_transfer(cls, pattern: str):
        if not pattern.endswith('*'):
            pattern += '*'

        keys = redis_client.keys(pattern)

        ret_keys = []
        if keys and len(keys) > 0:
            for k in keys:
                ret_keys.append(k.decode('utf-8'))

        return ret_keys

    @classmethod
    def caches(cls, prefix: str):
        keys = cls.keys(prefix + '*')
        # print(keys)
        caches = []
        if keys and len(keys) > 0:
            for k in keys:
                caches.append(dict(key=k.decode('utf-8'), value=cls.get(k)))
        return caches

    @classmethod
    def hset(cls, name, key, data):
        # print(type(key))
        redis_client.hset(name, key, data)

    @classmethod
    def hget(cls, name, key):
        data = redis_client.hget(name, key)
        # print(data)

        return data.decode('utf8') if data else None

    @classmethod
    def hgetall(cls, name):
        datas = redis_client.hgetall(name)
        ret = {k.decode('utf8'): v.decode('utf8') for k, v in datas.items()}
        # print(ret)
        return ret

    @classmethod
    def hdelete(cls, name, keys):
        if isinstance(keys, int) or isinstance(keys, str) or isinstance(keys, float):
            redis_client.hdel(name, keys)
        elif isinstance(keys, tuple) or isinstance(keys, list) or isinstance(keys, set):
            redis_client.hdel(name, *keys)
        else:
            raise TypeError("类型错误，仅支持传入int、str、float、tuple、list、set类型")
