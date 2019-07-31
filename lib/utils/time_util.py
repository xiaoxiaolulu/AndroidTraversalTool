# -*- coding:utf-8 -*-
import time
import datetime


def timeStamp(format_key: str) -> str:
    r"""格式化时间

    :Args:
     - format_key: 转化格式方式, str object.
    """
    format_time = {
        'default':
            {
                'format_day': '%Y-%m-%d',
                'format_now': '%Y-%m-%d-%H_%M_%S',
                'unix_now': '%Y-%m-%d %H:%M:%S',
            }
    }
    try:
        time_stamp = time.strftime(format_time['default'][format_key], time.localtime(time.time()))
        return time_stamp
    except KeyError:
        pass


def timeUnix() -> int:
    r"""转化为时间蹉
    """
    unix = int(time.mktime(time.strptime(timeStamp('unix_now'), "%Y-%m-%d %H:%M:%S")))
    return unix


def time_difference(day: int) -> str:
    r"""时间差计算，根据当前时间累加days

    :Args:
     - days: 相差多少天, str object.
    """
    difference = (datetime.datetime.now() + datetime.timedelta(days=day)).strftime("%Y-%m-%d %H:%M:%S")
    return difference
