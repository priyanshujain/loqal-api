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
    expires_at = models.DateTimeField(null=True)
    is_cancelled = models.BooleanField(default=False)
    cancellation_reason = models.CharField(max_length=256, blank=True)
    loyalty_program = models.ForeignKey(
        LoyaltyProgram, on_delete=models.CASCADE, related_name="cash_rewards"
    )

    class Meta:
        db_table = "cash_reward"


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
