from django.urls import path

from apps.user.views.staff import UserLoginAPI

urlpatterns = [
    path("staff/login/", UserLoginAPI.as_view(), name="staff_user_login"),
]
