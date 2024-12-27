from datetime import datetime, timezone
import math

"""
获取当前时间戳各语言语法
Java语法
// pure java
System.currentTimeMillis() / 1000

// joda java
DateTime.now().getMillis() / 1000

// java >= 8
Instant.now().getEpochSecond()

python语法

import time
time.time()

import arrow
arrow.utcnow().timestamp

MySQL语法

SELECT unix_timestamp(now())

JavaScript语法

Math.round(new Date() / 1000)
"""


def separate_timestamp(timestamp):
    """将浮点数时间戳分离为秒和毫秒"""
    seconds = math.floor(timestamp)  # 秒部分
    milliseconds = int((timestamp - seconds) * 1000)  # 毫秒部分
    return seconds, milliseconds


def timestamp_to_datetime_and_separate(timestamp):
    """将时间戳（秒+毫秒）转换为日期时间，并分离秒和毫秒"""
    try:
        dt_utc = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        seconds, milliseconds = separate_timestamp(timestamp)
        return dt_utc, seconds, milliseconds
    except (TypeError, OSError) as e:
        raise ValueError(f"Invalid timestamp: {e}")


def datetime_to_timestamp_and_separate(dt):
    """将日期时间转换为时间戳（秒+毫秒），并分离秒和毫秒"""
    if not isinstance(dt, datetime):
        raise ValueError("Input must be a datetime object")
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    try:
        timestamp = dt.timestamp()  # 返回带小数的秒数，即包含毫秒
        seconds, milliseconds = separate_timestamp(timestamp)
        return seconds, milliseconds
    except (TypeError, OSError) as e:
        raise ValueError(f"Invalid datetime: {e}")


def main():
    # 示例时间戳（包含毫秒）
    example_timestamp = 1672531200.123456  # 2023-01-01 00:00:00.123456 UTC
    print(f"原始时间戳（包含毫秒）: {example_timestamp}")  # <<<<< 填写未转化时间戳的地方

    # 时间戳转日期时间并分离秒和毫秒
    converted_datetime, seconds, milliseconds = timestamp_to_datetime_and_separate(example_timestamp)
    print(f"时间戳转换为日期时间（带毫秒）: {converted_datetime}")
    print(f"分离出的秒部分: {seconds}")  # <<<<< 转化后的时间戳秒
    print(f"分离出的毫秒部分: {milliseconds}")  # <<<<< 转化后的时间戳毫秒

    # 示例日期时间字符串（包含毫秒）
    # 下面是填写年月日时分秒的地方，格式为 "YYYY-MM-DD HH:MM:SS":
    datetime_str = "2024-12-27 13:56:15"  # <<<<< 填写未转化的日期时间字符串
    format_str = "%Y-%m-%d %H:%M:%S"  # 定义日期时间字符串的格式

    # 解析日期时间字符串为 datetime 对象
    try:
        example_datetime = datetime.strptime(datetime_str, format_str).replace(tzinfo=timezone.utc)
        print(f"从字符串解析得到的日期时间: {example_datetime}")

        # 日期时间转时间戳（包含毫秒），并分离秒和毫秒
        # 这里是填写已经转化为时间戳的入口：
        converted_seconds, converted_milliseconds = datetime_to_timestamp_and_separate(example_datetime)
        print(f"日期时间转换为时间戳 - 秒部分: {converted_seconds}")  # <<<<< 已经转化为时间戳秒
        print(f"日期时间转换为时间戳 - 毫秒部分: {converted_milliseconds}")  # <<<<< 已经转化为时间戳毫秒
    except ValueError as e:
        print(f"Error parsing datetime string: {e}")


if __name__ == "__main__":
    main()
