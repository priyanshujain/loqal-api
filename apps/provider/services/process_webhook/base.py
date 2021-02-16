import hmac
from hashlib import sha256

from dateutil import parser
from django.utils import timezone
from django.utils.translation import gettext as _

from api.services import ServiceBase
from apps.provider.dbapi import (create_provider_webhook_event,
                                 get_provider_webhook)

from .tasks import process_webhook_event

__all__ = ("ProcesssProviderWebhook",)


class ProcesssProviderWebhook(ServiceBase):
    def __init__(self, headers, request_data, request_body, webhook_id):
        self.headers = headers
        self.request_body = request_body
        self.request_data = request_data
        self.webhook_id = webhook_id

    def handle(self):
        provider_webhook = get_provider_webhook(webhook_id=self.webhook_id)
        if not provider_webhook or not provider_webhook.is_active:
            return None

        signature = self.headers.get("X-Request-Signature-SHA-256", None)
        if not signature:
            return

        is_verified = self._verify_gateway_signature(
            proposed_signature=signature,
            webhook_secret=provider_webhook.webhook_secret,
            payload_body=str(self.request_body, "utf-8"),
        )

        if not is_verified:
            return

        event_id = self.request_data.get("id", "")
        target_resource_dwolla_id = self.request_data.get("resourceId", "")
        topic = self.request_data.get("topic", "")
        timestamp = self.request_data.get("timestamp", "")
        event_timestamp = timezone.now()
        if timestamp:
            event_timestamp = parser.parse(timestamp)

        customer_dwolla_id = None
        if "customer" in topic:
            customer_dwolla_id = (
                self.request_data.get("_links", {})
                .get("customer", {})
                .get("href", "")
                .split("/")
                .pop()
            )

        event = self._factory_provider_webhook_event(
            webhook_id=provider_webhook.id,
            dwolla_id=event_id,
            target_resource_dwolla_id=target_resource_dwolla_id,
            topic=topic,
            customer_dwolla_id=customer_dwolla_id,
            event_timestamp=event_timestamp,
        )

        process_webhook_event.delay(event_id=event.id)

    def _verify_gateway_signature(
        self, proposed_signature, webhook_secret, payload_body
    ):
        signature = hmac.new(
            webhook_secret.encode("utf-8"),
            payload_body.encode("utf-8"),
            sha256,
        ).hexdigest()
        return hmac.compare_digest(signature, proposed_signature)

    def _factory_provider_webhook_event(
        self,
        webhook_id,
        dwolla_id,
        topic,
        customer_dwolla_id,
        target_resource_dwolla_id,
        event_timestamp,
    ):
        return create_provider_webhook_event(
            webhook_id=webhook_id,
            event_payload=self.request_data,
            dwolla_id=dwolla_id,
            topic=topic,
            customer_dwolla_id=customer_dwolla_id,
            target_resource_dwolla_id=target_resource_dwolla_id,
            event_timestamp=event_timestamp,
        )
