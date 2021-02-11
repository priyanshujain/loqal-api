from django.contrib import auth
from django.contrib.auth import update_session_auth_hash
from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.user.dbapi import set_new_user_password
from apps.user.notifications import SendPasswordChangeAlert
from apps.user.validators import ForgotPasswordValidator

__all__ = ("ChangePassword",)


class ChangePassword(ServiceBase):
    def __init__(self, request, data, customer_type):
        self.request = request
        self.data = data
        self.customer_type = customer_type

    def _validate_data(self):
        request = self.request
        data = run_validator(validator=ForgotPasswordValidator, data=self.data)
        email = request.user.email
        username = f"{email}::{self.customer_type}"
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

    def handle(self):
        self._validate_data()
        session = self.request.session
        data = self.data
        user = self.user
        set_new_user_password(user=user, new_password=data["new_password"])
        SendPasswordChangeAlert(user=user, session=session).send()
        update_session_auth_hash(self.request, user)
