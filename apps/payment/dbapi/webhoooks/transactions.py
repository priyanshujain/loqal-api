from apps.payment.models import Transaction


def get_transaction(dwolla_id):
    try:
        return Transaction.objects.get(dwolla_id=dwolla_id)
    except Transaction.DoesNotExist:
        return None