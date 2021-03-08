"""
Merchant payments relted db operations.
"""

from decimal import Decimal

from django.db.models import Count, Q, Sum
from django.db.utils import IntegrityError
from django.utils import translation

from apps.order.models import Order
from apps.payment.models import (
    DirectMerchantPayment,
    Payment,
    PaymentQrCode,
    PaymentRegister,
    PaymentRequest,
    Refund,
    Transaction,
)
from apps.payment.models.transaction import DisputeTransaction
from apps.payment.options import PaymentStatus, RefundStatus
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


def get_merchant_refund(merchant_account, refund_id):
    """"""
    try:
        return Refund.objects.get(
            payment__order__merchant=merchant_account,
            refund_tracking_id=refund_id,
        )
    except Refund.DoesNotExist:
        return None


def get_merchant_disputes(merchant_account):
    """"""
    return DisputeTransaction.objects.filter(
        transaction__payment__order__merchant=merchant_account
    )


def get_all_disputes():
    """"""
    return DisputeTransaction.objects.all()


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
            order__merchant=merchant_account,
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
        last_name = consumer.user.last_name
        if last_name and len(str(last_name)) > 0:
            last_name = str(last_name)[0]
        aggregate_consumers.append(
            {
                "created_at": consumer.created_at,
                "consumer_loqal_id": consumer.username,
                "first_name": consumer.user.first_name,
                "last_name": last_name,
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
        transaction__payment__order__merchant=merchant_account,
        transaction__payment__order__consumer=consumer_account,
    )
    return {
        "consumer_account": consumer_account,
        "payments": payments,
        "refunds": refunds,
        "disputes": disputes,
    }
