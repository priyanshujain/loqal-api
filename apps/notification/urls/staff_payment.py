from django.urls import path

from apps.notification.views.staff_payment import (
    AddStaffNoticationSettingAPI, DeleteStaffNoticationSettingAPI,
    DisableStaffNoticationSettingAPI, EnableStaffNoticationSettingAPI,
    GetStaffNoticationSettingAPI)

urlpatterns = [
    path(
        "merchant/payment/create/",
        AddStaffNoticationSettingAPI.as_view(),
        name="add_staff_payment_notification_setting",
    ),
    path(
        "merchant/payment/<uuid:setting_id>/disable/",
        DisableStaffNoticationSettingAPI.as_view(),
        name="disable_staff_payment_notification_setting",
    ),
    path(
        "merchant/payment/<uuid:setting_id>/enable/",
        EnableStaffNoticationSettingAPI.as_view(),
        name="enable_staff_payment_notification_setting",
    ),
    path(
        "merchant/payment/<uuid:setting_id>/delete/",
        DeleteStaffNoticationSettingAPI.as_view(),
        name="delete_staff_payment_notification_setting",
    ),
    path(
        "merchant/payment/settings/",
        GetStaffNoticationSettingAPI.as_view(),
        name="all_staff_payment_notification_setting",
    ),
]
