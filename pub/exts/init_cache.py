import redis

# 改为在redis_utils中获取实例
redis_client = redis.StrictRedis(host="127.0.0.1", port=6379, db=0)
