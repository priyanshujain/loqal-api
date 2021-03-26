import re

from django.db.models import Q

from apps.payment.models import Transaction
from apps.payment.options import TransactionSourceTypes


def get_all_merchant_transanction(merchant_id):
    return Transaction.objects.filter(
        payment__order__merchant_id=merchant_id,
        sender_source_type=TransactionSourceTypes.BANK_ACCOUNT,
        recipient_source_type=TransactionSourceTypes.BANK_ACCOUNT,
    ).filter(~Q(is_sender_failure=True))


def get_single_merchant_transanction(merchant_id, settlement_id):
    try:
        return Transaction.objects.get(
            payment__order__merchant_id=merchant_id,
            transaction_tracking_id=settlement_id,
        )
    except Transaction.DoesNotExist:
        return None
