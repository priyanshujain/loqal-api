from decimal import Decimal

from api import serializers
from apps.account.models import ConsumerAccount
from apps.banking.models import BankAccount
from apps.order.models import Order
from apps.payment.dbapi import transaction
from apps.payment.models import Transaction
from apps.payment.models.payment import Payment, PaymentEvent
from apps.payment.models.refund import Refund
from apps.payment.options import PaymentProcess

__all__ = ("MerchantPaymentDetailsResponse",)


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



class RefundBasicDetailsResponse(serializers.ModelSerializer):
    refund_type = serializers.ChoiceCharEnumSerializer(read_only=True)
    status = serializers.ChoiceEnumSerializer(read_only=True)

    class Meta:
        model = Refund
        fields = (
            "created_at",
            "refund_type",
            "refund_tracking_id",
            "status",
            "amount",
            "return_reward_value",
            "reclaim_reward_value",
        )


class MerchantTransactionBasicInfoResponse(serializers.ModelSerializer):
    status = serializers.ChoiceEnumSerializer(read_only=True)
    amount = serializers.CharField(read_only=True)
    sender_source_type = serializers.ChoiceCharEnumSerializer(read_only=True)
    recipient_source_type = serializers.ChoiceCharEnumSerializer(
        read_only=True
    )
    transaction_type = serializers.ChoiceCharEnumSerializer(read_only=True)
    refund_payment = RefundBasicDetailsResponse(read_only=True)

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
            "refund_payment",
        )


class PaymentEventResponse(serializers.ModelSerializer):
    event_type = serializers.ChoiceEnumSerializer(read_only=True)
    transfer_type = serializers.ChoiceCharEnumSerializer(read_only=True)

    class Meta:
        model = PaymentEvent
        fields = (
            "created_at",
            "event_type",
            "parameters",
            "transfer_type",
        )


class MerchantPaymentDetailsResponse(serializers.ModelSerializer):
    status = serializers.ChoiceEnumSerializer(read_only=True)
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
    transactions = MerchantTransactionBasicInfoResponse(
        many=True, read_only=True
    )
    events = PaymentEventResponse(many=True, read_only=True)

    class Meta:
        model = Payment
        fields = (
            "created_at",
            "captured_amount",
            "order_total_amount",
            "order_net_amount",
            "order_return_amount",
            "payment_tracking_id",
            "status",
            "customer",
            "transactions",
            "events",
            "discount",
            "total_tip_amount",
        )
