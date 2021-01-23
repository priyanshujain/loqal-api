import hmac
from hashlib import sha256

from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.services import ServiceBase
from apps.account.dbapi.webhooks import get_account_by_dwolla_id
from apps.provider.dbapi import (create_provider_webhook_event,
                                 get_provider_webhook)

from .banking import ApplyBankingWebhook
from .beneficial_owners import ApplyBeneficialOwnerWebhook
from .onboarding import ApplyOnboardingWebhook
from .payments import ApplyPaymentWebhook

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
        event = self._factory_provider_webhook_event(
            webhook_id=provider_webhook.id,
            dwolla_id=event_id,
            target_resource_dwolla_id=target_resource_dwolla_id,
            topic=topic,
        )

        if not "customer" in topic:
            # Add account related webhooks here
            return

        account_dwolla_id = (
            self.request_data.get("_links", {})
            .get("customer", {})
            .get("href", "")
            .split("/")
            .pop()
        )
        customer_account = get_account_by_dwolla_id(
            dwolla_id=account_dwolla_id
        )
        if not customer_account:
            raise ValidationError(
                {"detail": ErrorDetail("Invalid id for customer.")}
            )

        if "transfer" in topic:
            ApplyPaymentWebhook(
                event=event, customer_account=customer_account
            ).handle()
        elif "funding_source" in topic:
            ApplyBankingWebhook(
                event=event, customer_account=customer_account
            ).handle()
        elif "beneficial_owner" in topic:
            ApplyBeneficialOwnerWebhook(
                event=event, customer_account=customer_account
            )
        else:
            ApplyOnboardingWebhook(
                event=event, customer_account=customer_account
            ).handle()

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
        self, webhook_id, dwolla_id, topic, target_resource_dwolla_id
    ):
        return create_provider_webhook_event(
            webhook_id=webhook_id,
            event_payload=self.request_data,
            dwolla_id=dwolla_id,
            topic=topic,
            target_resource_dwolla_id=target_resource_dwolla_id,
        )
