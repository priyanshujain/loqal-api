from __future__ import absolute_import, division, print_function

from datetime import datetime

from django.utils import timezone



class InvalidQuery(Exception):
    pass


DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
DATETIME_FORMAT_MICROSECONDS = "%Y-%m-%dT%H:%M:%S.%f"


def parse_unix_timestamp(value):
    return datetime.utcfromtimestamp(float(value)).replace(tzinfo=timezone.utc)


def parse_datetime_string(value):
    # timezones are not supported and are assumed UTC
    if value[-1:] == "Z":
        value = value[:-1]
    if len(value) >= 6 and value[-6] == "+":
        value = value[:-6]

    for format in [DATETIME_FORMAT_MICROSECONDS, DATETIME_FORMAT, DATE_FORMAT]:
        try:
            return datetime.strptime(value, format).replace(tzinfo=timezone.utc)
        except ValueError:
            pass

    try:
        return parse_unix_timestamp(value)
    except ValueError:
        pass

    raise InvalidQuery(u"{} is not a valid ISO8601 date query".format(value))

