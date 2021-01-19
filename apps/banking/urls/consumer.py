from django.urls import path

from apps.banking.views.consumer import (CreateBankAccountAPI,
                                         GetBankAccountAPI, PlaidLinkTokenAPI,
                                         ReAuthBankAccountAPI)

urlpatterns = [
    path(
        "consumer/accounts/create/",
        CreateBankAccountAPI.as_view(),
        name="create_consumer_bank_account",
    ),
    path(
        "consumer/accounts/reauth/",
        ReAuthBankAccountAPI.as_view(),
        name="reauth_consumer_bank_account",
    ),
    path(
        "consumer/accounts/plaid-token/",
        PlaidLinkTokenAPI.as_view(),
        name="create_consumer_plaid_token",
    ),
    path(
        "consumer/accounts/",
        GetBankAccountAPI.as_view(),
        name="view_consumer_bank_account",
    ),
]
