from django.conf.urls import url

from apps.account.views.user import UserSignupAPI

urlpatterns = [
    url(r"^signup/?$", UserSignupAPI.as_view(), name="account_signup_api"),
]
