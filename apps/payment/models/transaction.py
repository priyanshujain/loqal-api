from django.conf import settings
from django.db import models
from django.utils.crypto import get_random_string

from apps.account.models import Account
from apps.banking.models import BankAccount
from apps.payment.options import (ChargeStatus, DisputeReasonType,
                                  DisputeStatus, DisputeType, PaymentStatus,
                                  TransactionEventType, TransactionStatus,
                                  TransactionType)
from apps.provider.options import DEFAULT_CURRENCY
from db.models import AbstractBaseModel
from db.models.fields import ChoiceCharEnumField, ChoiceEnumField
from utils.shortcuts import generate_uuid_hex

from .payment import Payment

__all__ = (
    "Transaction",
    "DisputeTransaction",
)


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
    is_disputed = models.BooleanField(default=False)
    status = ChoiceEnumField(
        enum_type=TransactionStatus, default=TransactionStatus.NOT_SENT
    )
    correlation_id = models.CharField(
        default=generate_uuid_hex, editable=False, unique=True, max_length=40
    )
    transaction_tracking_id = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        default=None,
        unique=True,
        editable=False,
    )
    transaction_type = ChoiceCharEnumField(
        max_length=32,
        enum_type=TransactionType,
        default=TransactionType.DIRECT_MERCHANT_PAYMENT,
    )
    dwolla_id = models.CharField(max_length=255, blank=True)
    individual_ach_id = models.CharField(
        max_length=32, null=True, blank=True, default=None, unique=True
    )

    class Meta:
        db_table = "transaction"

    def add_dwolla_id(
        self,
        dwolla_id,
        individual_ach_id,
        status,
        amount_towards_order,
        save=True,
    ):
        self.dwolla_id = dwolla_id
        self.individual_ach_id = individual_ach_id
        self.status = status
        self.is_success = True
        if status == TransactionStatus.PENDING:
            if self.transaction_type in [
                TransactionType.PAYMENT_REQUEST,
                TransactionType.DIRECT_MERCHANT_PAYMENT,
            ]:
                self.payment.capture_payment(
                    amount=self.amount,
                    amount_towards_order=amount_towards_order,
                )
            if self.transaction_type == TransactionType.REFUND_PAYMENT:
                self.payment.update_charge_status_by_refund(self.amount)
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
                length=10, allowed_chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            )

        if not self.transaction_tracking_id:
            self.transaction_tracking_id = id_generator()
            while Transaction.objects.filter(
                transaction_tracking_id=self.transaction_tracking_id
            ).exists():
                self.transaction_tracking_id = id_generator()
        return super().save(*args, **kwargs)

    def enable_disputed(self, save=True):
        self.is_disputed = True
        if save:
            self.save()


class TransactionEvent(AbstractBaseModel):
    transaction = models.ForeignKey(
        Transaction,
        blank=True,
        null=True,
        related_name="events",
        on_delete=models.CASCADE,
    )
    event_type = ChoiceEnumField(enum_type=TransactionEventType)
    parameters = models.JSONField(blank=True, default=dict)

    class Meta:
        db_table = "transaction_event"


class DisputeTransaction(AbstractBaseModel):
    transaction = models.OneToOneField(
        Transaction,
        blank=True,
        null=True,
        related_name="dispute",
        on_delete=models.CASCADE,
    )
    dispute_tracking_id = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        default=None,
        unique=True,
        editable=False,
    )
    status = ChoiceEnumField(
        enum_type=DisputeStatus,
        default=DisputeStatus.OPEN,
    )
    dispute_type = ChoiceCharEnumField(
        max_length=32,
        enum_type=DisputeType,
        default=DisputeType.CHARGEBACK,
    )
    reason_type = ChoiceCharEnumField(
        max_length=32,
        enum_type=DisputeReasonType,
        default=DisputeReasonType.OTHER,
    )
    reason_message = models.TextField(default="")

    class Meta:
        db_table = "dispute_transaction"

    def save(self, *args, **kwargs):
        def id_generator():
            return get_random_string(
                length=10, allowed_chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            )

        if not self.dispute_tracking_id:
            self.dispute_tracking_id = id_generator()
            while DisputeTransaction.objects.filter(
                dispute_tracking_id=self.dispute_tracking_id
            ).exists():
                self.dispute_tracking_id = id_generator()
        return super().save(*args, **kwargs)
