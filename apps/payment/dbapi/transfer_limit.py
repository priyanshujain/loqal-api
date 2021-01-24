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
