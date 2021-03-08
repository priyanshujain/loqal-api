from api import serializers
from apps.reward.options import LoyaltyParameters, RewardValueType

__all__ = (
    "CreateLoyaltyProgramValidator",
    "EditLoyaltyProgramValidator",
)


class CreateLoyaltyProgramValidator(serializers.ValidationSerializer):
    loyalty_parameter = serializers.EnumChoiceField(
        enum_type=LoyaltyParameters
    )
    min_visits = serializers.IntegerField(default=1)
    min_total_purchase = serializers.DecimalField(
        min_value=0,
        max_digits=10,
        decimal_places=6,
        coerce_to_string=False,
        default=0,
    )
    program_months = serializers.IntegerField(required=False)
    reward_value_type = serializers.EnumChoiceField(
        enum_type=RewardValueType,
    )
    reward_value = serializers.DecimalField(
        min_value=0,
        max_digits=10,
        decimal_places=6,
        coerce_to_string=False,
        default=0,
    )
    reward_value_maximum = serializers.DecimalField(
        min_value=0,
        max_digits=10,
        decimal_places=6,
        coerce_to_string=False,
        default=0,
    )


class EditLoyaltyProgramValidator(serializers.ValidationSerializer):
    min_visits = serializers.IntegerField(default=1)
    min_total_purchase = serializers.DecimalField(
        min_value=0,
        max_digits=10,
        decimal_places=6,
        coerce_to_string=False,
        default=0,
    )
    program_months = serializers.IntegerField(required=False)
    reward_value_type = serializers.EnumChoiceField(
        enum_type=RewardValueType,
    )
    reward_value = serializers.DecimalField(
        min_value=0,
        max_digits=10,
        decimal_places=6,
        coerce_to_string=False,
        default=0,
    )
    reward_value_maximum = serializers.DecimalField(
        min_value=0,
        max_digits=10,
        decimal_places=6,
        coerce_to_string=False,
        default=0,
    )
