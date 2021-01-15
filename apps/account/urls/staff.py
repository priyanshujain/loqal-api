from django.urls import path

from apps.account.views.staff import (CreateNonLoqalMerchantsAPI,
                                      GetActiveMerchantsAPI,
                                      GetNonLoqalMerchantsAPI)

urlpatterns = [
    path(
        "staff/merchants/non-loqal/create/",
        CreateNonLoqalMerchantsAPI.as_view(),
        name="create_non_loqal_active_merchants",
    ),
    path(
        "staff/merchants/non-loqal/",
        GetNonLoqalMerchantsAPI.as_view(),
        name="view_non_loqal_active_merchants",
    ),
    path(
        "staff/merchants/",
        GetActiveMerchantsAPI.as_view(),
        name="view_active_merchants",
    ),
]
