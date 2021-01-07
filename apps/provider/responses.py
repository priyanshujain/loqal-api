from api import serializers
from apps.provider.models import (PaymentProvider, ProviderWebhook,
                                  ProviderWebhookEvent, TermsDocument)


class TermsDocumentResponse(serializers.ModelSerializer):
    class Meta:
        model = TermsDocument
        fields = "__all__"


class PaymentProviderResponse(serializers.ModelSerializer):
    class Meta:
        model = PaymentProvider
        fields = "__all__"


class ListWebhooksResponse(serializers.ModelSerializer):
    provider = serializers.CharField(
        source="provider.display_name", read_only=True
    )

    class Meta:
        model = ProviderWebhook
        fields = (
            "webhook_id",
            "dwolla_id",
            "is_active",
            "provider",
            "id",
        )


class ListWebhooksResponse(serializers.ModelSerializer):
    provider = serializers.CharField(
        source="provider.display_name", read_only=True
    )

    class Meta:
        model = ProviderWebhook
        fields = (
            "webhook_id",
            "dwolla_id",
            "is_active",
            "provider",
            "id",
        )


class ListWebhookEventsResponse(serializers.ModelSerializer):
    class Meta:
        model = ProviderWebhookEvent
        fields = (
            "event_payload",
            "dwolla_id",
            "is_processed",
            "topic",
            "target_resource_dwolla_id",
            "id",
        )
