from datetime import timedelta
from re import T

from django.db import models
from db.models.fields import ChoiceEnumField
from django.utils import timezone

from apps.account.models import Account, MerchantAccount
from apps.merchant.models import AccountMember
from apps.banking.models import BankAccount
from apps.payment.options import TransactionStatus, PaymentRequestStatus
from apps.provider.options import DEFAULT_CURRENCY
from db.models import AbstractBaseModel
from utils.shortcuts import generate_uuid_hex


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
    cashier = models.ForeignKey(AccountMember, on_delete=models.SET_NULL, blank=True, null=True)
    currency = models.CharField(max_length=3, default=DEFAULT_CURRENCY)
    qrcode_id = models.CharField(max_length=10, unique=True)
    is_expired = models.BooleanField(default=False)

    class Meta:
        db_table = "payment_qrcode"
        unique_together = (
            "merchant",
            "cashier",
        )


class Transaction(AbstractBaseModel):
    account = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    sender = models.ForeignKey(
        BankAccount,
        on_delete=models.DO_NOTHING,
        related_name="sender_bank_account",
    )
    recipient = models.ForeignKey(
        BankAccount,
        on_delete=models.DO_NOTHING,
        related_name="recipient_bank_account",
    )
    payment_qrcode = models.ForeignKey(
        PaymentQrCode, on_delete=models.SET_NULL, blank=True, null=True
    )
    payment_amount = models.FloatField()
    tip_amount = models.FloatField(default=0)
    payment_currency = models.CharField(max_length=3, default=DEFAULT_CURRENCY)
    fee_amount = models.FloatField(default=0.0)
    fee_currency = models.CharField(max_length=3, default=DEFAULT_CURRENCY)
    status = ChoiceEnumField(default=TransactionStatus.NOT_SENT)
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


class PaymentRequest(AbstractBaseModel):
    account = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    requested_to = models.ForeignKey(
        Account,
        on_delete=models.DO_NOTHING,
        related_name="requested_to_account",
    )
    payment_amount = models.FloatField()
    tip_amount = models.FloatField(default=0)
    payment_currency = models.CharField(max_length=3, default=DEFAULT_CURRENCY)
    status = ChoiceEnumField(default=PaymentRequestStatus.REQUEST_SENT)
    transaction = models.OneToOneField(
        Transaction, on_delete=models.CASCADE, null=True, blank=True
    )

    def add_transaction(self, transaction, save=True):
        self.transaction = transaction
        if save:
            self.save()

    class Meta:
        db_table = "payment_request"
