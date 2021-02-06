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
                            "This is your current username. "
                            "Please choose a different username."
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
                {"detail": ErrorDetail(_("You already have this username."))}
            )
        if check_account_username(username=username):
            raise ValidationError(
                {
                    "username": ErrorDetail(
                        _(
                            "This username already exists, please choose a different one."
                        )
                    )
                }
            )

        self.consumer_account.change_username(username)
