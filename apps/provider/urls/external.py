from django.urls import path

from apps.provider.views.external import ProviderWebhookAPI

urlpatterns = [
    path(
        "webhook/<str:webhook_id>/",
        ProviderWebhookAPI.as_view(),
        name="provider_webhook",
    ),
]
