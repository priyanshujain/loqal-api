from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _

from apps.account.models import MerchantAccount
from apps.reward.options import LoyaltyParameters, RewardType, RewardValueType
from db.models import AbstractBaseModel
from db.models.fields import ChoiceCharEnumField


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
