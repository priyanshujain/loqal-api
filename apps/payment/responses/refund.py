from api import serializers
from apps.account.models import ConsumerAccount
from apps.banking.models import BankAccount
from apps.payment.models import Transaction
from apps.payment.models.refund import Refund

__all__ = (
    "RefundHistoryResponse",
    "RefundListResponse",
    "RefundDetailsResponse",
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
    refund_type = serializers.ChoiceCharEnumSerializer(read_only=True)
    status = serializers.ChoiceCharEnumSerializer(read_only=True)
    payment_tracking_id = serializers.CharField(
        source="payment.payment_tracking_id", read_only=True
    )
    customer = CustomerDetailsResponse(
        source="payment.order.consumer", read_only=True
    )
    currency = serializers.CharField(
        source="transaction.currency", read_only=True
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
            "currency",
            "return_reward_value",
            "reclaim_reward_value",
        )


class RefundListResponse(serializers.ModelSerializer):
    refund_type = serializers.CharField(
        source="refund_type.label", read_only=True
    )
    status = serializers.CharField(source="status.label", read_only=True)
    payment_tracking_id = serializers.CharField(
        source="payment.payment_tracking_id", read_only=True
    )

    class Meta:
        model = Refund
        fields = (
            "created_at",
            "amount",
            "refund_type",
            "refund_tracking_id",
            "payment_tracking_id",
            "status",
            "return_reward_value",
            "reclaim_reward_value",
        )


class SenderAcconutResponse(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = (
            "bank_logo_base64",
            "bank_name",
            "account_number_suffix",
        )


class TransactionRefundResponse(serializers.ModelSerializer):
    merchant_bank_account = SenderAcconutResponse(
        source="sender_bank_account", read_only=True
    )
    customer_bank_account = SenderAcconutResponse(
        source="recipient_bank_account", read_only=True
    )
    status = serializers.CharField(source="status.label", read_only=True)

    class Meta:
        model = Transaction
        fields = (
            "created_at",
            "amount",
            "currency",
            "is_success",
            "fee_amount",
            "fee_currency",
            "merchant_bank_account",
            "customer_bank_account",
            "transaction_tracking_id",
            "status",
        )


class RefundDetailsResponse(serializers.ModelSerializer):
    refund_type = serializers.CharField(
        source="refund_type.label", read_only=True
    )
    status = serializers.CharField(source="status.label", read_only=True)
    payment_tracking_id = serializers.CharField(
        source="payment.payment_tracking_id", read_only=True
    )
    customer = CustomerDetailsResponse(
        source="payment.order.consumer", read_only=True
    )
    transaction = TransactionRefundResponse(read_only=True)

    class Meta:
        model = Refund
        fields = (
            "created_at",
            "refund_type",
            "refund_tracking_id",
            "payment_tracking_id",
            "transaction",
            "status",
            "amount",
            "customer",
            "return_reward_value",
            "reclaim_reward_value",
        )
