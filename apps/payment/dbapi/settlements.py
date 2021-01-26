from apps.payment.models import Transaction, payment


def get_all_merchant_transanction(merchant_id):
    return Transaction.objects.filter(payment__order__merchant_id=merchant_id)