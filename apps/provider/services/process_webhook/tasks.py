import logging

from celery import shared_task

from apps.account.dbapi import consumer
from apps.account.dbapi.webhooks import get_account_by_dwolla_id
from apps.provider.dbapi import (get_pending_webhook_event,
                                 get_provider_webhook_event)

from .banking import ApplyBankingWebhook
from .beneficial_owners import ApplyBeneficialOwnerWebhook
from .onboarding import ApplyOnboardingWebhook
from .payments import ApplyPaymentWebhook

logger = logging.getLogger(__name__)


@shared_task(queue="psp_webhook")
def process_webhook_event(event_id):
    current_event = get_provider_webhook_event(event_id=event_id)
    if not current_event:
        logger.warning("Invalid webhook event: need to check it.")
        return

    if not "customer" in current_event.topic:
        # Add account related webhooks here
        return

    def process_event(event):
        account_dwolla_id = (
            event.event_payload.get("_links", {})
            .get("customer", {})
            .get("href", "")
            .split("/")
            .pop()
        )
        customer_account = get_account_by_dwolla_id(
            dwolla_id=account_dwolla_id
        )
        if not customer_account:
            return

        if "transfer" in event.topic:
            ApplyPaymentWebhook(
                event=event, customer_account=customer_account
            ).handle()
        elif "funding_source" in event.topic:
            ApplyBankingWebhook(
                event=event, customer_account=customer_account
            ).handle()
        elif "beneficial_owner" in event.topic:
            ApplyBeneficialOwnerWebhook(
                event=event,
                customer_account=customer_account,
            ).handle()
        else:
            ApplyOnboardingWebhook(
                event=event, customer_account=customer_account
            ).handle()

    target_resource_dwolla_id = current_event.target_resource_dwolla_id
    pending_events = get_pending_webhook_event(
        target_resource_dwolla_id=target_resource_dwolla_id
    )
    for event in pending_events:
        process_event(event=event)


def process_past_webhooks_for_transaction(transaction):
    pending_events = get_pending_webhook_event(
        target_resource_dwolla_id=transaction.dwolla_id
    )
    for event in pending_events:
        account_dwolla_id = (
            event.event_payload.get("_links", {})
            .get("customer", {})
            .get("href", "")
            .split("/")
            .pop()
        )
        customer_account = get_account_by_dwolla_id(
            dwolla_id=account_dwolla_id
        )
        if not customer_account:
            return

        ApplyPaymentWebhook(
            event=event,
            customer_account=customer_account,
            transaction=transaction,
        ).handle()


def process_single_webhook_event(event):
    if not "customer" in event.topic:
        # Add account related webhooks here
        logger.warning("Non customer related events received")
        return

    account_dwolla_id = (
        event.event_payload.get("_links", {})
        .get("customer", {})
        .get("href", "")
        .split("/")
        .pop()
    )
    customer_account = get_account_by_dwolla_id(dwolla_id=account_dwolla_id)
    if not customer_account:
        logger.warning("Invalid dwolla customer in given webhook")
        return

    if "transfer" in event.topic:
        ApplyPaymentWebhook(
            event=event, customer_account=customer_account
        ).handle()
    elif "funding_source" in event.topic:
        ApplyBankingWebhook(
            event=event, customer_account=customer_account
        ).handle()
    elif "beneficial_owner" in event.topic:
        ApplyBeneficialOwnerWebhook(
            event=event,
            customer_account=customer_account,
        ).handle()
    else:
        ApplyOnboardingWebhook(
            event=event, customer_account=customer_account
        ).handle()
