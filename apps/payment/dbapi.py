"""
Payments relted db operations.
"""

import re
from django.db.utils import IntegrityError

from apps.payment.models import (
    PaymentRegister,
    Transaction,
    PaymentQrCode,
    PaymentRequest,
)


def create_payment_register(account_id):
    """
    dbapi for creating default payment register.
    """
    try:
        return PaymentRegister.objects.create(account_id=account_id)
    except IntegrityError:
        return None


def create_transaction(
    account_id,
    sender_id,
    recipient_id,
    payment_amount,
    tip_amount,
    payment_currency,
    fee_amount,
    fee_currency,
    payment_qrcode=None,
):
    """
    dbapi for creating new transaction.
    """
    try:
        return Transaction.objects.create(
            account_id=account_id,
            sender_id=sender_id,
            recipient_id=recipient_id,
            payment_amount=payment_amount,
            tip_amount=tip_amount,
            payment_currency=payment_currency,
            fee_amount=fee_amount,
            fee_currency=fee_currency,
            payment_qrcode=payment_qrcode,
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

def get_merchant_qrcodes(merchant_id, cashier_id):
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
    