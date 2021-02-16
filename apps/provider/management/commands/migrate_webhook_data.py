from django.core.management.base import BaseCommand

from apps.provider.models import ProviderWebhookEvent


class Command(BaseCommand):
    def handle(self, *args, **options):
        events = ProviderWebhookEvent.objects.all()
        for event in events:
            if not "customer" in event.topic:
                continue
            customer_dwolla_id = (
                event.event_payload.get("_links", {})
                .get("customer", {})
                .get("href", "")
                .split("/")
                .pop()
            )
            if not customer_dwolla_id:
                continue
            if not event.customer_dwolla_id:
                event.customer_dwolla_id = customer_dwolla_id
                event.save()
