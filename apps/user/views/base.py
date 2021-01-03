import qrcode
from django.conf import settings
from django.utils.translation import gettext as _
from otpauth import OtpAuth

from django.contrib.auth.models import AnonymousUser


from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.views import APIView, LoggedInAPIView
from apps.user.dbapi import get_user_by_email
from apps.user.services import (AddChangeUserAvatar, ChangePassword,
                                ResetPasswordTokenValidate, Session)
from apps.user.validators import UserEmailExistsValidator
from utils import auth
from utils.shortcuts import img2base64, rand_str


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
        request.user = AnonymousUser()
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


class ResetPasswordTokenValidateAPI(APIView):
    def post(self, request):
        self._run_services(request=request)
        return self.response()

    def _run_services(self, request):
        service = ResetPasswordTokenValidate(
            request=request, data=self.request_data
        )
        service.handle()


class UserAvatarAPI(LoggedInAPIView):
    def post(self, request):
        self._run_services()
        return self.response()

    def _run_services(self):
        AddChangeUserAvatar(
            user=self.request.user, data=self.request_data
        ).handle()
