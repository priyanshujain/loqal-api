from django.urls import path

from apps.merchant.views.member_user import (GetUserProfileAPI,
                                             UpdateUserProfileAPI)

urlpatterns = [
    path(
        "member/profile/update/",
        UpdateUserProfileAPI.as_view(),
        name="merchant_user_profile_update",
    ),
    path(
        "member/profile/",
        GetUserProfileAPI.as_view(),
        name="merchant_user_profile",
    ),
]
