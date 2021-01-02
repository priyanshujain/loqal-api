from django.urls import path

from apps.merchant.views.profile import (GetMerchantProfileAPI,
                                         UpdateMerchantProfileAPI)

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
]
