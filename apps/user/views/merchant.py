import qrcode
from django.conf import settings
from django.utils.timezone import now
from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.views import APIView, MerchantAPIView
from apps.account.notifications import SendMerchantAccountVerifyEmail
from apps.user.notifications import SendMerchantResetPasswordEmail
from apps.user.options import CustomerTypes
from apps.user.services import (ApplyResetPassword, ChangePassword,
                                EmailVerification, LoginRequest,
                                RequestResetPassword)


class ResendEmailverificationAPI(MerchantAPIView):
    def post(self, request):
        user = request.user
        if user.email_verified:
            raise ValidationError(
                {"detail": ErrorDetail(_("Email has already verified."))}
            )
        if user.email_verification_token_expire_time < now():
            user.gen_email_verification_token()
        SendMerchantAccountVerifyEmail(user=user).send()
        return self.response()


class UserLoginAPI(APIView):
    throttle_scope = "login"

    def post(self, request):
        if request.user.is_authenticated:
            raise ValidationError(
                {"detail": ErrorDetail(_("You are already logged in."))}
            )
        session = request.session
        if session:
            session.set_expiry(settings.SESSION_INACTIVITY_EXPIRATION_DURATION)

        service_response = self._run_services(request=request)
        if service_response:
            return self.response(service_response)
        return self.response()

    def _run_services(self, request):
        service = LoginRequest(
            request=request,
            data=self.request_data,
            customer_type=CustomerTypes.MERCHANT,
        )
        return service.handle()


class RequestResetPasswordAPI(APIView):
    def post(self, request):
        try:
            reset_password_object = RequestResetPassword(
                request=request,
                data=self.request_data,
                customer_type=CustomerTypes.MERCHANT,
            ).handle()
            SendMerchantResetPasswordEmail(
                reset_password_object=reset_password_object
            ).send()
        except ValidationError as err:
            if err.detail.get("code") == "INVALID_EMAIL":
                return self.response()
            else:
                raise err
        return self.response()


class ApplyResetPasswordAPI(APIView):
    def post(self, request):
        self._run_services(request=request)
        return self.response()

    def _run_services(self, request):
        service = ApplyResetPassword(
            request=request,
            data=self.request_data,
            customer_type=CustomerTypes.MERCHANT,
        )
        service.handle()


class VerifyEmailAPI(APIView):
    def post(self, request):
        self._run_services()
        return self.response()

    def _run_services(self):
        service = EmailVerification(data=self.request_data)
        service.handle()


class UserChangePasswordAPI(MerchantAPIView):
    def post(self, request):
        """
        Changes user's password and asks him to login again.
        """
        self._run_services(request=request)
        return self.response()

    def _run_services(self, request):
        service = ChangePassword(
            request=request,
            data=self.request_data,
            customer_type=CustomerTypes.MERCHANT,
        )
        service.handle()
