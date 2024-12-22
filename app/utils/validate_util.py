import re
from typing import Union

from app.utils import convert_string_to_datetime, convert_string_to_date


def validate_datetime_format(datetime_str: str) -> bool:
    pattern = r'^\d{2}:\d{2}:\d{2} \d{2}/\d{2}/\d{4}$'
    return re.match(pattern, datetime_str) is not None


def validate_date_format(date_str: str) -> bool:
    pattern = r'^\d{2}/\d{2}/\d{4}$'
    return re.match(pattern, date_str) is not None


def validate_datetime(name: str, value: str) -> (bool, Union[str, None]):
    if not validate_datetime_format(datetime_str=value):
        return False, f'{name} must be a valid format hh:mm:ss dd/mm/yyyy.'
    if not convert_string_to_datetime(datetime_str=value):
        return False, f'{name} must be a valid date.'
    return True, None


def validate_date(name: str, value: str) -> (bool, Union[str, None]):
    if not validate_date_format(date_str=value):
        return False, f'{name} must be a valid format dd/mm/yyyy.'
    if not convert_string_to_date(date_str=value):
        return False, f'{name} must be a valid date.'
    return True, None
