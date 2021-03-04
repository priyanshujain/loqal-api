from api import serializers
from apps.rewards.models import (CashReward, LoyaltyProgram, RewardUsage,
                                 RewardUsageItem, VoucherReward)


class CashRewardResponse(serializers.ModelSerializer):
    class Meta:
        model = CashReward
        fields = (
            "created_at",
            "available_value",
            "used_value",
            "is_full_used",
        )


class VoucherRewardResponse(serializers.ModelSerializer):
    class Meta:
        model = VoucherReward
        fields = (
            "created_at",
            "value",
            "value_maximum",
            "is_used",
        )
