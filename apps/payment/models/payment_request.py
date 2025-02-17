from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils.timezone import now

from apps.account.models import Account, MerchantAccount
from apps.merchant.models import AccountMember
from apps.payment.options import PaymentRequestStatus
from apps.provider.options import DEFAULT_CURRENCY
from db.models import AbstractBaseModel
from db.models.fields import ChoiceEnumField

from .payment import Payment
from .qrcode import PaymentQrCode
from .transaction import Transaction

__all__ = (
    "PaymentRequest",
    "PrePaymentRequest",
)


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
    cashier = models.ForeignKey(
        AccountMember,
        blank=True,
        null=True,
        related_name="payment_requests",
        on_delete=models.SET_NULL,
    )
    register = models.ForeignKey(
        PaymentQrCode,
        blank=True,
        null=True,
        related_name="payment_requests",
        on_delete=models.SET_NULL,
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
        related_name="related_payment_request",
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = "payment_request"

    def reject(self, save=True):
        self.status = PaymentRequestStatus.REJECTED
        if save:
            self.save()

    def add_transaction(self, transaction, tip_amount, save=True):
        self.transaction = transaction
        self.tip_amount = tip_amount
        self.status = PaymentRequestStatus.ACCEPTED
        self.payment.capture_payment(
            amount=(self.amount + tip_amount), amount_towards_order=self.amount
        )
        if save:
            self.save()

    def add_payment(self, payment, tip_amount, save=True):
        self.payment = payment
        self.tip_amount = tip_amount
        if save:
            self.save()

    def set_failed(self, save=True):
        self.status = PaymentRequestStatus.FAILED
        if save:
            self.save()

    def set_accepted(self, save=True):
        self.status = PaymentRequestStatus.ACCEPTED
        if save:
            self.save()


class PrePaymentRequest(AbstractBaseModel):
    merchant = models.ForeignKey(
        MerchantAccount,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="from_pre_payment_requests",
    )
    register = models.ForeignKey(
        PaymentQrCode,
        blank=True,
        null=True,
        related_name="pre_payment_requests",
        on_delete=models.SET_NULL,
    )
    amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0,
    )
    phone_number = models.CharField(max_length=10, default=None, null=True)
    phone_number_country = models.CharField(max_length=2, default="US")
    expires_at = models.DateTimeField(default=now)

    class Meta:
        db_table = "pre_payment_request"

    def set_expiration(self, save=True):
        self.expires_at = now() + timedelta(hours=2)
        if save:
            self.save()
        return self.expires_at
