from api import serializers
from apps.account.models import ConsumerAccount
from apps.payment.models import Transaction


__all__ = ("MerchantTransactionHistoryResponse",)


class CustomerDetailsResponse(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.SerializerMethodField("get_last_name")
    loqal_id = serializers.CharField(source="username", read_only=True)

    class Meta:
        model = ConsumerAccount
        fields = (
            "first_name",
            "last_name",
            "loqal_id",
        )

    def get_bank_logo(self, obj):
        last_name = obj.user.last_name
        if last_name:
            return last_name[0]
        return ""


class MerchantTransactionHistoryResponse(serializers.ModelSerializer):
    payment_status = serializers.CharField(
        source="payment.status.label", read_only=True
    )
    payment_tracking_id = serializers.CharField(
        source="payment.payment_tracking_id", read_only=True
    )
    transaction_status = serializers.CharField(
        source="transaction.status.label", read_only=True
    )
    customer = CustomerDetailsResponse(source="payment.order.consumer", read_only=True)

    class Meta:
        model = Transaction
        fields = (
            "created_at",
            "amount",
            "payment_tracking_id",
            "currency",
            "payment_status",
            "transaction_status",
            "is_success",
            "is_dispute",
            "customer",
        )