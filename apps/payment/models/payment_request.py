from django.conf import settings
from django.db import models

from apps.account.models import Account
from apps.payment.options import PaymentRequestStatus
from apps.provider.options import DEFAULT_CURRENCY
from db.models import AbstractBaseModel
from db.models.fields import ChoiceEnumField

from .payment import Payment
from .transaction import Transaction

__all__ = ("PaymentRequest",)


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
        related_name="related_payment_request",
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = "payment_request"

    def reject(self, save=True):
        self.status = PaymentRequestStatus.REJECTED
        self.payment.cancelled_payment()
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

    def add_payment(self, payment, save=True):
        self.payment = payment
        if save:
            self.save()

    def set_failed(self, save=True):
        self.status = PaymentRequestStatus.FAILED
        if save:
            self.save()
