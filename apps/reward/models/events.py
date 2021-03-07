from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _

from apps.account.models import ConsumerAccount, MerchantAccount
from apps.reward.options import RewardEventType, RewardValueType
from db.models import AbstractBaseModel
from db.models.fields import ChoiceCharEnumField

from .rewards import CashReward, VoucherReward
from .usage import RewardUsageItem


class RewardEvent(AbstractBaseModel):
    merchant = models.ForeignKey(
        MerchantAccount,
        on_delete=models.CASCADE,
        related_name="reward_events",
    )
    consumer = models.ForeignKey(
        ConsumerAccount,
        on_delete=models.CASCADE,
        related_name="reward_events",
    )
    event_type = ChoiceCharEnumField(max_length=32, enum_type=RewardEventType)
    reward_value_type = ChoiceCharEnumField(
        max_length=32, enum_type=RewardValueType
    )
    voucher_reward = models.ForeignKey(
        VoucherReward,
        on_delete=models.CASCADE,
        related_name="events",
        blank=True,
        null=True,
    )
    cash_reward = models.ForeignKey(
        CashReward,
        on_delete=models.CASCADE,
        related_name="event_logs",
        blank=True,
        null=True,
    )
    value = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0,
        null=True,
    )
    reward_usage_item = models.ForeignKey(
        RewardUsageItem, on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        db_table = "reward_event"

    def de_activate(self, save=True):
        self.is_active = False
        if save:
            self.save()
