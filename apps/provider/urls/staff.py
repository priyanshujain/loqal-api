from django.urls import path

from apps.provider.views.staff import (AccountProviderCredentialsAPI,
                                       ActivateTermsDocumentAPI,
                                       CreatePaymentProviderAPI,
                                       CreatePaymentProviderCredsAPI,
                                       CreateTermDocumentAPI,
                                       ListClientAccountProviderAPI,
                                       ListTermsAPI, PaymentAccountStatusAPI,
                                       ProviderLogoUploadAPI,
                                       RemoveTermDocumentAPI,
                                       UpdatePaymentProviderAPI,
                                       UpdatePaymentProviderCredsAPI)

urlpatterns = [
    path("create/", CreatePaymentProviderAPI.as_view(),),
    path("update/", UpdatePaymentProviderAPI.as_view(),),
    path("logo/update/", ProviderLogoUploadAPI.as_view(),),
    path("creds/create/", CreatePaymentProviderCredsAPI.as_view(),),
    path("creds/update/", UpdatePaymentProviderCredsAPI.as_view(),),
    path("terms/create/", CreateTermDocumentAPI.as_view(),),
    path("terms/deactivate/", RemoveTermDocumentAPI.as_view(),),
    path("terms/reactivate/", ActivateTermsDocumentAPI.as_view(),),
    path("terms/", ListTermsAPI.as_view(),),
    path("client/credential/add/", AccountProviderCredentialsAPI.as_view(),),
    path(
        "client/providers/connected/", ListClientAccountProviderAPI.as_view(),
    ),
    path(
        "client/<int:account_id>/payment-account/",
        PaymentAccountStatusAPI.as_view(),
    ),
]
