from datetime import datetime, date, time
from typing import Union

import pytz
from django.conf import settings
from django.utils import timezone


def convert_timezone(old_time: datetime, new_timezone: str = settings.TIME_ZONE) -> datetime:
    if timezone.is_naive(old_time):
        old_time = timezone.make_aware(old_time, timezone=pytz.timezone(settings.TIME_ZONE))

    target_timezone = pytz.timezone(new_timezone)
    return old_time.astimezone(target_timezone)


def convert_string_to_datetime(datetime_str: str) -> Union[datetime, None]:
    try:
        datetime_obj = datetime.strptime(datetime_str, '%H:%M:%S %d/%m/%Y')
        return convert_timezone(old_time=datetime_obj)
    except ValueError as e:
        return None


def convert_string_to_date(date_str: str) -> Union[date, None]:
    try:
        return datetime.strptime(date_str, '%d/%m/%Y').date()
    except ValueError as e:
        return None


def convert_datetime_to_string(datetime_value: datetime) -> str:
    datetime_value = convert_timezone(old_time=datetime_value)
    return datetime_value.strftime('%H:%M:%S %d/%m/%Y')


def convert_date_to_string(date_value: date) -> str:
    return date_value.strftime('%d/%m/%Y')


def convert_time_to_string(time_value: time) -> str:
    return time_value.strftime('%H:%M:%S')


def convert_date_to_day_of_week(date_value: date) -> str:
    return date_value.strftime('%a').upper()
