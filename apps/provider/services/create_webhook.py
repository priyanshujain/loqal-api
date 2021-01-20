from urllib.parse import urljoin

from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ProviderAPIException
from api.services import ServiceBase
from apps.provider.dbapi import create_provider_webhook, get_provider
from apps.provider.lib.actions import ProviderAPIActionBase

__all__ = ("CreateProviderWebhook",)


class CreateProviderWebhook(ServiceBase):
    def __init__(self):
        self.provider = get_provider()

    def handle(self):
        provider_webhook = self._factory_provider_webhook()
        webhook_path = reverse(
            "provider_webhook",
            kwargs={"webhook_id": provider_webhook.webhook_id},
        )
        webhook_url = urljoin(settings.API_BASE_URL, webhook_path)
        webhook_data = {
            "webhook_url": webhook_url,
            "webhook_secret": provider_webhook.webhook_secret,
        }
        dwolla_response = self._send_to_dwolla(webhook_data=webhook_data)
        provider_webhook.add_dwolla_id(dwolla_id=dwolla_response["dwolla_id"])
        return provider_webhook

    def _factory_provider_webhook(self):
        return create_provider_webhook(provider_id=self.provider.id)

    def _send_to_dwolla(self, webhook_data):
        api_action = CreateWebhookAPIAction()
        api_response = api_action.create(webhook_data=webhook_data)
        return api_response


class CreateWebhookAPIAction(ProviderAPIActionBase):
    def create(self, webhook_data):

        response = self.client.management.create_webhook(data=webhook_data)
        if self.get_errors(response):
            raise ProviderAPIException(
                {
                    "detail": ErrorDetail(
                        _(
                            "Banking service failed, Please try "
                            "again. If the problem persists please "
                            "contact our support team."
                        )
                    )
                }
            )
        return {
            "status": response["data"].get("status"),
            "dwolla_id": response["data"].get("dwolla_id"),
        }
