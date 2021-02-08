from django.utils.translation import gettext as _

from api.services import ServiceBase
from apps.merchant.dbapi import get_all_beneficial_owners
from apps.provider.dbapi import get_pending_webhook_event
from apps.provider.services.process_webhook.tasks import process_webhook_event

__all__ = ("ProcessPendingOnboardingWebhooks",)


class ProcessPendingOnboardingWebhooks(ServiceBase):
    def __init__(self, merchant):
        self.merchant = merchant

    def handle(self):
        customer_dwolla_id = self.merchant.account.dwolla_id
        self.process_webhook(dwolla_id=customer_dwolla_id)

        beneficial_owners = get_all_beneficial_owners(
            merchant_id=self.merchant.id
        )
        for owner in beneficial_owners:
            self.process_webhook(owner.dwolla_id)

    def process_webhook(self, dwolla_id):
        if not dwolla_id:
            return
        events = get_pending_webhook_event(target_resource_dwolla_id=dwolla_id)
        if events.exists():
            event = events.first()
            process_webhook_event(event_id=event.id)
