from django.urls import path

from apps.merchant.views.consumer import (ListCategoryMerchantsAPI,
                                          MerchantBasicDetailsAPI,
                                          MerchantSearchAPI, StoreDetailsAPI)

urlpatterns = [
    path(
        "details/<uuid:merchant_id>/basic-info/",
        MerchantBasicDetailsAPI.as_view(),
        name="store_basic_details",
    ),
    path(
        "details/<uuid:merchant_id>/",
        StoreDetailsAPI.as_view(),
        name="store_details",
    ),
    path(
        "stores/search",
        MerchantSearchAPI.as_view(),
        name="merchant_category_stores_search",
    ),
    path(
        "stores/",
        ListCategoryMerchantsAPI.as_view(),
        name="merchant_category_stores",
    ),
]
