from django.urls import path

from apps.user.views.merchant import (ApplyResetPasswordAPI,
                                      RequestResetPasswordAPI,
                                      ResendEmailverificationAPI, UserLoginAPI,
                                      VerifyEmailAPI)

urlpatterns = [
    path("merchant/login/", UserLoginAPI.as_view(), name="user_login"),
    path(
        "merchant/reset-password/request/",
        RequestResetPasswordAPI.as_view(),
        name="request_reset_password",
    ),
    path(
        "merchant/reset-password/apply/",
        ApplyResetPasswordAPI.as_view(),
        name="apply_reset_password",
    ),
    path(
        "merchant/email-verification/apply/",
        VerifyEmailAPI.as_view(),
        name="verify_email",
    ),
    path(
        "merchant/email-verification/resend/",
        ResendEmailverificationAPI.as_view(),
        name="resend_email_verification",
    ),
]
