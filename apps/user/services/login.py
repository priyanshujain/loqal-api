from django.conf import settings
from django.utils.translation import gettext as _
from otpauth import OtpAuth

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.user.models import Authenticator
from apps.user.notifications import SendLoginAlert
from apps.user.validators import OtpAuthValidator, UserLoginValidator
from utils import auth

from .session import Session

__all__ = (
    "LoginRequest",
    "SmsOtpAuth",
    "ResendSmsOtpAuth",
)


class SmsOtpAuth(object):
    def __init__(self, user, request, data={}):
        self.user = user
        self.request = request
        self.data = data

    def _validate_interface(
        self,
    ):
        interface = Authenticator.objects.get_interface(
            user=self.user, interface_id="sms"
        )
        if not interface.is_enrolled():
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _("Phone number has not been verified.")
                    )
                }
            )
        return interface

    def send_otp(self):
        interface = self._validate_interface()
        interface.send_text(for_enrollment=False, request=self.request)

    def validate_otp(self):
        data = run_validator(validator=OtpAuthValidator, data=self.data)
        otp = self.data["otp"]

        interface = self._validate_interface()
        error = False
        # If dev environment validate otp by 222222
        if settings.APP_ENV == "developement":
            if otp == "222222":
                self.perform_login()
                return
            else:
                error = True

        if self.interface.validate_otp(otp):
            self.perform_login()
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

    def perform_login(self):
        auth.login(request=self.request, user=self.user, passed_2fa=True)
        self.interface.authenticator.mark_used()
        AfterLogin(request=self.request, user=self.user).handle()


class LoginRequest(ServiceBase):
    def __init__(self, request, data):
        self.request = request
        self.data = data

    def _validate_data(self, data):
        data = run_validator(validator=UserLoginValidator, data=data)

    def execute(self):
        data = self.data
        self._validate_data(data=data)
        user = auth.authenticate(
            email=data["email"], password=data["password"]
        )

        if user:
            if user.is_disabled:
                raise ValidationError(
                    {
                        "detail": ErrorDetail(
                            _("Your account has been disabled.")
                        )
                    }
                )

            if not user.two_factor_auth:
                return self._auth_login(user)

            if user.two_factor_auth and "tfa_code" not in data:
                raise ValidationError(
                    {"tfa_code": [ErrorDetail(_("This is required."))]}
                )

            if OtpAuth(user.tfa_token).valid_totp(data["tfa_code"]):
                return self._auth_login(user)
            else:
                raise ValidationError(
                    {
                        "tfa_code": [
                            ErrorDetail(
                                _("Invalid two factor authentication code.")
                            )
                        ]
                    }
                )
        else:
            raise ValidationError(
                {"detail": ErrorDetail(_("Invalid email or password."))}
            )

    def _auth_login(self, user):
        request = self.request
        if auth.login(request, user):
            AfterLogin(request=request, user=user).handle()
        else:
            SmsOtpAuth(user=user, request=self.request).send_otp()
            return {"otp_pending": True}


class ResendSmsOtpAuth(object):
    def __init__(self, request):
        self.request = request

    def handle(self):
        user = auth.get_pending_2fa_user(self.request)
        if not user:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _("User not found, please go to login page.")
                    )
                }
            )

        SmsOtpAuth(user=user, request=self.request).send_otp()


class AfterLogin(object):
    def __init__(self, request, user):
        self.user = user
        self.request = request

    def handle(self):
        Session(request=self.request).create_session(user=self.user)
        SendLoginAlert(user=self.user, session=self.request.session).send()
