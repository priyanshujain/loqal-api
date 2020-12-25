"""
Payments relted db operations.
"""

from decimal import Decimal

from django.db.models import Count, Sum
from django.db.utils import IntegrityError

from apps.payment.models import (
    DirectMerchantPayment,
    Payment,
    PaymentQrCode,
    PaymentRegister,
    PaymentRequest,
    Transaction,
)
from apps.payment.options import PaymentStatus, TransactionTypes
from utils.types import to_float


def create_payment_register(account_id):
    """
    dbapi for creating default payment register.
    """
    try:
        return PaymentRegister.objects.create(account_id=account_id)
    except IntegrityError:
        return None


def create_payment(
    order_id,
    payment_process,
):
    """
    dbapi for creating new transaction.
    """
    try:
        return Payment.objects.create(
            order_id=order_id,
            status=PaymentStatus.IN_PROGRESS,
            payment_process=payment_process,
        )
    except IntegrityError:
        return None


def create_transaction(
    sender_bank_account_id,
    recipient_bank_account_id,
    sender_balance_at_checkout,
    amount,
    currency,
    fee_bearer_account_id,
    fee_amount,
    fee_currency,
    payment_id,
    customer_ip_address,
):
    """
    dbapi for creating new transaction.
    """
    try:
        return Transaction.objects.create(
            sender_bank_account_id=sender_bank_account_id,
            recipient_bank_account_id=recipient_bank_account_id,
            sender_balance_at_checkout=sender_balance_at_checkout,
            amount=Decimal(amount),
            currency=currency,
            fee_bearer_account_id=fee_bearer_account_id,
            fee_amount=Decimal(fee_amount),
            fee_currency=fee_currency,
            payment_id=payment_id,
            customer_ip_address=customer_ip_address,
        )
    except IntegrityError:
        return None


def get_transactions(account_id):
    """
    get transactions for an account.
    """
    try:
        return Transaction.objects.filter(
            account_id=account_id,
        )
    except IntegrityError:
        return None


def create_payment_qrcode(qrcode_id):
    """
    Create QR code
    """
    try:
        return PaymentQrCode.objects.create(qrcode_id=qrcode_id)
    except IntegrityError:
        return None


def get_payment_qrcode(qrcode_id):
    """
    get QR code by qrcode_id
    """
    try:
        return PaymentQrCode.objects.get(qrcode_id=qrcode_id)
    except PaymentQrCode.DoesNotExist:
        return None


def get_payment_qrcode_by_id(qrcode_id, merchant_id):
    """
    get QR code by qrcode_id and merchant_id
    """
    try:
        return PaymentQrCode.objects.get(qrcode_id=qrcode_id, merchant_id=merchant_id)
    except PaymentQrCode.DoesNotExist:
        return None


def assign_payment_qrcode(qrcode_id, merchant_id, cashier_id):
    """
    Assign QR code to a merchant
    """
    PaymentQrCode.objects.filter(qrcode_id=qrcode_id).update(
        merchant_id=merchant_id, cashier_id=cashier_id
    )


def get_merchant_qrcodes(merchant_id):
    """
    Get all QR code for a merchant
    """
    qrcode_qs = PaymentQrCode.objects.filter(merchant_id=merchant_id)
    if qrcode_qs.exists():
        return qrcode_qs
    return None


def get_cashier_qrcode(merchant_id, cashier_id):
    """
    Get QR code for a cashier
    """
    try:
        return PaymentQrCode.objects.get(merchant_id=merchant_id, cashier_id=cashier_id)
    except PaymentQrCode.DoesNotExist:
        return None


def get_empty_qrcodes():
    """
    Get QR code for a cashier
    """
    return PaymentQrCode.objects.filter(merchant_id=None, cashier_id=None)


def create_payment_request(
    account_from_id,
    account_to_id,
    payment_id,
    amount,
    currency,
    order_id,
):
    """
    dbapi for creating new payment request.
    """
    try:
        return PaymentRequest.objects.create(
            account_from_id=account_from_id,
            account_to_id=account_to_id,
            payment_id=payment_id,
            amount=Decimal(amount),
            currency=currency,
            order_id=order_id,
        )
    except IntegrityError:
        return None


def create_direct_merchant_payment(
    payment_id,
    tip_amount=0,
    payment_qrcode_id=None,
):
    """
    dbapi for creating new direct merchant payment.
    """
    try:
        return DirectMerchantPayment.objects.create(
            payment_id=payment_id,
            payment_qrcode_id=payment_qrcode_id,
            tip_amount=Decimal(tip_amount),
        )
    except IntegrityError:
        return None


def get_merchant_payment_reqeust(account_id):
    return PaymentRequest.objects.filter(account_id=account_id)


def get_consumer_payment_reqeust(account_id):
    return PaymentRequest.objects.filter(requested_to_id=account_id)


def get_payment_reqeust_by_id(payment_request_id, account_to_id):
    try:
        return PaymentRequest.objects.get(
            id=payment_request_id, account_to_id=account_to_id
        )
    except PaymentRequest.DoesNotExist:
        return None


def get_transactions_to_merchant(account_id):
    """
    get transactions to a merchant's account
    """
    try:
        return Transaction.objects.filter(
            recipient__account_id=account_id,
        )
    except IntegrityError:
        return None


def get_customers_aggregate_transactions(account_id):
    aggregate_consumers = []
    consumers = [
        transaction.sender.account.consumeraccount
        for transaction in Transaction.objects.filter(
            recipient__account_id=account_id
        ).distinct("sender")
    ]
    for consumer in consumers:
        payment_stats = Transaction.objects.filter(
            sender__account_id=consumer.account.id,
            transaction_type=TransactionTypes.PAYMENT,
        ).aggregate(
            total_payment_amount=Sum("amount"),
            total_tip_amount=Sum("tip_amount"),
            total_payments=Count("id"),
        )
        refund_stats = Transaction.objects.filter(
            sender__account_id=consumer.account.id,
            transaction_type=TransactionTypes.REFUND,
        ).aggregate(
            total_refund_amount=Sum("amount"),
            total_refunds=Count("id"),
        )
        aggregate_consumers.append(
            {
                "consumer_loqal_id": consumer.username,
                "first_name": consumer.user.first_name,
                "last_name": consumer.user.last_name,
                "total_payments": payment_stats["total_payments"],
                "total_payment_amount": to_float(payment_stats["total_payment_amount"]),
                "total_tip_amount": to_float(payment_stats["total_tip_amount"]),
                "total_refund_amount": to_float(refund_stats["total_refund_amount"]),
                "total_refunds": refund_stats["total_refunds"],
            }
        )
    return aggregate_consumers
