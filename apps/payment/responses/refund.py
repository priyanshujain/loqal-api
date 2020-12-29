from api import serializers
from apps.account.models import ConsumerAccount
from apps.banking.models import BankAccount
from apps.payment.models import Transaction
from apps.payment.models.payment import Payment, PaymentEvent
from apps.payment.models.refund import Refund
from apps.payment.options import PaymentProcess

__all__ = (
    "RefundHistoryResponse",
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


class RefundHistoryResponse(serializers.ModelSerializer):
    refund_type = serializers.CharField(
        source="refund_type.label", read_only=True
    )
    status = serializers.CharField(source="status.label", read_only=True)
    payment_tracking_id = serializers.CharField(source="payment.payment_tracking_id", read_only=True)
    customer = CustomerDetailsResponse(source="payment.order.consumer", read_only=True)

    class Meta:
        model = Refund
        fields = (
            "created_at",
            "refund_type",
            "refund_tracking_id",
            "payment_tracking_id",
            "customer",
            "status",
        )
