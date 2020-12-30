from django.db.utils import IntegrityError

from apps.payment.models.transaction import DisputeTransaction

__all__ = (
    "create_dispute_transaction",
    "get_dispute_transaction",
    "get_dispute_by_id",
    "get_consumer_dispute_by_transaction",
)


def create_dispute_transaction(transaction_id, reason_type, reason_message):
    try:
        return DisputeTransaction.objects.create(
            transaction_id=transaction_id,
            reason_type=reason_type,
            reason_message=reason_message,
        )
    except IntegrityError:
        return None


def get_dispute_transaction(transaction_id):
    try:
        return DisputeTransaction.objects.get(transaction_id=transaction_id)
    except DisputeTransaction.DoesNotExist:
        return None


def get_consumer_dispute_by_transaction(consumer_account, transaction_id):
    try:
        return DisputeTransaction.objects.get(
            transaction_id=transaction_id,
            transaction__payment__order__consumer=consumer_account,
        )
    except DisputeTransaction.DoesNotExist:
        return None


def get_dispute_by_id(merchant_account, dispute_id):
    try:
        return DisputeTransaction.objects.get(
            dispute_tracking_id=dispute_id,
            transaction__payment__order__merchant=merchant_account,
        )
    except DisputeTransaction.DoesNotExist:
        return None
