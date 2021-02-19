from datetime import timedelta

from django.db.models import Q
from django.utils.timezone import now

from apps.payment.models import PaymentRegister, Transaction
from apps.payment.options import TransactionType


def get_payment_register(account_id):
    try:
        return PaymentRegister.objects.get(account_id=account_id)
    except PaymentRegister.DoesNotExist:
        return None


def get_transactions_by_bank_account(bank_account_id, from_datetime):
    return Transaction.objects.filter(
        created_at__gte=from_datetime,
        sender_bank_account_id=bank_account_id,
        is_success=True,
    )


def get_pending_transactions_sender(bank_account_id):
    return Transaction.objects.filter(
        sender_bank_account_id=bank_account_id,
        is_success=True,
        is_sender_tranfer_pending=True,
    )


def get_pending_transactions_receiver(bank_account_id):
    return Transaction.objects.filter(
        is_success=True,
        recipient_bank_account_id=bank_account_id,
        is_receiver_tranfer_complete=False,
    )


def get_pending_transactions_all(bank_account_id):
    return Transaction.objects.filter(is_success=True).filter(
        Q(
            sender_bank_account_id=bank_account_id,
            is_sender_tranfer_pending=True,
        )
        | Q(
            recipient_bank_account_id=bank_account_id,
            is_receiver_tranfer_complete=False,
        )
    )


def empty_transactions():
    return Transaction.objects.none()


def get_30days_transactions_consumer(consumer_account_id):
    time_from = now() - timedelta(days=30)
    time_to = now()
    return Transaction.objects.filter(
        payment__order__consumer_id=consumer_account_id,
        is_success=True,
    ).filter(Q(created_at__gte=time_from) & Q(created_at__lte=time_to))


def get_30days_transactions_merchant(merchant_account_id):
    time_from = now() - timedelta(days=30)
    time_to = now()
    return Transaction.objects.filter(
        payment__order__merchant_id=merchant_account_id,
        is_success=True,
    ).filter(Q(created_at__gte=time_from) & Q(created_at__lte=time_to))


def get_transactions_in_period(time_from, time_to):
    return (
        Transaction.objects.filter(
            is_success=True,
        )
        .filter(Q(created_at__gte=time_from) & Q(created_at__lte=time_to))
        .filter(
            Q(transaction_type=TransactionType.DIRECT_MERCHANT_PAYMENT)
            | Q(transaction_type=TransactionType.PAYMENT_REQUEST)
        )
    )
