"""
Payments relted db operations.
"""

from decimal import Decimal

from django.conf import settings
from django.db.models import Q
from django.db.utils import IntegrityError

from apps.order.models import Order
from apps.payment.models import (DirectMerchantPayment, Payment, PaymentQrCode,
                                 PaymentRegister, PaymentRequest, Refund,
                                 Transaction)
from apps.payment.options import (PaymentRequestStatus, PaymentStatus,
                                  TransactionSourceTypes, TransactionStatus,
                                  TransactionType)
from apps.provider.options import DEFAULT_CURRENCY


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
    customer_ip_address,
    sender_bank_account_id=None,
    recipient_bank_account_id=None,
    amount=Decimal(0.0),
    currency=DEFAULT_CURRENCY,
    fee_bearer_account_id=None,
    fee_amount=Decimal(0.0),
    fee_currency=DEFAULT_CURRENCY,
    payment_id=None,
    sender_source_type=TransactionSourceTypes.NA,
    recipient_source_type=TransactionSourceTypes.NA,
    refund_payment_id=None,
    direct_merchant_payment_id=None,
    payment_request_id=None,
    reward_usage_id=None,
    transaction_type=TransactionType.DIRECT_MERCHANT_PAYMENT,
    min_access_balance_required=Decimal(
        settings.MIN_BANK_ACCOUNT_BALANCE_REQUIRED
    ),
    is_success=False,
    status=TransactionStatus.NOT_SENT,
):
    """
    dbapi for creating new transaction.
    """
    try:
        return Transaction.objects.create(
            sender_bank_account_id=sender_bank_account_id,
            recipient_bank_account_id=recipient_bank_account_id,
            amount=Decimal(amount),
            currency=currency,
            fee_bearer_account_id=fee_bearer_account_id,
            fee_amount=Decimal(fee_amount),
            fee_currency=fee_currency,
            payment_id=payment_id,
            customer_ip_address=customer_ip_address,
            transaction_type=transaction_type,
            min_access_balance_required=min_access_balance_required,
            sender_source_type=sender_source_type,
            recipient_source_type=recipient_source_type,
            refund_payment_id=refund_payment_id,
            direct_merchant_payment_id=direct_merchant_payment_id,
            payment_request_id=payment_request_id,
            reward_usage_id=reward_usage_id,
            is_success=is_success,
            status=status,
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
        return PaymentQrCode.objects.get(
            qrcode_id=qrcode_id, merchant_id=merchant_id
        )
    except PaymentQrCode.DoesNotExist:
        return None


def get_single_qrcode_by_id(qrcode_id):
    """
    get QR code by qrcode_id
    """
    try:
        return PaymentQrCode.objects.get(qrcode_id=qrcode_id)
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


def get_all_qrcodes():
    """
    Get all QR codes
    """
    return PaymentQrCode.objects.all()


def get_cashier_qrcode(merchant_id, cashier_id):
    """
    Get QR code for a cashier
    """
    try:
        return PaymentQrCode.objects.get(
            merchant_id=merchant_id, cashier_id=cashier_id
        )
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
    amount,
    currency,
    cashier_id=None,
):
    """
    dbapi for creating new payment request.
    """
    try:
        return PaymentRequest.objects.create(
            account_from_id=account_from_id,
            account_to_id=account_to_id,
            amount=Decimal(amount),
            currency=currency,
            cashier_id=cashier_id,
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


def create_refund_payment(
    payment_id,
    requested_items_value,
    amount,
    refund_type,
    return_reward_value,
    reclaim_reward_value,
    refund_reason,
    refund_note,
    cashier_id=None,
):
    """
    dbapi for creating new refund payment.
    """
    try:
        return Refund.objects.create(
            payment_id=payment_id,
            requested_items_value=requested_items_value,
            amount=amount,
            refund_type=refund_type,
            return_reward_value=return_reward_value,
            reclaim_reward_value=reclaim_reward_value,
            refund_reason=refund_reason,
            refund_note=refund_note,
            cashier_id=cashier_id,
        )
    except IntegrityError:
        return None


def get_merchant_payment_reqeust(account_id, is_pending=False):
    qs = PaymentRequest.objects.filter(account_from_id=account_id)
    if is_pending:
        qs = qs.filter(status=PaymentRequestStatus.REQUEST_SENT)
    return qs


def get_consumer_payment_reqeust(account_id, is_pending=False):
    qs = PaymentRequest.objects.filter(account_to_id=account_id)
    if is_pending:
        qs = qs.filter(status=PaymentRequestStatus.REQUEST_SENT)
    return qs


def get_payment_reqeust_by_uid(payment_request_id, account_to_id):
    try:
        return PaymentRequest.objects.get(
            u_id=payment_request_id, account_to_id=account_to_id
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


def get_consumer_transactions(consumer_account):
    return Transaction.objects.filter(
        Q(payment__order__consumer=consumer_account)
        | Q(reward_usage__consumer=consumer_account)
    )


def get_merchant_transactions(merchant_account):
    return Transaction.objects.filter(
        payment__order__merchant=merchant_account
    )


def get_merchant_payments(merchant_account):
    return Payment.objects.filter(order__merchant=merchant_account)


def get_merchant_transaction(merchant_account, transaction_tracking_id):
    try:
        return Transaction.objects.get(
            payment__order__merchant=merchant_account,
            transaction_tracking_id=transaction_tracking_id,
        )
    except Transaction.DoesNotExist:
        return None


def get_consumer_transaction(consumer_account, transaction_tracking_id):
    transactions = get_consumer_transactions(consumer_account=consumer_account)
    transactions = transactions.filter(
        transaction_tracking_id=transaction_tracking_id
    )
    if not transactions.exists():
        return None
    return transactions.first()


def get_recent_store_orders(consumer_account):
    return (
        Order.objects.filter(
            consumer=consumer_account, payment__status=PaymentStatus.CAPTURED
        )
        .order_by("merchant", "-updated_at")
        .distinct("merchant")
    )


def get_payment_by_id(payment_id):
    try:
        return Payment.objects.get(id=payment_id)
    except Payment.DoesNotExist:
        return None
