import qrcode
from django.conf import settings
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.utils.translation import gettext as _
from django.views.decorators.csrf import ensure_csrf_cookie
from otpauth import OtpAuth

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.views import APIView, LoggedInAPIView
from apps.account.notifications import SendAccountVerifyEmail
from apps.user.dbapi import get_user_by_email, update_user_profile
from apps.user.responses import UserProfileResponse
from apps.user.services import (AddChangeUserAvatar, AddPhoneNumber,
                                ApplyResetPassword, ChangePassword,
                                EmailVerification, LoginRequest,
                                RequestResetPassword, ResendPhoneNumberOtp,
                                ResendSmsOtpAuth, ResetPasswordTokenValidate,
                                Session, SmsOtpAuth, StartSmsAuthEnrollment,
                                VerifyPhoneNumber)
from apps.user.validators import EditProfileValidator, UserEmailExistsValidator
from utils import auth
from utils.shortcuts import img2base64, rand_str


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


class UpdateUserProfileAPI(LoggedInAPIView):
    """
    Update user profile API
    """

    def put(self, request):
        data = run_validator(EditProfileValidator, self.request_data)
        user_profile = request.user.userprofile
        update_user_profile(
            user_profile=user_profile,
            first_name=data["first_name"],
            last_name=data["last_name"],
            phone_number=data["phone_number"],
            position=data["position"],
        )
        return self.response(status=204)


class ResendEmailverificationAPI(LoggedInAPIView):
    def post(self, request):
        user = request.user
        if user.email_verified:
            raise ValidationError(
                {"detail": ErrorDetail(_("Email has already verified."))}
            )
        if user.email_verification_token_expire_time < now():
            user.gen_email_verification_token()
        SendVerifyEmail(user=user).send()
        return self.response()


class UsernameOrEmailCheckAPI(APIView):
    def post(self, request):
        """
        check email is duplicate during signup
        """
        data = run_validator(UserEmailExistsValidator, self.request_data)
        email = data["email"].lower()
        user = get_user_by_email(email=email)
        if user:
            raise ValidationError(
                {
                    "email": ErrorDetail(
                        _("This email already exists with another user.")
                    )
                }
            )
        return self.response()


class UserLoginAPI(APIView):
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
        service = LoginRequest(request=request, data=self.request_data)
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


class ResendPhoneNumberVerifyOtpAPI(LoggedInAPIView):
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


class AddPhoneNumberAPI(LoggedInAPIView):
    def post(self, request):
        self._run_services()
        return self.response()

    def _run_services(self):
        service = AddPhoneNumber(request=self.request, data=self.request_data)
        service.handle()


class StartSmsAuthEnrollmentAPI(LoggedInAPIView):
    def post(self, request):
        enrollment_secret = self._run_services()
        return self.response({"secret": enrollment_secret})

    def _run_services(self):
        service = StartSmsAuthEnrollment(request=self.request)
        return service.handle()


class VerifyPhoneNumberAPI(LoggedInAPIView):
    def post(self, request):
        self._run_services(user=request.user)
        return self.response()

    def _run_services(self, user):
        service = VerifyPhoneNumber(
            user=user, request=self.request, data=self.request_data
        )
        service.handle()


class ListSessionsAPI(LoggedInAPIView):
    def get(self, request):
        only_active = request.GET.get("only_active")
        if only_active == "true":
            only_active = True
        else:
            only_active = False

        service = Session(request=request, only_active=only_active)
        return self.response(service.list_sessions())


class DeleteSessionAPI(LoggedInAPIView):
    def delete(self, request):
        session_key = request.GET.get("session_key")
        if not session_key:
            raise ValidationError(
                {"session_key": [ErrorDetail(_("This is required."))]}
            )
        service = Session(request=request)
        service.delete_session(session_key=session_key)
        return self.response()


class GetTwoFactorAuthQRCodeAPI(LoggedInAPIView):
    def get(self, request):
        """
        Get QR code
        """
        user = request.user
        if user.two_factor_auth:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _("Two factor auth is aleady enabled.")
                    )
                }
            )
        token = rand_str()
        user.set_tfa_token(token=token)

        label = f"{user.email}"
        image = qrcode.make(
            OtpAuth(token).to_uri("totp", label, settings.APP_NAME)
        )
        return self.response(img2base64(image))


class TwoFactorAuthAPIBase(LoggedInAPIView):
    def validate(self, request):
        code = self.request_data.get("code", "")
        if not code:
            raise ValidationError(
                {"detail": ErrorDetail(_("Two factor code is required."))}
            )

        user = request.user
        if not OtpAuth(user.tfa_token).valid_totp(code):
            raise ValidationError(
                {"code": [ErrorDetail(_("Invalid two factor code."))]}
            )

        return code


class EnableTwoFactorAuthAPI(TwoFactorAuthAPIBase):
    def post(self, request):
        """
        Enable 2FA
        """
        user = request.user
        if user.two_factor_auth:
            raise ValidationError(
                {"detail": ErrorDetail(_("Two factor auth already enabled."))}
            )

        self.validate(request=request)

        user.enable_tfa()
        return self.response()


class DisableTwoFactorAuthAPI(TwoFactorAuthAPIBase):
    def post(self, request):
        """
        Disable 2FA
        """
        user = request.user
        if not user.two_factor_auth:
            raise ValidationError(
                {"detail": ErrorDetail(_("Two factor auth already disabled."))}
            )

        self.validate(request=request)

        user.disable_tfa()
        return self.response()


class CheckTFAStausAPI(LoggedInAPIView):
    def get(self, request):
        """
        Check TFA status for current user
        """
        user = request.user
        return self.response({"two_factor_auth": user.two_factor_auth})


class UserLogoutAPI(LoggedInAPIView):
    def post(self, request):
        """
        Logout the user i.e end the session.
        """
        auth.logout(request)
        return self.response()


class UserChangePasswordAPI(LoggedInAPIView):
    def post(self, request):
        """
        Changes user's password and asks him to login again.
        """
        self._run_services(request=request)
        return self.response()

    def _run_services(self, request):
        service = ChangePassword(request=request, data=self.request_data)
        service.handle()


class RequestResetPasswordAPI(APIView):
    def post(self, request):
        self._run_services(request=request)
        return self.response()

    def _run_services(self, request):
        service = RequestResetPassword(request=request, data=self.request_data)
        service.handle()


class ResetPasswordTokenValidateAPI(APIView):
    def post(self, request):
        self._run_services(request=request)
        return self.response()

    def _run_services(self, request):
        service = ResetPasswordTokenValidate(
            request=request, data=self.request_data
        )
        service.handle()


class ApplyResetPasswordAPI(APIView):
    def post(self, request):
        self._run_services(request=request)
        return self.response()

    def _run_services(self, request):
        service = ApplyResetPassword(request=request, data=self.request_data)
        service.handle()


class VerifyEmailAPI(APIView):
    def post(self, request):
        self._run_services()
        return self.response()

    def _run_services(self):
        service = EmailVerification(data=self.request_data)
        service.handle()


class UserAvatarAPI(LoggedInAPIView):
    def post(self, request):
        self._run_services()
        return self.response()

    def _run_services(self):
        AddChangeUserAvatar(
            user=self.request.user, data=self.request_data
        ).handle()
