import logging
import time

from apps.front import FrontConfig
from pub.consts import RedisKey
from pub.exts.init_cache import redis_client
from pub.utils.redis_utils import with_redis_lock


class InvalidSystemClock(Exception):
    """
    时钟回拨异常
    """
    pass


# 64位ID的划分
WORKER_ID_BITS = 5
DATACENTER_ID_BITS = 5
SEQUENCE_BITS = 12

# 最大取值计算
MAX_WORKER_ID = -1 ^ (-1 << WORKER_ID_BITS)  # 2**5-1 0b11111
MAX_DATACENTER_ID = -1 ^ (-1 << DATACENTER_ID_BITS)

# 移位偏移计算
WOKER_ID_SHIFT = SEQUENCE_BITS
DATACENTER_ID_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS
TIMESTAMP_LEFT_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS + DATACENTER_ID_BITS

# 序号循环掩码
SEQUENCE_MASK = -1 ^ (-1 << SEQUENCE_BITS)

# Twitter元年时间戳
TWEPOCH = 1288834974657

logger = logging.getLogger('flask.app')


class IdWorker(object):
    """
    用于生成IDs
    """

    def __init__(self, datacenter_id, worker_id, sequence=0):
        """
        初始化
        :param datacenter_id: 数据中心（机器区域）ID
        :param worker_id: 机器ID
        :param sequence: 起始序号f
        """
        # sanity check
        if worker_id > MAX_WORKER_ID or worker_id < 0:
            raise ValueError('worker_id值越界')

        if datacenter_id > MAX_DATACENTER_ID or datacenter_id < 0:
            raise ValueError('datacenter_id值越界')

        self.worker_id = worker_id
        self.datacenter_id = datacenter_id
        # self.sequence = sequence
        redis_client.set(RedisKey.SNOW_FLAKE_CACHE + f':{self.datacenter_id}:{self.worker_id}:sequence', sequence)

        # self.last_timestamp = -1  # 上次计算的时间戳
        redis_client.set(RedisKey.SNOW_FLAKE_CACHE + f':{self.datacenter_id}:{self.worker_id}:last_timestamp', -1)

    @staticmethod
    def _gen_timestamp():
        """
        生成整数时间戳
        :return:int timestamp
        """
        return int(time.time() * 1000)

    @property
    def last_timestamp(self):
        value = redis_client.get(RedisKey.SNOW_FLAKE_CACHE + f':{self.datacenter_id}:{self.worker_id}:last_timestamp')
        return int(value.decode('utf-8'))

    def set_last_timestamp(self, timestamp):
        redis_client.set(RedisKey.SNOW_FLAKE_CACHE + f':{self.datacenter_id}:{self.worker_id}:last_timestamp',
                         timestamp)

    @property
    def sequence(self):
        value = redis_client.get(RedisKey.SNOW_FLAKE_CACHE + f':{self.datacenter_id}:{self.worker_id}:sequence')
        return int(value.decode('utf-8'))

    def set_sequence(self, sequence):
        redis_client.set(RedisKey.SNOW_FLAKE_CACHE + f':{self.datacenter_id}:{self.worker_id}:sequence', sequence)

    @with_redis_lock('snow_flake_lock', timeout=5, blocking=True, sleep=0.1, blocking_timeout=10)
    def get_id(self):
        """
        获取新ID
        :return:
        """
        timestamp = self._gen_timestamp()

        # 时钟回拨
        if timestamp < self.last_timestamp:
            logging.error('clock is moving backwards. Rejecting requests until {}'.format(self.last_timestamp))
            raise InvalidSystemClock

        if timestamp == self.last_timestamp:
            self.set_sequence((self.sequence + 1) & SEQUENCE_MASK)
            if self.sequence == 0:
                timestamp = self._til_next_millis(self.last_timestamp)
        else:
            self.set_sequence(0)

        self.set_last_timestamp(timestamp)

        new_id = ((timestamp - TWEPOCH) << TIMESTAMP_LEFT_SHIFT) | (self.datacenter_id << DATACENTER_ID_SHIFT) | \
                 (self.worker_id << WOKER_ID_SHIFT) | self.sequence

        return new_id

    def _til_next_millis(self, last_timestamp):
        """
        等到下一毫秒
        """
        timestamp = self._gen_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._gen_timestamp()
        return timestamp


safe_id_worker = IdWorker(FrontConfig.SNOWFLAKE_DATACENTER_ID, FrontConfig.SNOWFLAKE_WORKER_ID,
                          FrontConfig.SNOWFLAKE_SEQUENCE)

if __name__ == '__main__':
    print(safe_id_worker.get_id())
    print(safe_id_worker.get_id())
    print(safe_id_worker.get_id())
    print(safe_id_worker.get_id())
    print(safe_id_worker.get_id())
