from django.urls import path

from apps.merchant.views.profile import (GetCodesAndProtocolsAPI,
                                         GetMerchantOperationHoursAPI,
                                         GetMerchantProfileAPI,
                                         GetServiceAvailabilityAPI,
                                         UpdateCodesAndProtocolsAPI,
                                         UpdateMerchantOperationHoursAPI,
                                         UpdateMerchantProfileAPI,
                                         UpdateServiceAvailabilityAPI)

urlpatterns = [
    path(
        "profile/update/",
        UpdateMerchantProfileAPI.as_view(),
        name="update_merchant_profile",
    ),
    path(
        "profile/",
        GetMerchantProfileAPI.as_view(),
        name="view_merchant_profile",
    ),
    path(
        "operation-hours/update/",
        UpdateMerchantOperationHoursAPI.as_view(),
        name="update_operational_hours",
    ),
    path(
        "operation-hours/",
        GetMerchantOperationHoursAPI.as_view(),
        name="view_operational_hours",
    ),
    path(
        "codes-protocols/update/",
        UpdateCodesAndProtocolsAPI.as_view(),
        name="update_codes_protocols",
    ),
    path(
        "codes-protocols/",
        GetCodesAndProtocolsAPI.as_view(),
        name="view_codes_protocols",
    ),
    path(
        "service-availibility/update/",
        UpdateServiceAvailabilityAPI.as_view(),
        name="update_service_availibilitys",
    ),
    path(
        "service-availibility/",
        GetServiceAvailabilityAPI.as_view(),
        name="view_service_availibility",
    ),
]
