from decimal import Decimal

from django.db.utils import IntegrityError

from apps.payment.models import MerchantReceiveLimit, PaymentRegister

__all__ = (
    "create_merchant_receive_limit",
    "update_merchant_receive_limit",
    "update_consumer_limit",
    "get_payment_register",
    "get_merchant_receive_limit",
)


def create_merchant_receive_limit(merchant_id, transaction_limit=Decimal(500)):
    try:
        return MerchantReceiveLimit.objects.create(
            merchant_id=merchant_id, transaction_limit=transaction_limit
        )
    except IntegrityError:
        return None


def update_merchant_receive_limit(merchant_id, transaction_limit):
    MerchantReceiveLimit.objects.filter(merchant_id=merchant_id).update(
        transaction_limit=transaction_limit
    )


def update_consumer_limit(account_id, daily_send_limit):
    PaymentRegister.objects.filter(account_id=account_id).update(
        daily_send_limit=daily_send_limit
    )


def get_payment_register(account_id):
    try:
        return PaymentRegister.objects.get(account_id=account_id)
    except PaymentRegister.DoesNotExist:
        return None


def get_merchant_receive_limit(merchant_id):
    try:
        return MerchantReceiveLimit.objects.get(merchant_id=merchant_id)
    except MerchantReceiveLimit.DoesNotExist:
        return None
