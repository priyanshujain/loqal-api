from django.urls import path

from apps.account.views.merchant import MerchantProfileAPI, MerchantSignupAPI

urlpatterns = [
    path(
        "merchant/signup/",
        MerchantSignupAPI.as_view(),
        name="merchant_signup",
    ),
    path(
        "merchant/profile/",
        MerchantProfileAPI.as_view(),
        name="merchant_profile",
    ),
]
