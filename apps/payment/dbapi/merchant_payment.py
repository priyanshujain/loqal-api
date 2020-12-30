"""
Merchant payments relted db operations.
"""

from apps.payment.models.transaction import DisputeTransaction
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
from apps.payment.options import PaymentStatus, TransactionTypes, RefundStatus
from utils.types import to_float
from apps.order.models import Order


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


def get_merchant_disputes(merchant_account):
    """"""
    return DisputeTransaction.objects.filter(
        transaction__payment__order__merchant=merchant_account
    )


def get_merchant_customers(merchant_account):
    aggregate_consumers = []
    consumers = [
        order.consumer
        for order in Order.objects.filter(merchant=merchant_account).distinct(
            "consumer"
        )
    ]
    for consumer in consumers:
        payment_stats = Payment.objects.filter(
            order__consumer=consumer,
            status=PaymentStatus.CAPTURED,
        ).aggregate(
            total_payment_amount=Sum("captured_amount"),
            total_payments=Count("id"),
        )
        refund_stats = Refund.objects.filter(
            payment__order__consumer=consumer,
            status=RefundStatus.PROCESSED,
        ).aggregate(
            total_refund_amount=Sum("amount"),
            total_refunds=Count("id"),
        )
        aggregate_consumers.append(
            {
                "created_at": consumer.created_at,
                "consumer_loqal_id": consumer.username,
                "first_name": consumer.user.first_name,
                "last_name": consumer.user.last_name,
                "total_payments": payment_stats["total_payments"],
                "total_payment_amount": to_float(payment_stats["total_payment_amount"]),
                "total_refund_amount": to_float(refund_stats["total_refund_amount"]),
                "total_refunds": refund_stats["total_refunds"],
            }
        )
    return aggregate_consumers



def get_customer_details(merchant_account, customer_id):
    payments = Payment.objects.filter(
        order__merchant=merchant_account, order__consumer__username=customer_id
    )
    if not payments.exists():
        return None
    consumer_account = payments.first().order.consumer
    refunds = Refund.objects.filter(
            payment__order__consumer=consumer_account,
        )
    disputes = DisputeTransaction.objects.filter(
            transaction__payment__order__consumer=consumer_account,
        )
    return {
        "consumer_account": consumer_account,
        "payments": payments,
        "refunds": refunds,
        "disputes": disputes,
    }

