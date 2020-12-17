from django.urls import path

from apps.merchant.views.consumer import MerchantBasicDetailsAPI

urlpatterns = [
    path(
        "basic-info/",
        MerchantBasicDetailsAPI.as_view(),
        name="business_basic_details",
    ),
]
