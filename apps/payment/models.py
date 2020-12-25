from apps.provider.lib.api import payment
from datetime import timedelta
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.account.models import Account, MerchantAccount
from apps.banking.models import BankAccount
from apps.merchant.models import AccountMember
from apps.order.models import Order
from apps.payment.options import (
    PaymentMethodType,
    PaymentRequestStatus,
    PaymentStatus,
    RefundType,
    TransactionStatus,
    ChargeStatus,
    PaymentProcess,
)
from apps.provider.options import DEFAULT_CURRENCY
from db.models import AbstractBaseModel
from db.models.fields import ChoiceCharEnumField, ChoiceEnumField
from utils.shortcuts import generate_uuid_hex
from django.utils.crypto import get_random_string


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

    class Meta:
        db_table = "payment_register"

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
    """
    This represents payment status for a single order
    """

    gateway = models.CharField(max_length=64, default="dwolla")
    payment_method_type = ChoiceCharEnumField(
        max_length=64,
        default=PaymentMethodType.ACH,
        enum_type=PaymentMethodType,
    )
    payment_process = ChoiceEnumField(
        enum_type=PaymentProcess, default=PaymentProcess.NOT_PROVIDED
    )
    captured_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=Decimal("0.0"),
    )
    charge_status = ChoiceEnumField(
        enum_type=ChargeStatus, default=ChargeStatus.NOT_CHARGED
    )
    order = models.OneToOneField(
        Order, related_name="payment", on_delete=models.CASCADE
    )
    status = ChoiceEnumField(
        enum_type=PaymentStatus,
    )

    class Meta:
        db_table = "payment"


class Transaction(AbstractBaseModel):
    sender_bank_account = models.ForeignKey(
        BankAccount,
        on_delete=models.DO_NOTHING,
        related_name="sender_transactions",
        db_index=True,
    )
    recipient_bank_account = models.ForeignKey(
        BankAccount,
        on_delete=models.DO_NOTHING,
        related_name="recipient_transactions",
        db_index=True,
    )
    sender_balance_at_checkout = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0,
    )
    payment = models.ForeignKey(
        Payment,
        blank=True,
        null=True,
        related_name="transactions",
        on_delete=models.SET_NULL,
    )
    customer_ip_address = models.GenericIPAddressField(blank=True, null=True)
    amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0,
    )
    currency = models.CharField(max_length=3, default=DEFAULT_CURRENCY)
    fee_bearer_account = models.ForeignKey(
        Account, null=True, blank=True, on_delete=models.SET_NULL
    )
    fee_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0,
    )
    fee_currency = models.CharField(max_length=3, default=DEFAULT_CURRENCY)
    is_success = models.BooleanField(default=False)
    status = ChoiceEnumField(
        enum_type=TransactionStatus, default=TransactionStatus.NOT_SENT
    )
    correlation_id = models.CharField(
        default=generate_uuid_hex, editable=False, unique=True, max_length=40
    )
    tracking_number = models.CharField(
        max_length=10, null=True, blank=True, default=None, unique=True, editable=False
    )
    dwolla_id = models.CharField(max_length=255, blank=True)
    individual_ach_id = models.CharField(
        max_length=32, null=True, blank=True, default=None, unique=True
    )

    class Meta:
        db_table = "transaction"

    def add_dwolla_id(self, dwolla_id, individual_ach_id, status, save=True):
        self.dwolla_id = dwolla_id
        self.individual_ach_id = individual_ach_id
        self.status = status
        self.is_success = True
        if status == TransactionStatus.PENDING:
            self.payment.status = PaymentStatus.SUCCESS
            self.payment.save()
        if save:
            self.save()

    def update_status(self, status, save=True):
        self.status = status
        if save:
            self.save()

    def set_internal_error(self, save=True):
        self.status = TransactionStatus.INTERNAL_PSP_ERROR
        self.payment.status = PaymentStatus.FAILED
        self.payment.save()
        if save:
            self.save()

    def save(self, *args, **kwargs):
        def id_generator():
            return get_random_string(
                length=8, allowed_chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            )

        if not self.tracking_number:
            self.tracking_number = id_generator()
            while Transaction.objects.filter(
                tracking_number=self.tracking_number
            ).exists():
                self.tracking_number = id_generator()
        return super().save(*args, **kwargs)


class Refund(AbstractBaseModel):
    refund_type = ChoiceCharEnumField(max_length=32, enum_type=RefundType)
    transaction = models.OneToOneField(
        Transaction,
        null=True,
        blank=True,
        related_name="refund",
        on_delete=models.CASCADE,
    )
    payment = models.ForeignKey(
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

    class Meta:
        db_table = "payment_refund"

    def add_transaction(self, transaction, save=True):
        self.transaction = transaction
        if save:
            self.save()


class DirectMerchantPayment(AbstractBaseModel):
    payment_qrcode = models.ForeignKey(
        PaymentQrCode,
        blank=True,
        null=True,
        related_name="direct_merchant_payments",
        on_delete=models.SET_NULL,
    )
    tip_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0,
    )
    payment = models.ForeignKey(
        Payment,
        blank=True,
        null=True,
        related_name="direct_merchant_payments",
        on_delete=models.SET_NULL,
    )
    transaction = models.OneToOneField(
        Transaction,
        blank=True,
        null=True,
        related_name="direct_merchant_payments",
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = "direct_merchant_payment"

    def add_transaction(self, transaction, save=True):
        self.transaction = transaction
        if save:
            self.save()


class PaymentRequest(AbstractBaseModel):
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
    payment = models.ForeignKey(
        Payment,
        blank=True,
        null=True,
        related_name="payment_requests",
        on_delete=models.CASCADE,
    )
    transaction = models.OneToOneField(
        Transaction,
        blank=True,
        null=True,
        related_name="payment_request",
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = "payment_request"

    def reject(self, save=True):
        self.status = PaymentRequestStatus.REJECTED
        if save:
            self.save()

    def add_transaction(self, transaction, save=True):
        self.transaction = transaction
        self.status = PaymentRequestStatus.ACCEPTED
        if save:
            self.save()
