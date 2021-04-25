from django.urls import path

from apps.merchant.views.pos import (CreatePosStaffAPI,
                                     GeneratePosStaffLoginQrCodeAPI,
                                     GeneratePosStaffPinAPI, GetPosStaffAPI,
                                     UpdatePosStaffAPI)

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
        "pos/member-staff/",
        GetPosStaffAPI.as_view(),
        name="list_pos_staff",
    ),
]
