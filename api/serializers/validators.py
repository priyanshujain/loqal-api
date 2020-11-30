from datetime import datetime

from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError


def validate_date_format(date_string, format="%Y-%m-%d"):
    if not date_string:
        ValidationError({"detail": "Date value is required."})

    try:
        return datetime.strptime(date_string, format)
    except ValueError:
        ValidationError(
            {
                "detail": ErrorDetail(
                    _(
                        "This is the incorrect date format. "
                        "It should be YYYY-MM-DD."
                    )
                )
            }
        )
