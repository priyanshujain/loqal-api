from api import serializers
from apps.account.models import ConsumerAccount
from apps.order.models import Order
from apps.payment.models.payment import Payment

__all__ = ("MerchantPaymentHistoryResponse",)


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


class MerchantPaymentHistoryResponse(serializers.ModelSerializer):
    status = serializers.ChoiceEnumSerializer(read_only=True)
    charge_status = serializers.ChoiceEnumSerializer(read_only=True)
    customer = CustomerDetailsResponse(source="order.consumer", read_only=True)
    order_total_amount = serializers.CharField(
        source="order.total_amount", read_only=True
    )
    order_net_amount = serializers.CharField(
        source="order.total_net_amount", read_only=True
    )
    order_return_amount = serializers.CharField(
        source="order.total_return_amount", read_only=True
    )
    discount = PaymentDiscountResponse(source="order", read_only=True)

    class Meta:
        model = Payment
        fields = (
            "created_at",
            "payment_tracking_id",
            "status",
            "charge_status",
            "customer",
            "order_total_amount",
            "order_net_amount",
            "order_return_amount",
            "discount",
        )
