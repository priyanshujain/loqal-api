import re

from apps.payment.dbapi import transaction
from apps.payment.models import Transaction, payment


def get_all_merchant_transanction(merchant_id):
    return Transaction.objects.filter(payment__order__merchant_id=merchant_id)


def get_single_merchant_transanction(merchant_id, settlement_id):
    try:
        return Transaction.objects.get(
            payment__order__merchant_id=merchant_id,
            transaction_tracking_id=settlement_id,
        )
    except Transaction.DoesNotExist:
        return None
