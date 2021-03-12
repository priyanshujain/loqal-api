from api import serializers
from apps.payment.models import MerchantReceiveLimit, PaymentRegister

__all__ = (
    "PaymentRegisterResponse",
    "MerchantReceiveLimitResponse",
)


class PaymentRegisterResponse(serializers.ModelSerializer):
    class Meta:
        model = PaymentRegister
        fields = (
            "currency",
            "daily_send_limit",
            "weekly_send_limit",
            "daily_usage",
            "daily_usage_start_time",
            "weekly_usage",
            "weekly_usage_start_time",
            "passcode_required_minimum",
        )


class MerchantReceiveLimitResponse(serializers.ModelSerializer):
    class Meta:
        model = MerchantReceiveLimit
        fields = (
            "currency",
            "transaction_limit",
        )
