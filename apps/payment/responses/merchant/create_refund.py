from api import serializers
from apps.account.models import ConsumerAccount
from apps.order.models import Order
from apps.payment.models import Transaction
from apps.payment.models.refund import Refund

__all__ = (
    "RefundTransactionsResponse",
    "CreateRefundResponse",
)


class CustomerDetailsResponse(serializers.ModelSerializer):
    first_name = serializers.CharField(
        source="user.first_name", read_only=True
    )
    last_name = serializers.SerializerMethodField("get_last_name")
    loqal_id = serializers.CharField(source="username", read_only=True)

    class Meta:
        model = ConsumerAccount
        fields = (
            "first_name",
            "last_name",
            "loqal_id",
            "created_at",
        )

    def get_last_name(self, obj):
        last_name = obj.user.last_name
        if last_name:
            return last_name[0]
        return ""


class PaymentDiscountResponse(serializers.ModelSerializer):
    discount_type = serializers.ChoiceCharEnumSerializer(read_only=True)

    class Meta:
        model = Order
        fields = (
            "discount_amount",
            "discount_name",
            "discount_type",
        )


class RefundTransactionsResponse(serializers.ModelSerializer):
    status = serializers.ChoiceEnumSerializer(read_only=True)
    amount = serializers.CharField(read_only=True)
    sender_source_type = serializers.ChoiceCharEnumSerializer(read_only=True)
    recipient_source_type = serializers.ChoiceCharEnumSerializer(
        read_only=True
    )
    transaction_type = serializers.ChoiceCharEnumSerializer(read_only=True)
    refund_tracking_id = serializers.CharField(
        source="refund_payment.refund_tracking_id", read_only=True
    )

    class Meta:
        model = Transaction
        fields = (
            "created_at",
            "amount",
            "transaction_tracking_id",
            "currency",
            "status",
            "is_success",
            "sender_source_type",
            "recipient_source_type",
            "transaction_type",
            "refund_tracking_id",
        )


class CreateRefundResponse(serializers.ModelSerializer):
    refund_type = serializers.ChoiceCharEnumSerializer(read_only=True)
    status = serializers.ChoiceEnumSerializer(read_only=True)
    payment_tracking_id = serializers.CharField(
        source="payment.payment_tracking_id", read_only=True
    )
    customer = CustomerDetailsResponse(
        source="payment.order.consumer", read_only=True
    )
    amount = serializers.CharField(read_only=True)

    class Meta:
        model = Refund
        fields = (
            "created_at",
            "refund_type",
            "refund_tracking_id",
            "payment_tracking_id",
            "customer",
            "status",
            "amount",
            "return_reward_value",
            "reclaim_reward_value",
        )
