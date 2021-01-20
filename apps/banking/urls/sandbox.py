from django.urls import path

from apps.banking.views.sandbox import (ConsumerReAuthBankAccountAPI,
                                        MerchantReAuthBankAccountAPI)

urlpatterns = [
    path(
        "sandbox/customer/plaid/reset-auth/",
        ConsumerReAuthBankAccountAPI.as_view(),
    ),
    path(
        "sandbox/merchant/plaid/reset-auth/",
        MerchantReAuthBankAccountAPI.as_view(),
    ),
]
