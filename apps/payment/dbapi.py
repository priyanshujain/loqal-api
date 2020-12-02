from django.db.models import Q

from apps.payment.models import PaymentRequest, RateQuote, Transaction

from .options import PaymentRequestStatuses, TransactionStatus


def get_transaction_by_provider(provider_transaction_id, account_id):
    try:
        return Transaction.objects.get(
            provider_transaction_id=provider_transaction_id,
            account_id=account_id,
        )
    except Transaction.DoesNotExist:
        return None


def get_pending_payment_requests(account_id):
    return PaymentRequest.objects.filter(account_id=account_id).filter(
        Q(status=PaymentRequestStatuses.DEFAULT)
        | Q(status=PaymentRequestStatuses.APPROVAL_PENDING)
    )


def get_rejected_payment_requests(account_id):
    return PaymentRequest.objects.filter(account_id=account_id).filter(
        status=PaymentRequestStatuses.REJECTED
    )


def get_payment_request(payment_request_id, account_id):
    try:
        return PaymentRequest.objects.get(
            id=payment_request_id, account_id=account_id
        )
    except PaymentRequest.DoesNotExist:
        return None


def get_transaction(transaction_id, account_id):
    try:
        return Transaction.objects.get(
            id=transaction_id, account_id=account_id
        )
    except Transaction.DoesNotExist:
        return None


def get_transactions(account_id):
    return Transaction.objects.filter(account_id=account_id)


def create_payment_request(
    account_id,
    beneficiary_id,
    target_amount,
    source_currency,
    ref_document,
    payment_reference,
    purpose_of_payment,
    purpose_of_payment_code,
):
    return PaymentRequest.objects.create(
        account_id=account_id,
        beneficiary_id=beneficiary_id,
        target_amount=target_amount,
        source_currency=source_currency,
        ref_document=ref_document,
        payment_reference=payment_reference,
        purpose_of_payment=purpose_of_payment,
        purpose_of_payment_code=purpose_of_payment_code,
    )


def create_rate_quote(
    payment_account_id,
    beneficiary_id,
    provider_quote_id,
    source_currency,
    target_currency,
    rate,
    target_amount,
    expires_at,
    quote_request_time,
    quote_response_time,
    expected_transaction_date,
):
    return RateQuote.objects.create(
        payment_account_id=payment_account_id,
        beneficiary_id=beneficiary_id,
        provider_quote_id=provider_quote_id,
        source_currency=source_currency,
        target_currency=target_currency,
        rate=rate,
        target_amount=target_amount,
        expires_at=expires_at,
        quote_request_time=quote_request_time,
        quote_response_time=quote_response_time,
        expected_transaction_date=expected_transaction_date,
    )


def create_transaction(
    account_id,
    payment_request_id,
    quote_id,
    provider_transaction_id,
    fee_value,
    fee_currency,
):
    return Transaction.objects.create(
        account_id=account_id,
        payment_request_id=payment_request_id,
        quote_id=quote_id,
        provider_transaction_id=provider_transaction_id,
        fee_value=fee_value,
        fee_currency=fee_currency,
    )


def get_pending_transaction(
    account_id, provider_slug,
):
    return Transaction.objects.filter(
        account_id=account_id,
        quote__payment_account__provider__provider_slug=provider_slug,
        status=TransactionStatus.IN_PROCESS,
    )
