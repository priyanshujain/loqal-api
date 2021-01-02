from django.utils.timezone import now
from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.user.dbapi import get_user_by_email_token
from apps.user.validators import EmailVerificationValidator

__all__ = ("EmailVerification",)


class EmailVerification(ServiceBase):
    def __init__(self, data):
        self.data = data

    def _validate_data(self):
        data = run_validator(
            validator=EmailVerificationValidator, data=self.data
        )

        token = data["token"]
        user = get_user_by_email_token(token=token)

        if not user:
            raise ValidationError(
                {"token": [ErrorDetail(_("Provided token is not valid."))]}
            )

        if user.email_verified:
            raise ValidationError(
                {"detail": ErrorDetail(_("Email has been already verified."))}
            )

        if user.email_verification_token_expire_time < now():
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _(
                            "Provided link has been expired. Please request email verification again."
                        )
                    )
                }
            )

        self.user = user

    def handle(self):
        self._validate_data()

        user = self.user
        user.verify_email()
        return True
