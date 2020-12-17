from django.urls import path

from apps.merchant.views.reference import BusinessClassificationsAPI, MerchantCategoriesAPI

urlpatterns = [
    path(
        "reference/business-classifications/",
        BusinessClassificationsAPI.as_view(),
        name="business_classfications",
    ),
    path(
        "reference/categories/",
        MerchantCategoriesAPI.as_view(),
        name="business_categories",
    ),
]
