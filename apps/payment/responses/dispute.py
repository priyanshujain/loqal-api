from api import serializers
from apps.account.models import ConsumerAccount
from apps.payment.models import DisputeTransaction

from .payment import MerchantDetailsResponse

__all__ = (
    "DisputeHistoryResponse",
    "DisputeListResponse",
    "ConsumerDisputeDetailsResponse",
    "MerchantDisputeDetailsResponse",
    "StaffDisputeDetailsResponse",
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
        )

    def get_last_name(self, obj):
        last_name = obj.user.last_name
        if last_name:
            return last_name[0]
        return ""


class DisputeHistoryResponse(serializers.ModelSerializer):
    dispute_type = serializers.ChoiceCharEnumSerializer(read_only=True)
    status = serializers.ChoiceCharEnumSerializer(read_only=True)
    payment_tracking_id = serializers.CharField(
        source="transaction.payment.payment_tracking_id", read_only=True
    )
    customer = CustomerDetailsResponse(
        source="transaction.payment.order.consumer", read_only=True
    )

    class Meta:
        model = DisputeTransaction
        fields = (
            "created_at",
            "dispute_type",
            "dispute_tracking_id",
            "payment_tracking_id",
            "is_closed",
            "customer",
            "status",
        )


class DisputeListResponse(serializers.ModelSerializer):
    dispute_type = serializers.ChoiceCharEnumSerializer(read_only=True)
    status = serializers.ChoiceCharEnumSerializer(read_only=True)
    payment_tracking_id = serializers.CharField(
        source="transaction.payment.payment_tracking_id", read_only=True
    )
    reason_type = serializers.ChoiceCharEnumSerializer(read_only=True)

    class Meta:
        model = DisputeTransaction
        fields = (
            "created_at",
            "dispute_type",
            "dispute_tracking_id",
            "payment_tracking_id",
            "reason_type",
            "is_closed",
            "status",
        )


class ConsumerDisputeDetailsResponse(serializers.ModelSerializer):
    status = serializers.ChoiceCharEnumSerializer(read_only=True)
    reason_type = serializers.ChoiceCharEnumSerializer(read_only=True)

    class Meta:
        model = DisputeTransaction
        fields = (
            "created_at",
            "dispute_tracking_id",
            "reason_type",
            "status",
            "reason_message",
            "reason_type",
            "resolution",
            "notes",
            "is_closed",
        )


class MerchantDisputeDetailsResponse(serializers.ModelSerializer):
    dispute_type = serializers.ChoiceCharEnumSerializer(read_only=True)
    status = serializers.ChoiceCharEnumSerializer(read_only=True)
    transaction_tracking_id = serializers.CharField(
        source="transaction.transaction_tracking_id", read_only=True
    )
    amount = serializers.CharField(source="transaction.amount", read_only=True)
    payment_tracking_id = serializers.CharField(
        source="transaction.payment.payment_tracking_id", read_only=True
    )
    reason_type = serializers.ChoiceCharEnumSerializer(read_only=True)
    customer = CustomerDetailsResponse(
        source="transaction.payment.order.consumer", read_only=True
    )

    class Meta:
        model = DisputeTransaction
        fields = (
            "created_at",
            "dispute_type",
            "dispute_tracking_id",
            "payment_tracking_id",
            "transaction_tracking_id",
            "status",
            "customer",
            "reason_message",
            "reason_type",
            "notes",
            "dispute_type",
            "resolution",
            "is_closed",
            "amount",
        )


class StaffDisputeDetailsResponse(serializers.ModelSerializer):
    dispute_type = serializers.ChoiceCharEnumSerializer(read_only=True)
    status = serializers.ChoiceCharEnumSerializer(read_only=True)
    transaction_tracking_id = serializers.CharField(
        source="transaction.transaction_tracking_id", read_only=True
    )
    amount = serializers.CharField(source="transaction.amount", read_only=True)
    payment_tracking_id = serializers.CharField(
        source="transaction.payment.payment_tracking_id", read_only=True
    )
    reason_type = serializers.ChoiceCharEnumSerializer(read_only=True)
    customer = CustomerDetailsResponse(
        source="transaction.payment.order.consumer", read_only=True
    )
    merchant = MerchantDetailsResponse(
        source="transaction.payment.order.merchant", read_only=True
    )

    class Meta:
        model = DisputeTransaction
        fields = (
            "created_at",
            "dispute_type",
            "dispute_tracking_id",
            "payment_tracking_id",
            "transaction_tracking_id",
            "status",
            "customer",
            "merchant",
            "reason_message",
            "reason_type",
            "notes",
            "dispute_type",
            "is_closed",
            "amount",
            "resolution",
        )
