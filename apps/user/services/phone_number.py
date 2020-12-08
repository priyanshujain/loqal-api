from django.conf import settings
from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.user.validators import PhoneNumberCodeValidator, PhoneNumberValidator

__all__ = (
    "AddPhoneNumber",
    "VerifyPhoneNumber",
)


class AddPhoneNumber(ServiceBase):
    def __init__(self, user, data):
        self.data = data
        self.user = user

    def execute(self):
        data = self.data
        data = self._validate_data(data=data)

        contact_number = data["contact_number"]
        self.user.add_contact_number(contact_number=contact_number)
        self._send_sms()

    def _validate_data(self, data):
        if self.user.contact_number:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _("Phone number has already been added.")
                    )
                }
            )
        return run_validator(validator=PhoneNumberValidator, data=data)

    def _send_sms(self):
        pass


class VerifyPhoneNumber(ServiceBase):
    def __init__(self, user, data):
        self.user = user
        self.data = data

    def execute(self):
        data = self._validate_data(data=self.data)
        code = data["code"]

        if settings.APP_ENV == "local" or settings.APP_ENV == "development":
            if code == "555555":
                self.user.verify_contact_number()
            else:
                raise ValidationError(
                    {"code": ErrorDetail(_("Provided code does not match."))}
                )
        else:
            raise ValidationError(
                {"detail": ErrorDetail(_("Not implmented."))}
            )

    def _validate_data(self, data):
        if self.user.contact_number_verified:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _("Phone number has already been verified.")
                    )
                }
            )
        return run_validator(validator=PhoneNumberCodeValidator, data=data)
