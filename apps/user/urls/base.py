from django.urls import path

from apps.user.views import (CheckTFAStausAPI, DeleteSessionAPI,
                             DisableTwoFactorAuthAPI, EnableTwoFactorAuthAPI,
                             GetTwoFactorAuthQRCodeAPI, ListSessionsAPI,
                             ResetPasswordTokenValidateAPI, UserAvatarAPI,
                             UserLogoutAPI)

urlpatterns = [
    path("avatar/", UserAvatarAPI.as_view(), name="user_avatar"),
    path("logout/", UserLogoutAPI.as_view(), name="user_logout"),
    path(
        "reset-password/validate-token/",
        ResetPasswordTokenValidateAPI.as_view(),
        name="validate_reset_password_token",
    ),
    path(
        "tfa/status/",
        CheckTFAStausAPI.as_view(),
        name="tfa_status",
    ),
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
    path(
        "sessions/",
        ListSessionsAPI.as_view(),
        name="list_sessions",
    ),
    path(
        "sessions/delete/",
        DeleteSessionAPI.as_view(),
        name="delete_session",
    ),
]
