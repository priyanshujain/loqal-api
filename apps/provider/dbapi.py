from django.db.utils import IntegrityError

from integrations.options import IntegratedProviders
from utils.shortcuts import generate_encryption_key, rand_str

from .models import (PaymentProvider, PaymentProviderCred, ProviderWebhook,
                     ProviderWebhookEvent, TermsDocument)


def get_provider_cred(provider_slug, api_environment):
    try:
        return PaymentProviderCred.objects.get(
            provider__provider_slug=provider_slug,
            api_environment=api_environment,
        )
    except PaymentProviderCred.DoesNotExist:
        return None


def get_provider(provider_slug=IntegratedProviders.DWOLLA):
    try:
        return PaymentProvider.objects.get(provider_slug=provider_slug)
    except PaymentProvider.DoesNotExist:
        return None


def get_provider_terms(provider_id, term_id):
    try:
        return TermsDocument.objects.get(id=term_id, provider_id=provider_id)
    except TermsDocument.DoesNotExist:
        return None


def get_provider_terms_documents(provider_slug, country):
    terms_document_qs = TermsDocument.objects.filter(
        provider__provider_slug=provider_slug, country=country, is_active=True
    )
    if not terms_document_qs.exists():
        return None
    return terms_document_qs


def get_all_payment_providers():
    return PaymentProvider.objects.all()


def create_provider_webhook(provider_id):
    try:
        return ProviderWebhook.objects.create(
            provider_id=provider_id,
            webhook_id=rand_str(),
            webhook_secret=generate_encryption_key(),
        )
    except IntegrityError:
        return None


def get_provider_webhook(webhook_id):
    try:
        return ProviderWebhook.objects.get(webhook_id=webhook_id)
    except ProviderWebhook.DoesNotExist:
        return None


def get_all_provider_webhook():
    return ProviderWebhook.objects.filter(is_active=True)


def get_provider_webhook_events(webhook_id):
    return ProviderWebhookEvent.objects.filter(webhook_id=webhook_id)


def create_provider_webhook_event(
    webhook_id,
    event_payload,
    dwolla_id,
    topic,
    target_resource_dwolla_id,
    event_timestamp,
):
    try:
        return ProviderWebhookEvent.objects.create(
            webhook_id=webhook_id,
            event_payload=event_payload,
            dwolla_id=dwolla_id,
            topic=topic,
            event_timestamp=event_timestamp,
            target_resource_dwolla_id=target_resource_dwolla_id,
        )
    except IntegrityError:
        return None
