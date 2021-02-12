from django.urls import path

from apps.banking.views.merchant import (CreateBankAccountAPI,
                                         CreateIAVBankAccountAPI,
                                         GetBankAccountAPI, GetIAVTokenAPI,
                                         PlaidLinkTokenAPI,
                                         ReAuthBankAccountAPI,
                                         RemoveBankAccountAPI,
                                         VerifyMicroDepositAPI)

urlpatterns = [
    path(
        "merchant/accounts/create/",
        CreateBankAccountAPI.as_view(),
        name="create_merchant_bank_account",
    ),
    path(
        "merchant/accounts/verify-micro-deposit/",
        VerifyMicroDepositAPI.as_view(),
        name="verify_merchant_micro_deposit",
    ),
    path(
        "merchant/accounts/iav/create/",
        CreateIAVBankAccountAPI.as_view(),
        name="create_iav_,merchant_bank_account",
    ),
    path(
        "merchant/accounts/remove/",
        RemoveBankAccountAPI.as_view(),
        name="remove_merchant_bank_account",
    ),
    path(
        "merchant/accounts/reauth/",
        ReAuthBankAccountAPI.as_view(),
        name="reauth_merchant_bank_account",
    ),
    path(
        "merchant/plaid-token/",
        PlaidLinkTokenAPI.as_view(),
        name="create_merchant_plaid_token",
    ),
    path(
        "merchant/accounts/dwolla-iav-token/",
        GetIAVTokenAPI.as_view(),
        name="create_merchant_dwolla_iav_token",
    ),
    path(
        "merchant/accounts/",
        GetBankAccountAPI.as_view(),
        name="view_merchant_bank_account",
    ),
]
