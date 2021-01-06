from django.urls import path

from apps.user.views.consumer import (AddPhoneNumberAPI, ApplyResetPasswordAPI,
                                      GetUserProfileAPI,
                                      RequestResetPasswordAPI,
                                      ResendEmailverificationAPI,
                                      ResendPhoneNumberVerifyOtpAPI,
                                      ResendSmsOtpAuthAPI, SmsOtpAuthAPI,
                                      StartSmsAuthEnrollmentAPI, UserLoginAPI,
                                      VerifyEmailAPI, VerifyPhoneNumberAPI)

urlpatterns = [
    path(
        "consumer/login/", UserLoginAPI.as_view(), name="consumer_user_login"
    ),
    path("consumer/auth/otp/", SmsOtpAuthAPI.as_view(), name="otp_auth"),
    path(
        "consumer/auth/otp/resend/",
        ResendSmsOtpAuthAPI.as_view(),
        name="otp_auth_resend",
    ),
    path(
        "consumer/auth/otp/enrollment/",
        StartSmsAuthEnrollmentAPI.as_view(),
        name="start_otp_enrollment",
    ),
    path(
        "consumer/phone/add/",
        AddPhoneNumberAPI.as_view(),
        name="add_phone_number",
    ),
    path(
        "consumer/phone/verify/",
        VerifyPhoneNumberAPI.as_view(),
        name="verify_phone_number",
    ),
    path(
        "consumer/phone/verify/resend/",
        ResendPhoneNumberVerifyOtpAPI.as_view(),
        name="verify_phone_number_resend",
    ),
    path(
        "consumer/reset-password/request/",
        RequestResetPasswordAPI.as_view(),
        name="request_reset_password",
    ),
    path(
        "consumer/reset-password/apply/",
        ApplyResetPasswordAPI.as_view(),
        name="apply_reset_password",
    ),
    path(
        "consumer/profile/",
        GetUserProfileAPI.as_view(),
        name="view_user_profile",
    ),
    path(
        "consumer/email-verification/apply/",
        VerifyEmailAPI.as_view(),
        name="verify_email",
    ),
    path(
        "consumer/email-verification/resend/",
        ResendEmailverificationAPI.as_view(),
        name="resend_email_verification",
    ),
]
