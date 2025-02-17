from __future__ import absolute_import

import calendar
import re
from datetime import datetime, timedelta

import pytz
import six
from dateutil.parser import parse
from django.db import connections
from rest_framework import ISO_8601

DATE_TRUNC_GROUPERS = {"date": "day", "hour": "hour", "minute": "minute"}

epoch = datetime(1970, 1, 1, tzinfo=pytz.utc)


def to_timestamp(value):
    """
    Convert a time zone aware datetime to a POSIX timestamp (with fractional
    component.)
    """
    return (value - epoch).total_seconds()


def to_datetime(value):
    """
    Convert a POSIX timestamp to a time zone aware datetime.

    The timestamp value must be a numeric type (either a integer or float,
    since it may contain a fractional component.)
    """
    if value is None:
        return None

    return epoch + timedelta(seconds=value)


def floor_to_utc_day(value):
    """
    Floors a given datetime to UTC midnight.
    """
    return value.astimezone(pytz.utc).replace(
        hour=0, minute=0, second=0, microsecond=0
    )


def get_sql_date_trunc(col, db="default", grouper="hour"):
    conn = connections[db]
    method = DATE_TRUNC_GROUPERS[grouper]
    return conn.ops.date_trunc_sql(method, col)


def parse_date(datestr, timestr):
    # format is Y-m-d
    if not (datestr or timestr):
        return
    if not timestr:
        return datetime.strptime(datestr, "%Y-%m-%d")

    datetimestr = datestr.strip() + " " + timestr.strip()
    try:
        return datetime.strptime(datetimestr, "%Y-%m-%d %I:%M %p")
    except Exception:
        try:
            return parse(datetimestr)
        except Exception:
            return


def parse_timestamp(value):
    # TODO(mitsuhiko): merge this code with coreapis date parser
    if isinstance(value, datetime):
        return value
    elif isinstance(value, six.integer_types + (float,)):
        return datetime.utcfromtimestamp(value).replace(tzinfo=pytz.utc)
    value = (value or "").rstrip("Z").encode("ascii", "replace").split(b".", 1)
    if not value:
        return None
    try:
        rv = datetime.strptime(value[0].decode("ascii"), "%Y-%m-%dT%H:%M:%S")
    except Exception:
        return None
    if len(value) == 2:
        try:
            rv = rv.replace(microsecond=int(value[1].ljust(6, b"0")[:6]))
        except ValueError:
            rv = None
    return rv.replace(tzinfo=pytz.utc)


def parse_stats_period(period):
    """
    Convert a value such as 1h into a
    proper timedelta.
    """
    m = re.match("^(\d+)([hdmsw]?)$", period)
    if not m:
        return None
    value, unit = m.groups()
    value = int(value)
    if not unit:
        unit = "s"
    return timedelta(
        **{
            {
                "h": "hours",
                "d": "days",
                "m": "minutes",
                "s": "seconds",
                "w": "weeks",
            }[unit]: value
        }
    )


def datetime_format(dt):
    value = dt.isoformat()
    if value.endswith("+00:00"):
        value = value[:-6] + "Z"
    return value


def dt_add_months(dt, months):
    month = dt.month - 1 + months
    year = dt.year + month // 12
    month = month % 12 + 1
    day = min(dt.day, calendar.monthrange(year, month)[1])
    return dt.replace(year=year, month=month, day=day)
