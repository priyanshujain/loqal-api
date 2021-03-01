from collections import defaultdict
from enum import Flag

from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _

from apps.account.models import MerchantAccount
from apps.order.models import Order
from db.models import AbstractBaseModel
from db.models.fields import ChoiceCharEnumField

from .options import LoyaltyParameters, RewardType, RewardValueType


class LoyaltyProgram(AbstractBaseModel):
    merchant = models.ForeignKey(
        MerchantAccount,
        on_delete=models.CASCADE,
        related_name="loyalty_program",
    )
    loyalty_parameter = ChoiceCharEnumField(
        max_length=32,
        enum_type=LoyaltyParameters,
    )
    min_visits = models.PositiveSmallIntegerField(default=1)
    min_total_purchase = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0,
    )
    program_start_date = models.DateTimeField(null=True)
    program_end_date = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=True)
    reward_value_type = ChoiceCharEnumField(
        max_length=32,
        enum_type=RewardValueType,
    )
    reward_value = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0,
    )
    reward_type = ChoiceCharEnumField(
        max_length=32, enum_type=RewardType, default=RewardType.ENTIRE_SALE
    )
    reward_value_maximum = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0,
    )
    reward_start_date = models.DateTimeField(null=True)
    reward_end_date = models.DateTimeField(null=True)

    class Meta:
        db_table = "loyalty_program"

    def de_activate(self, save=True):
        self.is_active = False
        if save:
            self.save()


class CashReward(AbstractBaseModel):
    total_value = models.DecimalField(
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
    loyalty_program = models.ForeignKey(
        LoyaltyProgram, on_delete=models.CASCADE, related_name="cash_rewards"
    )
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="cash_rewards"
    )

    class Meta:
        db_table = "cash_reward"


class VoucherReward(AbstractBaseModel):
    value = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0,
    )
    is_used = models.BooleanField(default=False)
    expires_at = models.DateTimeField(null=True)
    loyalty_program = models.ForeignKey(
        LoyaltyProgram,
        on_delete=models.CASCADE,
        related_name="voucher_rewards",
    )
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="voucher_rewards"
    )

    class Meta:
        db_table = "voucher_reward"


class RewardUsage(AbstractBaseModel):
    total_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0,
    )
    is_credit = models.BooleanField(default=False)
    reward_value_type = ChoiceCharEnumField(
        max_length=32,
        enum_type=RewardValueType,
    )
    loyalty_program = models.ForeignKey(
        LoyaltyProgram, on_delete=models.CASCADE, related_name="reward_usage"
    )
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="reward_usage"
    )

    class Meta:
        db_table = "reward_usage"


class RewardUsageItem(AbstractBaseModel):
    voucher_reward = models.OneToOneField(
        VoucherReward,
        on_delete=models.CASCADE,
        related_name="usage",
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
    )
    usage = models.ForeignKey(
        RewardUsage, on_delete=models.CASCADE, related_name="items"
    )

    class Meta:
        db_table = "reward_usage_item"
