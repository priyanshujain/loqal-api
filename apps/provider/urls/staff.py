from django.urls import path

from apps.provider.views.staff import (ActivateTermsDocumentAPI,
                                       CreatePaymentProviderAPI,
                                       CreatePaymentProviderCredsAPI,
                                       CreateProviderWebhookAPI,
                                       CreateTermDocumentAPI, ListTermsAPI,
                                       ProviderLogoUploadAPI,
                                       RemoveTermDocumentAPI,
                                       UpdatePaymentProviderAPI,
                                       UpdatePaymentProviderCredsAPI)

urlpatterns = [
    path(
        "create/",
        CreatePaymentProviderAPI.as_view(),
    ),
    path(
        "update/",
        UpdatePaymentProviderAPI.as_view(),
    ),
    path(
        "logo/update/",
        ProviderLogoUploadAPI.as_view(),
    ),
    path(
        "creds/create/",
        CreatePaymentProviderCredsAPI.as_view(),
    ),
    path(
        "creds/update/",
        UpdatePaymentProviderCredsAPI.as_view(),
    ),
    path(
        "terms/create/",
        CreateTermDocumentAPI.as_view(),
    ),
    path(
        "terms/deactivate/",
        RemoveTermDocumentAPI.as_view(),
    ),
    path(
        "terms/reactivate/",
        ActivateTermsDocumentAPI.as_view(),
    ),
    path(
        "terms/",
        ListTermsAPI.as_view(),
    ),
    path(
        "create-webhook/",
        CreateProviderWebhookAPI.as_view(),
    ),
]
