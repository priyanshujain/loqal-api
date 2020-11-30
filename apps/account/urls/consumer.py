from django.urls import path

from apps.account.views.consumer import ConsumerSignupAPI

urlpatterns = [
    path(
        "consumer/signup/",
        ConsumerSignupAPI.as_view(),
        name="consumer_signup_api",
    ),
]
