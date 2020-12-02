from django.urls import path

from apps.account.views.consumer import (AddAccountZipCodeAPI,
                                         ConsumerAccountProfileAPI,
                                         ConsumerSignupAPI)

urlpatterns = [
    path(
        "zip-code/add/",
        AddAccountZipCodeAPI.as_view(),
        name="add_consumer_zip_code",
    ),
    path(
        "consumer/signup/",
        ConsumerSignupAPI.as_view(),
        name="consumer_signup_api",
    ),
    path(
        "consumer/profile/",
        ConsumerAccountProfileAPI.as_view(),
        name="consumer_account_profile",
    ),
]
