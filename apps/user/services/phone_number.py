from django.conf import settings
from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.payment.dbapi import create_payment_request, get_pre_payment_request
from apps.user.dbapi import get_user_by_phone
from apps.user.models import Authenticator
from apps.user.options import CustomerTypes
from apps.user.validators import (PhoneNumberValidator,
                                  ResendPhoneNumberOtpValidator,
                                  VerifyPhoneNumberOtpValidator)

__all__ = (
    "StartSmsAuthEnrollment",
    "AddPhoneNumber",
    "VerifyPhoneNumber",
    "ResendPhoneNumberOtp",
)


class StartSmsAuthEnrollment(object):
    """
    TODO: look at this approach using secret from security standpoint
    """

    def __init__(self, request):
        self.user = request.user
        self.request = request

    def handle(self):
        return EnrollSmsAuthenticator(
            request=self.request, user=self.user
        ).request_enrollment()


class AddPhoneNumber(ServiceBase):
    def __init__(self, request, data):
        self.request = request
        self.data = data
        self.user = request.user

    def handle(self):
        data = self.data
        data = self._validate_data(data=data)

        phone_number = data["phone_number"]
        phone_number_country = data.get("phone_number_country", "US")
        self.user.add_phone_number(
            phone_number=phone_number,
            phone_number_country=phone_number_country,
        )
        EnrollSmsAuthenticator(
            request=self.request, user=self.user, data=data
        ).send_otp()

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
        data = run_validator(validator=PhoneNumberValidator, data=data)
        phone_number = data["phone_number"]
        phone_user = get_user_by_phone(
            phone_number=phone_number, customer_type=CustomerTypes.CONSUMER
        )
        if phone_user and phone_user.id != self.user.id:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _(
                            "User with this phone number already exist please use a different phone number."
                        )
                    )
                }
            )
        return data


class VerifyPhoneNumber(ServiceBase):
    def __init__(self, user, request, consumer_account, data):
        self.user = user
        self.request = request
        self.consumer_account = consumer_account
        self.data = data

    def handle(self):
        data = self._validate_data(data=self.data)
        otp = data["otp"]

        if EnrollSmsAuthenticator(
            request=self.request, user=self.user, data=data
        ).validate_otp(otp):
            self.user.verify_phone_number()
            self._create_pending_payment_request()
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
        return run_validator(
            validator=VerifyPhoneNumberOtpValidator, data=data
        )

    def _create_pending_payment_request(self):
        consumer_account = self.consumer_account
        pre_payment_requests = get_pre_payment_request(
            phone_number=consumer_account.user.phone_number,
            phone_number_country=consumer_account.user.phone_number_country,
        )
        for pre_payment_request in pre_payment_requests:
            register_id = None
            if pre_payment_request.register:
                register_id = pre_payment_request.register.id
            create_payment_request(
                account_from_id=pre_payment_request.merchant.account.id,
                account_to_id=consumer_account.account.id,
                amount=pre_payment_request.amount,
                register_id=register_id,
            )


class ResendPhoneNumberOtp(object):
    def __init__(self, user, request, data):
        self.user = user
        self.request = request
        self.data = data

    def _validate_data(self):
        return run_validator(ResendPhoneNumberOtpValidator, data=self.data)

    def handle(self):
        data = self._validate_data()
        return EnrollSmsAuthenticator(
            request=self.request, user=self.user, data=data
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
        if interface.is_enrolled():
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _("Phone number has already been verified.")
                    )
                }
            )
        return interface

    def _validate_data(
        self,
    ):
        interface = self._validate_interface()
        try:
            interface.secret = self.data["secret"]
        except KeyError:
            raise ValidationError(
                {
                    "secret": ErrorDetail(
                        _("Please call request enrollment to get secret.")
                    )
                }
            )

        phone_number = self.user.phone_number
        phone_number_verified = self.user.phone_number_verified
        if not phone_number:
            raise ValidationError(
                {"detail": ErrorDetail(_("Phone number has not been added."))}
            )
        if phone_number_verified:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _("Phone number has already been verified.")
                    )
                }
            )
        interface.phone_number = phone_number
        interface.phone_number_country = self.user.phone_number_country
        return interface

    def request_enrollment(self):
        interface = self._validate_interface()
        return interface.secret

    def send_otp(self):
        interface = self._validate_data()
        if interface.send_text(for_enrollment=True, request=self.request):
            return True
        else:
            # TODO: Add error check for SMS service failed ,500 error
            return False

    def validate_otp(self, otp):
        interface = self._validate_data()

        # If dev environment validate otp by 222222
        if settings.APP_ENV == "development":
            if otp == "222222":
                self._enroll_interface(interface=interface)
                return True
            else:
                return False

        if settings.APP_ENV == "staging":
            if otp == "111111":
                self._enroll_interface(interface=interface)
                return True
            else:
                return False

        if interface.validate_otp(otp):
            self._enroll_interface(interface)
            return True

    def _enroll_interface(self, interface):
        interface.enroll(self.user)
