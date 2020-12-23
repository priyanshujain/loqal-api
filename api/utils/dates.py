from __future__ import absolute_import

from datetime import timedelta

import six
from django.utils import timezone

from .search import parse_datetime_string, InvalidQuery


MAX_STATS_PERIOD = timedelta(days=90)


class InvalidParams(Exception):
    pass

def default_start_end_dates(now=None):
    if now is None:
        now = timezone.now()
    return now - MAX_STATS_PERIOD, now


def get_date_range_from_params(params, optional=False):
    """
    Gets a date range from standard date range params we pass to the api.

    :param params:
    If `start` end `end` are passed, validate them, convert to `datetime` and
    returns them if valid.
    :param optional: When True, if no params passed then return `(None, None)`.
    :return: A length 2 tuple containing start/end or raises an `InvalidParams`
    exception
    """
    now = timezone.now()
    start, end = default_start_end_dates(now)

    if params.get("start") or params.get("end"):
        if not all([params.get("start"), params.get("end")]):
            raise InvalidParams("start and end are both required")
        try:
            start = parse_datetime_string(params["start"])
            end = parse_datetime_string(params["end"])
        except InvalidQuery as e:
            raise InvalidParams(six.text_type(e))
    elif optional:
        return None, None

    if start > end:
        raise InvalidParams("start must be before end")

    return start, end
