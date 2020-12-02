from .models import PaymentProvider, PaymentProviderCred, TermsDocument


def get_provider_cred(provider_slug, api_environment):
    try:
        return PaymentProviderCred.objects.get(
            provider__provider_slug=provider_slug,
            api_environment=api_environment,
        )
    except PaymentProviderCred.DoesNotExist:
        return None


def get_provider(provider_id):
    try:
        return PaymentProvider.objects.get(id=provider_id)
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
