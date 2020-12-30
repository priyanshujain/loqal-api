"""
Merchant payments relted db operations.
"""

from decimal import Decimal

from django.db.models import Count, Q, Sum
from django.db.utils import IntegrityError
from django.utils import translation

from apps.payment.models import (
    DirectMerchantPayment,
    Payment,
    PaymentQrCode,
    PaymentRegister,
    PaymentRequest,
    Refund,
    Transaction,
)
from apps.payment.options import PaymentStatus, TransactionTypes
from utils.types import to_float


def get_merchant_payment(merchant_account, payment_id):
    """"""
    try:
        return Payment.objects.get(
            order__merchant=merchant_account, payment_tracking_id=payment_id
        )
    except Payment.DoesNotExist:
        return None


def get_merchant_refunds(merchant_account):
    """"""
    return Refund.objects.filter(payment__order__merchant=merchant_account)
