from django.urls import path

from apps.merchant.views.reference import BusinessClassificationsAPI

urlpatterns = [
    path(
        "reference/business-classifications/",
        BusinessClassificationsAPI.as_view(),
        name="business_classfications",
    ),
]
