from django.urls import path

from apps.core.views import (AppMetaDataAPI, GetAppMetaDataAPI,
                             GetMerchantMetaDataAPI, MerchantMetaDataAPI)

urlpatterns = [
    path(
        "staff/app-metadata/",
        AppMetaDataAPI.as_view(),
        name="app_metadata",
    ),
    path(
        "app-metadata/",
        GetAppMetaDataAPI.as_view(),
        name="app_metadata_public",
    ),
    path(
        "staff/merchant-metadata/",
        MerchantMetaDataAPI.as_view(),
        name="merchant_metadata",
    ),
    path(
        "merchant-metadata/",
        GetMerchantMetaDataAPI.as_view(),
        name="merchant_metadata_public",
    ),
]
