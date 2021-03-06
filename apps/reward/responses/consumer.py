from api import serializers
from apps.reward.models import (CashReward, LoyaltyProgram, RewardUsage,
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


class RewardUsageItemResponse(serializers.ModelSerializer):
    cash_reward = CashRewardResponse(read_only=True)
    voucher_reward = VoucherRewardResponse(read_only=True)
    payment_id = serializers.CharField(
        source="usage.order.payment.u_id", read_only=True
    )
    order_id = serializers.CharField(source="usage.order.u_id", read_only=True)
    is_credit = serializers.BooleanField(
        source="usage.is_credit", read_only=True
    )

    class Meta:
        model = RewardUsageItem
        fields = (
            "created_at",
            "amount",
            "cash_reward",
            "voucher_reward",
            "is_credit",
            "is_reclaimed",
            "payment_id",
            "order_id",
        )
