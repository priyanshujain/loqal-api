from django.db.models import Q

from apps.payment.models import PaymentRegister, Transaction


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


def get_pending_transactions_merchant(bank_account_id):
    return Transaction.objects.filter(
        sender_bank_account_id=bank_account_id,
        is_success=True,
    ).filter(
        Q(is_sender_tranfer_pending=True)
        | Q(is_receiver_tranfer_complete=False)
    )


def empty_transactions():
    return Transaction.objects.none()
