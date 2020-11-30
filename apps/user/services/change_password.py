from django.contrib import auth
from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.user.dbapi import set_new_user_password
from apps.user.notifications import SendPasswordChangeAlert
from apps.user.validators import ForgotPasswordValidator

__all__ = ("ChangePassword",)


class ChangePassword(ServiceBase):
    def __init__(self, request, data):
        self.request = request
        self.data = data

    def _validate_data(self):
        request = self.request
        data = run_validator(validator=ForgotPasswordValidator, data=self.data)
        username = request.user.username
        user = auth.authenticate(
            username=username, password=data["old_password"]
        )
        if not user:
            raise ValidationError(
                {
                    "old_password": [
                        ErrorDetail(_("Old password is not correct."))
                    ]
                }
            )

        if data["old_password"] == data["new_password"]:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _("Old password and new password can not be the same.")
                    )
                }
            )

        self.user = user

    def execute(self):
        self._validate_data()
        session = self.request.session
        data = self.data
        user = self.user
        set_new_user_password(user=user, new_password=data["new_password"])
        SendPasswordChangeAlert(user=user, session=session).send()
