from django.urls import path

from apps.merchant.views.consumer import MerchantBasicDetailsAPI
from apps.merchant.views.stores import ListCategoryMerchantsAPI

urlpatterns = [
    path(
        "basic-info/",
        MerchantBasicDetailsAPI.as_view(),
        name="business_basic_details",
    ),
    path(
        "stores/",
        ListCategoryMerchantsAPI.as_view(),
        name="merchant_category_stores",
    ),
]
