from django.conf import settings
from django.db import models

from apps.payment.options import RefundStatus, RefundType
from db.models import AbstractBaseModel
from db.models.fields import ChoiceCharEnumField
from db.models.fields.enum import ChoiceEnumField

from .payment import Payment
from .transaction import Transaction

__all__ = ("Refund",)


class Refund(AbstractBaseModel):
    refund_type = ChoiceCharEnumField(max_length=32, enum_type=RefundType)
    transaction = models.OneToOneField(
        Transaction,
        null=True,
        blank=True,
        related_name="refund",
        on_delete=models.CASCADE,
    )
    status = ChoiceEnumField(
        enum_type=RefundStatus, default=RefundStatus.PROCESSED
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
