from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _

from apps.account.models import ConsumerAccount
from db.models import AbstractBaseModel

from .loyalty import LoyaltyProgram


class CashReward(AbstractBaseModel):
    consumer = models.ForeignKey(
        ConsumerAccount,
        related_name="cash_rewards",
        on_delete=models.CASCADE,
    )
    available_value = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0,
    )
    used_value = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0,
    )
    is_full_used = models.BooleanField(default=False)
    expires_at = models.DateTimeField(null=True)
    is_cancelled = models.BooleanField(default=False)
    cancellation_reason = models.CharField(max_length=256, blank=True)
    loyalty_program = models.ForeignKey(
        LoyaltyProgram, on_delete=models.CASCADE, related_name="cash_rewards"
    )

    class Meta:
        db_table = "cash_reward"

    def update_usage(self, used_amount, save=True):
        self.available_value -= used_amount
        self.used_value += used_amount
        if self.available_value == Decimal(0.0):
            self.is_full_used = True
        if save:
            self.save()

    def refund(self, refund_amount, save=True):
        self.available_value += refund_amount
        self.used_value -= refund_amount
        if self.available_value == Decimal(0.0):
            self.is_full_used = True
        else:
            self.is_full_used = False
        if save:
            self.save()


class VoucherReward(AbstractBaseModel):
    consumer = models.ForeignKey(
        ConsumerAccount,
        related_name="voucher_rewards",
        on_delete=models.CASCADE,
    )
    value = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0,
    )
    value_maximum = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0,
    )
    is_used = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    cancellation_reason = models.CharField(max_length=256, blank=True)
    expires_at = models.DateTimeField(null=True)
    loyalty_program = models.ForeignKey(
        LoyaltyProgram,
        on_delete=models.CASCADE,
        related_name="voucher_rewards",
    )

    class Meta:
        db_table = "voucher_reward"

    def update_usage(self, save=True):
        self.is_used = True
        if save:
            self.save()

    def refund(self, save=True):
        self.is_used = False
        if save:
            self.save()
