from apps.payment.models import Transaction


def get_transaction_by_dwolla_id(dwolla_id):
    try:
        return Transaction.objects.get(dwolla_id=dwolla_id)
    except Transaction.DoesNotExist:
        return None
