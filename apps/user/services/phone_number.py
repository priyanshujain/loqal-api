from django.conf import settings
from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.user.validators import PhoneNumberCodeValidator, PhoneNumberValidator
from apps.user.models import Authenticator


__all__ = (
    "AddPhoneNumber",
    "VerifyPhoneNumber",
)


class AddPhoneNumber(ServiceBase):
    def __init__(self, request, data):
        self.request = request
        self.data = data
        self.user = request.user

    def execute(self):
        data = self.data
        data = self._validate_data(data=data)

        phone_number = data["phone_number"]
        self.user.add_contact_number(phone_number=phone_number)
        EnrollSmsAuthenticator(request=self.request, user=self.user).enroll()

    def _validate_data(self, data):
        if self.user.phone_number:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _("Phone number has already been added.")
                    )
                }
            )
        return run_validator(validator=PhoneNumberValidator, data=data)


class EnrollSmsAuthenticator(object):
    def __init__(self, request, user):
        self.request = request
        self.user = user

    def get_interface(self):
        return Authenticator.objects.get_interface(self.user, "sms")
    
    def enroll(self):
        interface = self.get_interface()
        if interface.is_enrolled():
            raise ValidationError({
                "detail": ErrorDetail(_("User has already enrolled in sms auth."))
            })
        
        phone_number = getattr(self.user, "phone_number", None)
        if phone_number:
            interface.phone_number = phone_number
            interface.enroll(self.user)
            if interface.send_text(for_enrollment=True, request=self.request):
                return True
            else:
                # TODO: Add error check for SMS service failed ,500 error
                return False
        else:
            False


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
