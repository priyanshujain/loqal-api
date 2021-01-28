from django.urls import path

from apps.account.views.staff import (CreateNonLoqalMerchantsAPI,
                                      DisableAccountAPI, EnableAccountAPI,
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
        "staff/account/disable/",
        DisableAccountAPI.as_view(),
        name="disable_account",
    ),
    path(
        "staff/account/enable/",
        EnableAccountAPI.as_view(),
        name="enable_account",
    ),
    path(
        "staff/merchants/",
        GetActiveMerchantsAPI.as_view(),
        name="view_active_merchants",
    ),
]
