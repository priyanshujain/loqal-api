from django.urls import path

from apps.account.views.merchant import MerchantSignupAPI, MerchantProfileAPI

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
