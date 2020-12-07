from django.http.multipartparser import parse_header
from django.urls import path

from apps.user.views import (AddPhoneNumberAPI, ApplyResetPasswordAPI,
                             CheckTFAStausAPI, DeleteSessionAPI,
                             DisableTwoFactorAuthAPI, EnableTwoFactorAuthAPI,
                             GetTwoFactorAuthQRCodeAPI, GetUserProfileAPI,
                             ListSessionsAPI, RequestResetPasswordAPI,
                             ResendEmailverificationAPI,
                             ResetPasswordTokenValidateAPI,
                             UpdateUserProfileAPI, UserChangePasswordAPI,
                             UserLoginAPI, UserLogoutAPI,
                             UsernameOrEmailCheckAPI, VerifyEmailAPI,
                             VerifyPhoneNumberAPI,
                             SmsOtpAuthAPI,
                             UserAvatarAPI,)

urlpatterns = [
    path("login/", UserLoginAPI.as_view(), name="user_login"),
    path("auth/otp/", SmsOtpAuthAPI.as_view(), name="otp_auth"),
    path("avatar/", UserAvatarAPI.as_view(), name="user_avatar"),
    path("phone/add/", AddPhoneNumberAPI.as_view(), name="add_phone_number"),
    path(
        "phone/verify/",
        VerifyPhoneNumberAPI.as_view(),
        name="verify_phone_number",
    ),
    path("logout/", UserLogoutAPI.as_view(), name="user_logout"),
    path(
        "change-password/",
        UserChangePasswordAPI.as_view(),
        name="user_change_password",
    ),
    path(
        "reset-password/request/",
        RequestResetPasswordAPI.as_view(),
        name="request_reset_password",
    ),
    path(
        "reset-password/validate-token/",
        ResetPasswordTokenValidateAPI.as_view(),
        name="validate_reset_password_token",
    ),
    path(
        "reset-password/apply/",
        ApplyResetPasswordAPI.as_view(),
        name="apply_reset_password",
    ),
    path(
        "email/check/",
        UsernameOrEmailCheckAPI.as_view(),
        name="check_email_exists",
    ),
    path("profile/", GetUserProfileAPI.as_view(), name="view_user_profile"),
    path(
        "profile/update/",
        UpdateUserProfileAPI.as_view(),
        name="update_user_profile",
    ),
    path("tfa/status/", CheckTFAStausAPI.as_view(), name="tfa_status",),
    path(
        "tfa/qrcode/",
        GetTwoFactorAuthQRCodeAPI.as_view(),
        name="two_factor_auth_qr_code",
    ),
    path(
        "tfa/enable/",
        EnableTwoFactorAuthAPI.as_view(),
        name="enable_two_factor_auth",
    ),
    path(
        "tfa/disable/",
        DisableTwoFactorAuthAPI.as_view(),
        name="disable_two_factor_auth",
    ),
    path("sessions/", ListSessionsAPI.as_view(), name="list_sessions",),
    path(
        "sessions/delete/", DeleteSessionAPI.as_view(), name="delete_session",
    ),
    path(
        "email-verification/apply/",
        VerifyEmailAPI.as_view(),
        name="verify_email",
    ),
    path(
        "email-verification/resend/",
        ResendEmailverificationAPI.as_view(),
        name="resend_email_verification",
    ),
]
