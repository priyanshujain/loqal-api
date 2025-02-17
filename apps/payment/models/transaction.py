from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils.crypto import get_random_string

from apps.account.models import Account
from apps.banking.models import BankAccount
from apps.payment.options import (DisputeReasonType, DisputeStatus,
                                  DisputeType, PaymentStatus,
                                  TransactionEventType,
                                  TransactionFailureReasonType,
                                  TransactionReceiverStatus,
                                  TransactionSenderStatus,
                                  TransactionSourceTypes, TransactionStatus,
                                  TransactionType)
from apps.provider.options import DEFAULT_CURRENCY
from apps.reward.models import RewardUsage
from db.models import AbstractBaseModel
from db.models.fields import ChoiceCharEnumField, ChoiceEnumField
from utils.shortcuts import generate_uuid_hex

from .payment import Payment

__all__ = (
    "Transaction",
    "DisputeTransaction",
    "TransactionEvent",
)


class Transaction(AbstractBaseModel):
    sender_bank_account = models.ForeignKey(
        BankAccount,
        on_delete=models.DO_NOTHING,
        related_name="sender_transactions",
        db_index=True,
        blank=True,
        null=True,
    )
    recipient_bank_account = models.ForeignKey(
        BankAccount,
        on_delete=models.DO_NOTHING,
        related_name="recipient_transactions",
        db_index=True,
        blank=True,
        null=True,
    )
    sender_source_type = ChoiceCharEnumField(
        enum_type=TransactionSourceTypes,
        max_length=64,
        blank=True,
        default=TransactionSourceTypes.BANK_ACCOUNT,
    )
    recipient_source_type = ChoiceCharEnumField(
        enum_type=TransactionSourceTypes,
        max_length=64,
        blank=True,
        default=TransactionSourceTypes.BANK_ACCOUNT,
    )
    sender_balance_at_checkout = models.DecimalField(
        max_digits=12,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        null=True,
        default=None,
    )
    min_access_balance_required = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        null=True,
        default=None,
    )
    payment = models.ForeignKey(
        Payment,
        blank=True,
        null=True,
        related_name="transactions",
        on_delete=models.SET_NULL,
    )
    direct_merchant_payment = models.ForeignKey(
        "payment.DirectMerchantPayment",
        blank=True,
        null=True,
        related_name="transactions",
        on_delete=models.SET_NULL,
    )
    payment_request = models.ForeignKey(
        "payment.PaymentRequest",
        blank=True,
        null=True,
        related_name="transactions",
        on_delete=models.SET_NULL,
    )
    refund_payment = models.ForeignKey(
        "payment.Refund",
        blank=True,
        null=True,
        related_name="transactions",
        on_delete=models.SET_NULL,
    )
    reward_usage = models.OneToOneField(
        RewardUsage,
        blank=True,
        null=True,
        related_name="transaction",
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
        Account,
        related_name="paid_for_transactions",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    fee_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0,
    )
    fee_currency = models.CharField(max_length=3, default=DEFAULT_CURRENCY)
    is_success = models.BooleanField(default=False)
    is_disputed = models.BooleanField(default=False)

    # Statuses
    status = ChoiceEnumField(
        enum_type=TransactionStatus, default=TransactionStatus.NOT_SENT
    )
    sender_status = ChoiceCharEnumField(
        enum_type=TransactionSenderStatus,
        max_length=128,
        default=TransactionSenderStatus.NOT_STARTED,
    )
    receiver_status = ChoiceCharEnumField(
        enum_type=TransactionReceiverStatus,
        max_length=128,
        default=TransactionReceiverStatus.NOT_STARTED,
    )
    is_sender_tranfer_pending = models.BooleanField(default=True)
    is_receiver_tranfer_complete = models.BooleanField(default=False)

    # failure related
    failure_reason_type = ChoiceCharEnumField(
        max_length=128,
        enum_type=TransactionFailureReasonType,
        default=TransactionFailureReasonType.NA,
    )
    failure_reason_message = models.CharField(max_length=512, blank=True)
    is_sender_failure = models.BooleanField(null=True, default=None)

    # ACH return related
    ach_return_code = models.CharField(max_length=32, blank=True)
    ach_return_description = models.CharField(max_length=255, blank=True)
    ach_return_explaination = models.CharField(max_length=255, blank=True)
    ach_return_bank_account = models.ForeignKey(
        BankAccount,
        on_delete=models.SET_NULL,
        related_name="ach_return_transactions",
        null=True,
        blank=True,
    )
    ach_return_account = models.ForeignKey(
        Account,
        on_delete=models.SET_NULL,
        related_name="ach_return_transactions",
        null=True,
        blank=True,
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
        sender_balance_at_checkout=None,
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
                reclaimed_amount = amount_towards_order - self.amount
                self.payment.update_charge_status_by_refund(
                    amount=self.amount, reclaimed_amount=reclaimed_amount
                )
        if sender_balance_at_checkout != None:
            sender_balance_at_checkout = Decimal(sender_balance_at_checkout)
            sender_balance_at_checkout = round(
                sender_balance_at_checkout, settings.DEFAULT_DECIMAL_PLACES
            )
            self.sender_balance_at_checkout = sender_balance_at_checkout
        if save:
            self.save()

    def update_status(self, status, save=True):
        self.status = status
        if save:
            self.save()

    def set_internal_error(self, save=True):
        self.status = TransactionStatus.UNKNOWN_PSP_ERROR
        if self.payment.status == PaymentStatus.IN_PROGRESS:
            self.payment.status = PaymentStatus.FAILED
        self.payment.save()
        if save:
            self.save()

    def complete_receiver_transfer(self, save=True):
        self.is_receiver_tranfer_complete = True
        if save:
            self.save()

    def complete_sender_transfer(self, save=True):
        self.is_sender_tranfer_pending = False
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

    def set_payment_failed(self):
        self.payment.failed_payment()

    def set_balance_check_failed(self, save=True):
        self.is_sender_failure = True
        self.failure_reason_type = (
            TransactionFailureReasonType.BALANCE_CHECK_FAILED
        )
        self.failure_reason_message = "There is error from your Bank while checking balace. Please check your connected bank account and try again."
        self.set_payment_failed()
        if save:
            self.save()

    def set_insufficient_balance(self, save=True):
        self.is_sender_failure = True
        self.failure_reason_type = (
            TransactionFailureReasonType.INSUFFICIENT_BALANCE
        )
        self.failure_reason_message = "The money in your account is not enough for this payment. Check account balance and try again."
        self.set_payment_failed()
        if save:
            self.save()

    def set_daily_limit_exceeded(self, message, save=True):
        self.is_sender_failure = True
        self.failure_reason_type = (
            TransactionFailureReasonType.TRANSACTION_DAILY_LIMIT_EXCEEDED
        )
        self.failure_reason_message = message
        self.set_payment_failed()
        if save:
            self.save()

    def set_merchant_receive_limit_exceeded(self, message, save=True):
        self.is_sender_failure = True
        self.failure_reason_type = (
            TransactionFailureReasonType.MERCHANT_RECEIVE_LIMIT_EXCEEDED
        )
        self.failure_reason_message = message
        self.set_payment_failed()
        if save:
            self.save()

    def set_weekly_limit_exceeded(self, message, save=True):
        self.is_sender_failure = True
        self.failure_reason_type = (
            TransactionFailureReasonType.TRANSACTION_WEEKLY_LIMIT_EXCEEDED
        )
        self.failure_reason_message = message
        self.set_payment_failed()
        if save:
            self.save()

    def mark_processed(self, save=True):
        self.status = TransactionStatus.PROCESSED
        if save:
            self.save()

    def mark_failed(self, save=True):
        self.status = TransactionStatus.FAILED
        if save:
            self.save()

    def mark_cancelled(self, save=True):
        self.status = TransactionStatus.CANCELLED
        if save:
            self.save()

    def mark_sender_completed(self, save=True):
        self.status = TransactionStatus.SENDER_COMPLETED
        if save:
            self.save()

    def mark_psp_error(self, save=True):
        self.status = TransactionStatus.UNKNOWN_PSP_ERROR
        if save:
            self.save()

    def mark_internal_error(self, save=True):
        self.status = TransactionStatus.INTERNAL_ERROR
        if save:
            self.save()

    def log_ach_return(
        self,
        ach_return_code,
        ach_return_description,
        ach_return_explaination,
        ach_return_bank_account,
        ach_return_account,
        save=True,
    ):
        self.ach_return_code = ach_return_code
        self.ach_return_description = ach_return_description
        self.ach_return_explaination = ach_return_explaination
        self.ach_return_bank_account = ach_return_bank_account
        self.ach_return_account = ach_return_account
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
    event_timestamp = models.DateTimeField(null=True, blank=True)
    event_type = ChoiceCharEnumField(
        max_length=128, enum_type=TransactionEventType
    )
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
    status = ChoiceCharEnumField(
        enum_type=DisputeStatus,
        default=DisputeStatus.REVIEW_WAITING,
        max_length=64,
    )
    is_closed = models.BooleanField(default=False)
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
    notes = models.TextField(default="")
    resolution = models.TextField(default="")

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

    def update_status(self, status, notes, save=True):
        self.status = status
        self.notes = notes
        if save:
            self.save()

    def close_dispute(self, resolution, status, notes, save=True):
        self.resolution = resolution
        self.status = status
        self.notes = notes
        self.is_closed = True
        if save:
            self.save()
