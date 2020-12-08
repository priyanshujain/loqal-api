from django.urls import path

from apps.banking.views.consumer import (CreateBankAccountAPI, PlaidLinkTokenAPI, GetBankAccountAPI,)

urlpatterns = [
    path(
        "accounts/create/",
        CreateBankAccountAPI.as_view(),
    ),
    path(
        "accounts/",
        GetBankAccountAPI.as_view(),
    ),
    path(
        "plaid-token/",
        PlaidLinkTokenAPI.as_view(),
    ),
]
