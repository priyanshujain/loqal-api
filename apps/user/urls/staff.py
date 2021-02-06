from django.urls import path

from apps.user.views.staff import (AdminUserAddAPI, ChangeAdminRoleAPI,
                                   GetAdminUserAPI, UserLoginAPI)

urlpatterns = [
    path("staff/login/", UserLoginAPI.as_view(), name="staff_user_login"),
    path("staff/create/", AdminUserAddAPI.as_view(), name="admin_user_add"),
    path(
        "staff/change-role/",
        ChangeAdminRoleAPI.as_view(),
        name="admin_role_change",
    ),
    path("staff/members/", GetAdminUserAPI.as_view(), name="get_admin_users"),
]
