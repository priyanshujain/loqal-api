from datetime import timedelta
from decimal import Decimal
from django.db import models
from django.utils import timezone

from apps.account.models import Account, MerchantAccount
from apps.banking.models import BankAccount
from apps.merchant.models import AccountMember
from apps.payment.options import (
    PaymentRequestStatus,
    TransactionStatus,
    RefundType,
    RefundStatus,
    PaymentStatus,
    PaymentMethodType,
    QrCodePaymentStatus,
)
from apps.provider.options import DEFAULT_CURRENCY
from db.models import AbstractBaseModel
from db.models.fields import ChoiceCharEnumField, ChoiceEnumField
from utils.shortcuts import generate_uuid_hex
from apps.order.models import Order
from django.conf import settings


class PaymentRegister(AbstractBaseModel):
    account = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    currency = models.CharField(max_length=3, default=DEFAULT_CURRENCY)
    daily_send_limit = models.FloatField(default=500.0)
    weekly_send_limit = models.FloatField(default=5000.0)
    daily_usage = models.FloatField(default=0.0)
    daily_usage_start_time = models.DateTimeField(default=timezone.now)
    weekly_usage = models.FloatField(default=0.0)
    weekly_usage_start_time = models.DateTimeField(default=timezone.now)
    passcode_required_minimum = models.FloatField(default=100.0)

    def update_usage(self, amount):
        if timezone.now() > self.daily_usage_start_time + timedelta(hours=24):
            self.daily_usage_start_time = timezone.now()
            self.daily_usage = amount
        else:
            self.daily_usage += amount

        if timezone.now() > self.weekly_usage_start_time + timedelta(days=7):
            self.weekly_usage_start_time = timezone.now()
            self.weekly_usage = amount
        else:
            self.weekly_usage += amount
        self.save()

    def set_daily_limit(self, value):
        self.daily_send_limit = value
        self.save()

    def set_weekly_limit(self, value):
        self.weekly_send_limit = value
        self.save()

    def set_passcode_threshold(self, value):
        self.passcode_required_minimum = value
        self.save()

    class Meta:
        db_table = "payment_register"


class PaymentQrCode(AbstractBaseModel):
    merchant = models.ForeignKey(
        MerchantAccount, on_delete=models.CASCADE, blank=True, null=True
    )
    cashier = models.ForeignKey(
        AccountMember, on_delete=models.SET_NULL, blank=True, null=True
    )
    currency = models.CharField(max_length=3, default=DEFAULT_CURRENCY)
    qrcode_id = models.CharField(max_length=10, unique=True)
    is_expired = models.BooleanField(default=False)

    class Meta:
        db_table = "payment_qrcode"
        unique_together = (
            "merchant",
            "cashier",
        )


class Payment(AbstractBaseModel):
    gateway = models.CharField(max_length=64, default="dwolla")
    payment_method_type = ChoiceCharEnumField(
        max_length=64, default=PaymentMethodType.ACH, enum_type=PaymentMethodType
    )
    captured_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=Decimal("0.0"),
    )
    customer_ip_address = models.GenericIPAddressField(blank=True, null=True)
    order = models.ForeignKey(Order, related_name="payments", on_delete=models.CASCADE)
    status = ChoiceEnumField(
        enum_type=PaymentStatus,
    )

    class Meta:
        db_table = "payment"


class Transaction(AbstractBaseModel):
    account = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    sender = models.ForeignKey(
        BankAccount,
        on_delete=models.DO_NOTHING,
        related_name="sender_bank_account",
        db_index=True,
    )
    recipient = models.ForeignKey(
        BankAccount,
        on_delete=models.DO_NOTHING,
        related_name="recipient_bank_account",
        db_index=True,
    )
    payment = models.ForeignKey(
        Payment,
        blank=True,
        null=True,
        related_name="transactions",
        on_delete=models.SET_NULL,
    )
    amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0,
    )
    currency = models.CharField(max_length=3, default=DEFAULT_CURRENCY)
    fee_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0,
    )
    fee_currency = models.CharField(max_length=3, default=DEFAULT_CURRENCY)
    status = ChoiceEnumField(
        enum_type=TransactionStatus, default=TransactionStatus.NOT_SENT
    )
    correlation_id = models.CharField(
        default=generate_uuid_hex, editable=False, unique=True, max_length=40
    )
    dwolla_id = models.CharField(max_length=255, blank=True)

    def add_dwolla_id(self, dwolla_id):
        self.dwolla_id = dwolla_id
        self.status = TransactionStatus.PENDING
        self.save()

    class Meta:
        db_table = "transaction"


class Refund(AbstractBaseModel):
    order = models.ForeignKey(Order, related_name="refunds", on_delete=models.CASCADE)
    refund_type = ChoiceCharEnumField(max_length=32, enum_type=RefundType)
    payment = models.OneToOneField(
        Payment,
        null=True,
        blank=True,
        related_name="refunds",
        on_delete=models.CASCADE,
    )
    amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0,
    )
    status = ChoiceEnumField(
        enum_type=RefundStatus,
    )

    class Meta:
        db_table = "refund"

    def add_payment(self, payment, save=True):
        self.payment = payment
        if save:
            self.save()


class QrCodePayment(AbstractBaseModel):
    order = models.ForeignKey(
        Order, related_name="qrcode_payments", on_delete=models.CASCADE
    )
    payment_qrcode = models.ForeignKey(
        PaymentQrCode,
        blank=True,
        null=True,
        related_name="qrcode_payments",
        on_delete=models.SET_NULL,
    )
    tip_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0,
    )
    status = ChoiceEnumField(
        enum_type=QrCodePaymentStatus,
        default=QrCodePaymentStatus.IN_PROGRESS
    )
    payment = models.OneToOneField(
        Payment,
        blank=True,
        null=True,
        related_name="qrcode_payments",
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = "qrcode_payment"

    def add_payment(self, payment, save=True):
        self.payment = payment
        if save:
            self.save()

    def add_status(self, status, save=True):
        self.status = status
        if save:
            self.save()


class PaymentRequest(AbstractBaseModel):
    order = models.ForeignKey(
        Order, blank=True, null=True, related_name="payment_requests", on_delete=models.CASCADE
    )
    account_from = models.ForeignKey(
        Account,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="from_payment_requests",
    )
    account_to = models.ForeignKey(
        Account,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="to_payment_requests",
    )
    amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0,
    )
    tip_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0,
    )
    currency = models.CharField(max_length=3, default=DEFAULT_CURRENCY)
    status = ChoiceEnumField(
        enum_type=PaymentRequestStatus,
        default=PaymentRequestStatus.REQUEST_SENT,
    )
    payment = models.OneToOneField(
        Payment,
        blank=True,
        null=True,
        related_name="payment_requests",
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = "payment_request"

    def reject(self, save=True):
        self.status = PaymentRequestStatus.REJECTED
        if save:
            self.save()

    def add_payment(self, payment, save=True):
        self.payment = payment
        self.status = PaymentRequestStatus.ACCEPTED
        if save:
            self.save()
