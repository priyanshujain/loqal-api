from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from apps.account.dbapi import check_account_username
from apps.account.validators import ConsumerUsernameValidator

__all__ = (
    "ChangeAccountUsername",
    "CheckAccountUsername",
)


class CheckAccountUsername(object):
    def __init__(self, consumer_account, data):
        self.data = data
        self.consumer_account = consumer_account

    def handle(self):
        username = run_validator(ConsumerUsernameValidator, data=self.data)[
            "username"
        ]
        if username == self.consumer_account.username:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _(
                            "This is your current loqal ID. "
                            "Please choose a different one to"
                            " change your current Loqal ID."
                        )
                    ),
                    "message": ErrorDetail(
                        _("You already use this username.")
                    ),
                }
            )
        if check_account_username(username=username):
            return {"available": False}
        return {"available": True}


class ChangeAccountUsername(object):
    def __init__(self, consumer_account, data):
        self.data = data
        self.consumer_account = consumer_account

    def handle(self):
        username = run_validator(ConsumerUsernameValidator, data=self.data)[
            "username"
        ]
        if username == self.consumer_account.username:
            raise ValidationError(
                {"detail": ErrorDetail(
                        _(
                            "This is your current loqal ID. "
                            "Please choose a different one to change"
                            " your current Loqal ID."
                        )
                    )}
            )
        if check_account_username(username=username):
            raise ValidationError(
                {
                    "username": ErrorDetail(
                        _(
                            "This Loqal ID already exists with another user,"
                            " please choose a different one."
                        )
                    )
                }
            )

        self.consumer_account.change_username(username)
