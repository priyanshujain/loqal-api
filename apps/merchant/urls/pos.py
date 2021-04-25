from django.urls import path

from apps.merchant.views.pos import (CreatePosStaffAPI,
                                     GeneratePosStaffLoginQrCodeAPI,
                                     GeneratePosStaffPinAPI, GetPosStaffAPI,
                                     UpdatePosStaffAPI)
from apps.merchant.views.pos_member import (GetPosStaffProfileAPI,
                                            PosStaffLoginAPI,
                                            PosStaffLogoutAPI,
                                            PosStaffValidateAccessTokenAPI,
                                            UpdatePosStaffProfileAPI)

urlpatterns = [
    path(
        "pos/member-staff/create/",
        CreatePosStaffAPI.as_view(),
        name="create_pos_staff",
    ),
    path(
        "pos/member-staff/<uuid:pos_staff_id>/update/",
        UpdatePosStaffAPI.as_view(),
        name="update_pos_staff_pin",
    ),
    path(
        "pos/member-staff/<uuid:pos_staff_id>/pin/renew/",
        GeneratePosStaffPinAPI.as_view(),
        name="renew_pos_staff_pin",
    ),
    path(
        "pos/member-staff/<uuid:pos_staff_id>/login-qrcode/",
        GeneratePosStaffLoginQrCodeAPI.as_view(),
        name="pos_staff_login_qrcode",
    ),
    path(
        "pos/member-staff/validate-access-token/",
        PosStaffValidateAccessTokenAPI.as_view(),
        name="validate_access_token_pos_staff",
    ),
    path(
        "pos/member-staff/login/",
        PosStaffLoginAPI.as_view(),
        name="login_pos_staff",
    ),
    path(
        "pos/member-staff/logout/",
        PosStaffLogoutAPI.as_view(),
        name="logout_pos_staff",
    ),
    path(
        "pos/member-staff/profile/",
        GetPosStaffProfileAPI.as_view(),
        name="pos_staff_profile",
    ),
    path(
        "pos/member-staff/profile/update/",
        UpdatePosStaffProfileAPI.as_view(),
        name="pos_staff_profile_update",
    ),
    path(
        "pos/member-staff/",
        GetPosStaffAPI.as_view(),
        name="list_pos_staff",
    ),
]
