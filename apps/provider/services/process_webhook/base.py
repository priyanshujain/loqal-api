import hmac
from hashlib import sha256

from django.utils.translation import gettext as _

from api.services import ServiceBase
from apps.provider.dbapi import (create_provider_webhook_event,
                                 get_provider_webhook)

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
        )
        if not is_verified:
            return

        event_id = self.request_data.get("id", "")
        target_resource_dwolla_id = self.request_data.get("resourceId", "")
        topic = self.request_data.get("topic", "")
        self._factory_provider_webhook_event(
            webhook_id=provider_webhook.id,
            dwolla_id=event_id,
            target_resource_dwolla_id=target_resource_dwolla_id,
            topic=topic,
        )

    def _verify_gateway_signature(self, proposed_signature, webhook_secret):
        signature = hmac.new(
            webhook_secret.encode("utf-8"), self.request_body, sha256
        ).hexdigest()
        return hmac.compare_digest(signature, proposed_signature)

    def _factory_provider_webhook_event(
        self, webhook_id, dwolla_id, topic, target_resource_dwolla_id
    ):
        create_provider_webhook_event(
            webhook_id=webhook_id,
            event_payload=self.request_data,
            dwolla_id=dwolla_id,
            topic=topic,
            target_resource_dwolla_id=target_resource_dwolla_id,
        )
