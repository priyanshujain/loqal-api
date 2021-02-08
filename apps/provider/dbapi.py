from django.db.models import Q
from django.db.utils import IntegrityError

from apps.account.dbapi import merchant
from apps.merchant.models import (BeneficialOwner, ControllerDetails,
                                  ControllerVerificationDocument,
                                  IncorporationVerificationDocument,
                                  OwnerVerificationDocument)
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


def get_provider_webhook_event(event_id):
    try:
        return ProviderWebhookEvent.objects.get(id=event_id)
    except ProviderWebhookEvent.DoesNotExist:
        return None


def get_pending_webhook_event(target_resource_dwolla_id):
    return ProviderWebhookEvent.objects.filter(
        target_resource_dwolla_id=target_resource_dwolla_id, is_processed=False
    ).order_by("event_timestamp")


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


def get_merchant_webhook_event(merchant_account):
    customer_dwolla_id = merchant_account.account.dwolla_id
    ba_dwolla_ids = []
    document_dwolla_ids = []
    for ba in BeneficialOwner.objects.filter(merchant_id=merchant_account.id):
        if ba.dwolla_id:
            ba_dwolla_ids.append(ba.dwolla_id)
        for document in OwnerVerificationDocument.objects.filter(
            owner_id=ba.id
        ):
            if document.dwolla_id:
                document_dwolla_ids.append(document.dwolla_id)
    try:
        controller = merchant_account.controller_details
        for document in OwnerVerificationDocument.objects.filter(
            controller_id=controller.id
        ):
            if document.dwolla_id:
                document_dwolla_ids.append(document.dwolla_id)
    except Exception:
        pass
    try:
        incorporation_details = merchant_account.incorporation_details
        for document in IncorporationVerificationDocument.objects.filter(
            incorporation_details_id=incorporation_details.id
        ):
            if document.dwolla_id:
                document_dwolla_ids.append(document.dwolla_id)
    except Exception:
        pass

    return ProviderWebhookEvent.objects.filter(
        Q(target_resource_dwolla_id=customer_dwolla_id)
        | Q(target_resource_dwolla_id__in=ba_dwolla_ids)
        | Q(target_resource_dwolla_id__in=document_dwolla_ids)
    ).order_by("event_timestamp")


def get_webhook_event(id):
    try:
        return ProviderWebhookEvent.objects.get(id=id)
    except ProviderWebhookEvent.DoesNotExist:
        return None
