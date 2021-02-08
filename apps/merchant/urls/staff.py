from django.urls import path

from apps.merchant.views.staff import (DeleteNonLoqalAPI,
                                       GetCodesAndProtocolsAPI,
                                       GetMerchantOperationHoursAPI,
                                       GetMerchantProfileAPI,
                                       GetServiceAvailabilityAPI,
                                       UpdateCodesAndProtocolsAPI,
                                       UpdateMerchantOperationHoursAPI,
                                       UpdateMerchantProfileAPI,
                                       UpdateServiceAvailabilityAPI)

urlpatterns = [
    path(
        "<uuid:merchant_id>/profile/update/",
        UpdateMerchantProfileAPI.as_view(),
        name="staff_update_merchant_profile",
    ),
    path(
        "<uuid:merchant_id>/profile/",
        GetMerchantProfileAPI.as_view(),
        name="staff_view_merchant_profile",
    ),
    path(
        "<uuid:merchant_id>/operation-hours/update/",
        UpdateMerchantOperationHoursAPI.as_view(),
        name="staff_update_operational_hours",
    ),
    path(
        "<uuid:merchant_id>/operation-hours/",
        GetMerchantOperationHoursAPI.as_view(),
        name="staff_view_operational_hours",
    ),
    path(
        "<uuid:merchant_id>/codes-protocols/update/",
        UpdateCodesAndProtocolsAPI.as_view(),
        name="staff_update_codes_protocols",
    ),
    path(
        "<uuid:merchant_id>/codes-protocols/",
        GetCodesAndProtocolsAPI.as_view(),
        name="staff_view_codes_protocols",
    ),
    path(
        "<uuid:merchant_id>/service-availibility/update/",
        UpdateServiceAvailabilityAPI.as_view(),
        name="update_service_availibilitys",
    ),
    path(
        "<uuid:merchant_id>/service-availibility/",
        GetServiceAvailabilityAPI.as_view(),
        name="view_service_availibility",
    ),
    path(
        "non-loqal/<uuid:merchant_id>/",
        DeleteNonLoqalAPI.as_view(),
        name="delete_non_loqal",
    ),
]
