from django.db.models import Q

from utils.shortcuts import generate_encryption_key, rand_str

from .models import (PaymentAccount, PaymentAccountOpeningConsent,
                     PaymentAccountOpeningCreds, PaymentProvider,
                     PaymentProviderCred, ProviderUpdateWebhook, TermsDocument)
from .options import PaymentAccountStatus


def get_provider_cred(provider_slug, api_environment):
    try:
        return PaymentProviderCred.objects.get(
            provider__provider_slug=provider_slug,
            api_environment=api_environment,
        )
    except PaymentProviderCred.DoesNotExist:
        return None


def get_payment_account(provider_slug, account_id):
    try:
        return PaymentAccount.objects.get(
            provider__provider_slug=provider_slug, account_id=account_id
        )
    except PaymentAccount.DoesNotExist:
        return None


def get_submitted_payment_accounts(account_id):
    return PaymentAccount.objects.filter(account_id=account_id).exclude(
        Q(status=PaymentAccountStatus.TERMS_ACCEPTED)
        | Q(status=PaymentAccountStatus.ONBOARDING_DATA_ERROR)
        | Q(status=PaymentAccountStatus.CLIENT_SUBMITTED)
    )


def get_provider(provider_id):
    try:
        return PaymentProvider.objects.get(id=provider_id)
    except PaymentProvider.DoesNotExist:
        return None


def approved_payment_accounts(account_id):
    return PaymentAccount.objects.filter(
        status=PaymentAccountStatus.KEYS_PROVIDED, account_id=account_id
    )


def check_all_payment_accounts_approved(account_id):
    return (
        PaymentAccount.objects.filter(account_id=account_id)
        .exclude(status=PaymentAccountStatus.KEYS_PROVIDED)
        .count()
        == 0
    )


def all_payment_accounts(account_id):
    return PaymentAccount.objects.filter(account_id=account_id)


def is_all_payment_accounts_approved(account_id):
    return (
        approved_payment_accounts(account_id=account_id).count()
        == all_payment_accounts(account_id=account_id).count()
    )


def get_provider_terms(provider_id, term_id):
    try:
        return TermsDocument.objects.get(id=term_id, provider_id=provider_id)
    except TermsDocument.DoesNotExist:
        return None


def get_payment_account_creds(provider_slug, account_id):
    payment_account = get_payment_account(provider_slug, account_id)
    if not payment_account:
        return None
    try:
        return payment_account.account_opening_creds
    except PaymentAccountOpeningCreds.DoesNotExist:
        return None


def create_payment_account(provider_id, account_id):
    payment_account, _ = PaymentAccount.objects.get_or_create(
        account_id=account_id,
        provider_id=provider_id,
        status=PaymentAccountStatus.CLIENT_SUBMITTED,
    )
    return payment_account


def create_payment_account_opening_consent(
    payment_account_id, term_id, user_agent, ip, consent_timestamp
):
    return PaymentAccountOpeningConsent.objects.create(
        payment_account_id=payment_account_id,
        term_id=term_id,
        user_agent=user_agent,
        ip=ip,
        consent_timestamp=consent_timestamp,
    )


def create_payment_account_openingcreds(
    payment_account_id, api_key, account_number
):
    (
        payment_account_openingcreds,
        _,
    ) = PaymentAccountOpeningCreds.objects.get_or_create(
        payment_account_id=payment_account_id,
        api_key=api_key,
        account_number=account_number,
    )
    return payment_account_openingcreds


def create_provider_webhook(provider_id, api_key):
    return ProviderUpdateWebhook.objects.create(
        provider_id=provider_id,
        webhook_id=rand_str(),
        webhook_secret=generate_encryption_key(),
        api_key=api_key,
    )


def get_provider_terms_documents(provider_slug, country):
    terms_document_qs = TermsDocument.objects.filter(
        provider__provider_slug=provider_slug, country=country, is_active=True
    )
    if not terms_document_qs.exists():
        return None
    return terms_document_qs


def get_all_payment_providers():
    return PaymentProvider.objects.all()


def get_provider_update_webhook(webhook_id):
    try:
        return ProviderUpdateWebhook.objects.get(webhook_id=webhook_id)
    except ProviderUpdateWebhook.DoesNotExist:
        return None


def get_payment_account_creds_by_apikey(api_key, provider_slug):
    try:
        return PaymentAccountOpeningCreds.objects.get(
            api_key=api_key,
            payment_account__provider__provider_slug=provider_slug,
        )
    except PaymentAccountOpeningCreds.DoesNotExist:
        return None
