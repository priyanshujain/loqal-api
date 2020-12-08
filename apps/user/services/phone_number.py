from re import error

from django.conf import settings
from django.utils.translation import gettext as _
from rest_framework.utils.serializer_helpers import ReturnDict

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.user.models import Authenticator
from apps.user.validators import OtpAuthValidator, PhoneNumberValidator

__all__ = (
    "AddPhoneNumber",
    "VerifyPhoneNumber",
    "ResendPhoneNumberOtp",
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
        self.user.add_phone_number(phone_number=phone_number)
        EnrollSmsAuthenticator(request=self.request, user=self.user).send_otp()

    def _validate_data(self, data):
        if self.user.phone_number_verified:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _(
                            "Phone number can not be changed as it has already been verifed."
                        )
                    )
                }
            )
        return run_validator(validator=PhoneNumberValidator, data=data)


class VerifyPhoneNumber(ServiceBase):
    def __init__(self, user, request, data):
        self.user = user
        self.request = request
        self.data = data

    def execute(self):
        data = self._validate_data(data=self.data)
        otp = data["otp"]

        if EnrollSmsAuthenticator(
            request=self.request, user=self.user
        ).validate_otp(otp):
            self.user.verify_phone_number()
        else:
            raise ValidationError(
                {"code": ErrorDetail(_("Provided otp code does not match."))}
            )

    def _validate_data(self, data):
        if self.user.phone_number_verified:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _("Phone number has already been verified.")
                    )
                }
            )
        return run_validator(validator=OtpAuthValidator, data=data)


class ResendPhoneNumberOtp(object):
    def __init__(self, user, request):
        self.user = user
        self.request = request

    def handle(self):
        return EnrollSmsAuthenticator(
            request=self.request, user=self.user
        ).send_otp()


class EnrollSmsAuthenticator(object):
    def __init__(self, user, request, data={}):
        self.user = user
        self.request = request
        self.data = data

    def _validate_interface(self):
        interface = Authenticator.objects.get_interface(
            user=self.user, interface_id="sms"
        )
        phone_number = self.user.phone_number
        if not phone_number:
            raise ValidationError(
                {"detail": ErrorDetail(_("Phone number has not been added."))}
            )

        if interface.is_enrolled():
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _("Phone number has already been verified.")
                    )
                }
            )

        interface.phone_number = phone_number
        return interface

    def send_otp(self):
        interface = self._validate_interface()
        if interface.send_text(for_enrollment=True, request=self.request):
            return True
        else:
            # TODO: Add error check for SMS service failed ,500 error
            return False

    def validate_otp(self, otp):
        interface = self._validate_interface()

        # If dev environment validate otp by 222222
        error = False
        if settings.APP_ENV == "development":
            if otp == "222222":
                self.activate_interface(interface=interface)
                return True
            else:
                error = True

        if interface.validate_otp(otp):
            self.activate_interface(interface=interface)
            return True
        else:
            error = True

        if error:
            raise ValidationError(
                {
                    "otp": ErrorDetail(
                        _("Invalid confirmation code. Try again.")
                    )
                }
            )

    def activate_interface(self, interface):
        interface.enroll(self.user)
