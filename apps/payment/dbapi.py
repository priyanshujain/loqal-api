"""
Payments relted db operations.
"""

from django.db.utils import IntegrityError

from apps.payment.models import PaymentRegister, Transaction


def create_payment_register(account_id):
    """
    dbapi for creating default payment register.
    """
    try:
        return PaymentRegister.objects.create(account_id=account_id)
    except IntegrityError:
        return None


def create_transaction(
    account_id,
    sender_id,
    recipient_id,
    payment_amount,
    tip_amount,
    payment_currency,
    fee_amount,
    fee_currency,
):
    """
    dbapi for creating new transaction.
    """
    try:
        return Transaction.objects.create(
            account_id=account_id,
            sender_id=sender_id,
            recipient_id=recipient_id,
            payment_amount=payment_amount,
            tip_amount=tip_amount,
            payment_currency=payment_currency,
            fee_amount=fee_amount,
            fee_currency=fee_currency,
        )
    except IntegrityError:
        return None
