from django.urls import path

from apps.user.views.staff import (AdminUserAddAPI, ChangeAdminRoleAPI,
                                   GetAdminUserAPI, GetUserProfileAPI,
                                   UserChangePasswordAPI, UserLoginAPI)

urlpatterns = [
    path("staff/login/", UserLoginAPI.as_view(), name="staff_user_login"),
    path(
        "staff/profile/",
        GetUserProfileAPI.as_view(),
        name="view_staff_profile",
    ),
    path("staff/create/", AdminUserAddAPI.as_view(), name="admin_user_add"),
    path(
        "staff/change-password/",
        UserChangePasswordAPI.as_view(),
        name="staff_change_password",
    ),
    path(
        "staff/change-role/",
        ChangeAdminRoleAPI.as_view(),
        name="admin_role_change",
    ),
    path("staff/members/", GetAdminUserAPI.as_view(), name="get_admin_users"),
]
