from django.urls import path

from apps.merchant.views.consumer import (MerchantBasicDetailsAPI,
                                          MerchantDetailsAPI,
                                          MerchantSearchAPI)
from apps.merchant.views.stores import ListCategoryMerchantsAPI

urlpatterns = [
    path(
        "basic-info/",
        MerchantBasicDetailsAPI.as_view(),
        name="business_basic_details",
    ),
    path(
        "details/<uuid:merchant_id>",
        MerchantDetailsAPI.as_view(),
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
