from django.contrib import auth
from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.user.dbapi import (gen_reset_password_token,
                             get_reset_password_object_by_token,
                             get_user_by_email, set_new_user_password)
from apps.user.validators import (ApplyResetPasswordValidator,
                                  RequestResetPasswordValidator,
                                  ResetPasswordTokenValidator)
from apps.user.notifications import SendPasswordChangeAlert


__all__ = (
    "RequestResetPassword",
    "ResetPasswordTokenValidate",
    "ApplyResetPassword",
)


class RequestResetPassword(ServiceBase):
    def __init__(self, request, data):
        self.request = request
        self.data = data
        self.user = request.user

    def _validate_data(self):
        data = run_validator(
            validator=RequestResetPasswordValidator, data=self.data
        )

        user = self.user
        if user.is_authenticated:
            raise ValidationError(
                {"detail": ErrorDetail(_("You are already logged in."))}
            )

        user = get_user_by_email(email=data["email"])
        if not user:
            raise ValidationError(
                {
                    "email": [
                        ErrorDetail(_("User does not exist with this email."))
                    ]
                }
            )
        self.user = user

    def handle(self):
        self._validate_data()
        user = self.user
        return gen_reset_password_token(user_id=user.id)


class ResetPasswordTokenValidate(ServiceBase):
    def __init__(self, request, data):
        self.request = request
        self.data = data
        self.user = request.user

    def _validate_token(self, token):
        token_object = get_reset_password_object_by_token(token=token)
        if not token_object:
            raise ValidationError(
                {"token": [ErrorDetail(_("Provided token is not valid."))]}
            )

        if token_object.is_expired:
            raise ValidationError(
                {"token": [ErrorDetail(_("Provided token is expired."))]}
            )
        return token_object

    def _check_if_authenticated(self):
        user = self.user
        if user.is_authenticated:
            raise ValidationError(
                {"detail": ErrorDetail(_("You are already logged in."))}
            )

    def _validate_data(self):
        data = run_validator(
            validator=ResetPasswordTokenValidator, data=self.data
        )
        token = data["token"]
        self._check_if_authenticated()
        token_object = self._validate_token(token=token)
        return token_object

    def handle(self):
        self._validate_data()


class ApplyResetPassword(ResetPasswordTokenValidate):
    def __init__(self, request, data):
        self.request = request
        self.data = data
        self.user = request.user

    def _check_if_old_password_used(self, email, password):
        user = auth.authenticate(email=email, password=password)
        if user:
            raise ValidationError(
                {
                    "password": [
                        ErrorDetail(
                            _("Please do not old password as new password.")
                        )
                    ]
                }
            )

    def _validate_data(self):
        data = run_validator(
            validator=ApplyResetPasswordValidator, data=self.data
        )
        token = data["token"]
        self._check_if_authenticated()
        token_object = self._validate_token(token=token)
        self._check_if_old_password_used(
            email=token_object.user.email, password=data["password"]
        )
        return token_object

    def handle(self):
        token_object = self._validate_data()

        user = token_object.user
        session = self.request.session
        data = self.data
        password = data["password"]
        set_new_user_password(user=user, new_password=password)

        token_object.expire_token()
        SendPasswordChangeAlert(user=user, session=session).send()
