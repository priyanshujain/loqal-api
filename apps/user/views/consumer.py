from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.utils.translation import gettext as _
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.parsers import MultiPartParser

from api.exceptions import ErrorDetail, ValidationError
from api.views import (APIView, ConsumerAPIView, ConsumerPre2FaAPIView,
                       LoggedInAPIView)
from apps.account.notifications import SendConsumerAccountVerifyEmail
from apps.notification.tasks import SendEmailVerifiedNotification
from apps.user.notifications import SendConsumerResetPasswordEmail
from apps.user.options import CustomerTypes
from apps.user.responses import UserProfileResponse
from apps.user.services import (AddChangeUserAvatar, AddPhoneNumber,
                                ApplyResetPassword, ChangePassword,
                                EmailVerification, LoginRequest,
                                RequestResetPassword, ResendPhoneNumberOtp,
                                ResendSmsOtpAuth, SmsOtpAuth,
                                StartSmsAuthEnrollment, VerifyPhoneNumber)
from utils import auth


class GetUserProfileAPI(APIView):
    """
    Get user profile API
    - View user profile.
    - Also used for checking if user is logged In.
    """

    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        # TODO: Revisit status of this API, discuss with @adi
        user = request.user
        if not user.is_authenticated:
            return self.response()

        return self.response(UserProfileResponse(user).data)


class ResendEmailverificationAPI(ConsumerAPIView):
    def post(self, request):
        user = request.user
        if user.email_verified:
            raise ValidationError(
                {"detail": ErrorDetail(_("Email has already verified."))}
            )
        if user.email_verification_token_expire_time < now():
            user.gen_email_verification_token()
        SendConsumerAccountVerifyEmail(user=user).send()
        return self.response()


class UserLoginAPI(APIView):
    throttle_scope = "login"

    def post(self, request):
        if request.user.is_authenticated:
            raise ValidationError(
                {"detail": ErrorDetail(_("You are already logged in."))}
            )

        service_response = self._run_services(request=request)

        if service_response:
            session = request.session
            # Assign the 7 days expiration period
            if session:
                session.set_expiry(60 * 60 * 24 * 7)
            return self.response(service_response)
        return self.response()

    def _run_services(self, request):
        service = LoginRequest(
            request=request,
            data=self.request_data,
            customer_type=CustomerTypes.CONSUMER,
        )
        return service.handle()


class SmsOtpAuthAPI(APIView):
    """
    Validate sms otp after email and password verification
    """

    def post(self, request):
        if request.user.is_authenticated:
            raise ValidationError(
                {"detail": ErrorDetail(_("You are already logged in."))}
            )

        user = auth.get_pending_2fa_user(request)
        if not user:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _("User not found, please go to login page.")
                    )
                }
            )
        self._run_services(user=user)
        return self.response()

    def _run_services(self, user):
        is_valid = SmsOtpAuth(
            user=user, request=self.request, data=self.request_data
        ).validate_otp()
        if not is_valid:
            raise ValidationError(
                {"otp": [ErrorDetail(_("Otp is not valid or expired."))]}
            )


class ResendSmsOtpAuthAPI(APIView):
    """
    Resend sms otp after email and password verification
    """

    def post(self, request):
        if request.user.is_authenticated:
            raise ValidationError(
                {"detail": ErrorDetail(_("You are already logged in."))}
            )
        self._run_services()
        return self.response()

    def _run_services(self):
        ResendSmsOtpAuth(request=self.request).handle()


class ResendPhoneNumberVerifyOtpAPI(ConsumerPre2FaAPIView):
    """
    Resend sms otp for phone number verification
    """

    def post(self, request):
        user = request.user
        self._run_services(user=user)
        return self.response()

    def _run_services(self, user):
        ResendPhoneNumberOtp(
            user=user, request=self.request, data=self.request_data
        ).handle()


class AddPhoneNumberAPI(ConsumerPre2FaAPIView):
    def post(self, request):
        self._run_services()
        return self.response()

    def _run_services(self):
        service = AddPhoneNumber(request=self.request, data=self.request_data)
        service.handle()


class StartSmsAuthEnrollmentAPI(ConsumerPre2FaAPIView):
    def post(self, request):
        enrollment_secret = self._run_services()
        return self.response({"secret": enrollment_secret})

    def _run_services(self):
        service = StartSmsAuthEnrollment(request=self.request)
        return service.handle()


class VerifyPhoneNumberAPI(ConsumerPre2FaAPIView):
    def post(self, request):
        self._run_services(user=request.user)
        return self.response()

    def _run_services(self, user):
        service = VerifyPhoneNumber(
            user=user, request=self.request, data=self.request_data
        )
        service.handle()


class RequestResetPasswordAPI(APIView):
    def post(self, request):
        try:
            reset_password_object = RequestResetPassword(
                request=request,
                data=self.request_data,
                customer_type=CustomerTypes.CONSUMER,
            ).handle()
            SendConsumerResetPasswordEmail(
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
            customer_type=CustomerTypes.CONSUMER,
        )
        service.handle()


class VerifyEmailAPI(APIView):
    def post(self, request):
        self._run_services(request)
        return self.response()

    def _run_services(self, request):
        service = EmailVerification(data=self.request_data)
        user = service.handle()
        if user:
            device_id = request.session.get("device_id")
            SendEmailVerifiedNotification(
                user_id=user.id, device_id=device_id
            ).send()


class UserChangePasswordAPI(LoggedInAPIView):
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
            customer_type=CustomerTypes.CONSUMER,
        )
        service.handle()


class UploadAvatarFileAPI(ConsumerAPIView):
    parser_classes = (MultiPartParser,)

    def post(self, request):
        AddChangeUserAvatar(request=request).handle()
        return self.response()
