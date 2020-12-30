from django.urls import path

from apps.user.views.merchant import GetUserProfileAPI, UpdateUserProfileAPI

urlpatterns = [
    path(
        "merchant/profile/",
        GetUserProfileAPI.as_view(),
        name="merchant_user_profile",
    ),
    path(
        "merchant/profile/update/",
        UpdateUserProfileAPI.as_view(),
        name="merchant_user_profile_update",
    ),
]
