from datetime import datetime, date, timedelta

import pytz
from flask import current_app


def get_past_date(past: int, date_: datetime) -> str:
    """
    获取过去第几天的日期
    :param past: 过去n天
    :param date_:
    :return:
    """
    return (date_ - timedelta(days=past)).date().strftime('%Y-%m-%d')


def get_date_list(past: int, date_: datetime) -> list:
    """
    获取过去几天的日期集合
    :param past:
    :param date_:
    :return:
    """
    result = []
    for i in range(past - 1, 0, -1):
        result.append(get_past_date(i, date_))
    # 今天的日期
    result.append(datetime.now().date().strftime('%Y-%m-%d'))

    return result


def set_timezone(obj: datetime, timezone: str = None) -> datetime:
    if timezone is None:
        timezone = current_app.config.get('TIMEZONE')
    return obj.astimezone(pytz.timezone(timezone)) if obj else obj


if __name__ == '__main__':
    print(get_date_list(7, datetime.now()))
