from django.urls import path

from apps.banking.views.merchant import (
    CreateBankAccountAPI,
    GetBankAccountAPI,
    PlaidLinkTokenAPI,
)


urlpatterns = [
    path(
        "merchant/accounts/create/",
        CreateBankAccountAPI.as_view(),
        name="create_merchant_bank_account",
    ),
    path(
        "merchant/plaid-token/",
        PlaidLinkTokenAPI.as_view(),
        name="create_merchant_plaid_token",
    ),
    path(
        "merchant/accounts/",
        GetBankAccountAPI.as_view(),
        name="view_merchant_bank_account",
    ),
]
