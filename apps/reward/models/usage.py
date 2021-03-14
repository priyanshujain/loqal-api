from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _

from apps.order.models import Order
from apps.reward.options import RewardValueType
from db.models import AbstractBaseModel
from db.models.fields import ChoiceCharEnumField

from .rewards import CashReward, VoucherReward


class RewardUsage(AbstractBaseModel):
    total_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0,
        null=True,
    )
    is_credit = models.BooleanField(default=False)
    reward_value_type = ChoiceCharEnumField(
        max_length=32,
        enum_type=RewardValueType,
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="reward_usages",
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "reward_usage"


class RewardUsageItem(AbstractBaseModel):
    voucher_reward = models.ForeignKey(
        VoucherReward,
        on_delete=models.CASCADE,
        related_name="usages",
        blank=True,
        null=True,
    )
    cash_reward = models.ForeignKey(
        CashReward,
        on_delete=models.CASCADE,
        related_name="usages",
        blank=True,
        null=True,
    )
    amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0,
        null=True,
    )
    usage = models.ForeignKey(
        RewardUsage, on_delete=models.CASCADE, related_name="items"
    )
    is_reclaimed = models.BooleanField(default=False)

    class Meta:
        db_table = "reward_usage_item"
