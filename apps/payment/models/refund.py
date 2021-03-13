from django.conf import settings
from django.db import models
from django.utils.crypto import get_random_string

from apps.payment.options import RefundReasonTypes, RefundStatus, RefundType
from apps.reward.models import RewardUsage
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
    refund_reason = ChoiceCharEnumField(
        max_length=256,
        enum_type=RefundReasonTypes,
        default=RefundReasonTypes.RETURNS,
    )
    refund_note = models.CharField(
        max_length=256,
        blank=True,
    )
    payment = models.ForeignKey(
        Payment,
        null=True,
        blank=True,
        related_name="refunds",
        on_delete=models.CASCADE,
    )
    requested_items_value = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0,
    )
    amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0,
    )
    return_reward_value = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0,
    )
    reclaim_reward_value = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0,
    )
    reward_credit = models.ForeignKey(
        RewardUsage,
        null=True,
        blank=True,
        related_name="refunds",
        on_delete=models.CASCADE,
    )
    refund_tracking_id = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        default=None,
        unique=True,
        editable=False,
    )

    class Meta:
        db_table = "payment_refund"

    def add_transaction(self, transaction, save=True):
        self.transaction = transaction
        if save:
            self.save()

    def set_refund_failed(self, transaction=None, save=True):
        if transaction:
            self.transaction = transaction
        self.status = RefundStatus.FAILED
        if save:
            self.save()

    def add_reward_credit(self, reward_credit, save=True):
        self.reward_credit = reward_credit
        if save:
            self.save()

    def save(self, *args, **kwargs):
        def id_generator():
            return get_random_string(
                length=10, allowed_chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            )

        if not self.refund_tracking_id:
            self.refund_tracking_id = id_generator()
            while Refund.objects.filter(
                refund_tracking_id=self.refund_tracking_id
            ).exists():
                self.refund_tracking_id = id_generator()
        return super().save(*args, **kwargs)
