from api import serializers
from apps.reward.models import (CashReward, LoyaltyProgram, RewardUsage,
                                 RewardUsageItem, VoucherReward)


class LoyaltyProgramResponse(serializers.ModelSerializer):
    loyalty_parameter = serializers.ChoiceCharEnumSerializer(read_only=True)
    reward_value_type = serializers.ChoiceCharEnumSerializer(read_only=True)
    reward_type = serializers.ChoiceCharEnumSerializer(read_only=True)

    class Meta:
        model = LoyaltyProgram
        fields = (
            "created_at",
            "loyalty_parameter",
            "min_visits",
            "min_total_purchase",
            "program_start_date",
            "program_end_date",
            "is_active",
            "reward_value_type",
            "reward_value",
            "reward_type",
            "reward_start_date",
            "reward_end_date",
            "reward_value_maximum",
        )
