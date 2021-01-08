from django.db.utils import IntegrityError

from apps.account.models import PaymentAccountOpeningConsent

__all__ = (
    "create_payment_account_consent",
    "get_payment_account_consent",
)


def create_payment_account_consent(
    account_id,
    user_id,
    user_agent,
    ip_address,
    consent_timestamp,
    payment_term_document_id,
):
    try:
        return PaymentAccountOpeningConsent.objects.create(
            account_id=account_id,
            user_id=user_id,
            user_agent=user_agent,
            ip_address=ip_address,
            consent_timestamp=consent_timestamp,
            payment_term_document_id=payment_term_document_id,
        )
    except IntegrityError:
        return None


def get_payment_account_consent(
    account_id,
    user_id,
):
    consents = PaymentAccountOpeningConsent.objects.filter(
        account_id=account_id,
        user_id=user_id,
    ).order_by("-created_at")
    if not consents.exists():
        return None

    return consents.first()
