from api import serializers
from apps.account.models import ConsumerAccount
from apps.banking.models import BankAccount
from apps.payment.models import Transaction
from apps.payment.models.refund import Refund
from apps.reward.models import RewardUsage

__all__ = ("MerchantRefundDetailsResponse",)


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


class BankAcconutResponse(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = (
            "bank_logo_base64",
            "bank_name",
            "account_number_suffix",
        )


class RefundTransactionBasicInfoResponse(serializers.ModelSerializer):
    status = serializers.ChoiceEnumSerializer(read_only=True)
    amount = serializers.CharField(read_only=True)
    sender_source_type = serializers.ChoiceCharEnumSerializer(read_only=True)
    recipient_source_type = serializers.ChoiceCharEnumSerializer(
        read_only=True
    )
    transaction_type = serializers.ChoiceCharEnumSerializer(read_only=True)
    banks_details = serializers.SerializerMethodField("get_bank_details")

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

    def get_bank_details(self, obj):
        self.refund_payment = None
        bank_account = None
        self.refund_payment = obj.refund_payment
        bank_account = obj.recipient_bank_account
        if not self.refund_payment:
            bank_account = obj.sender_bank_account
        if bank_account:
            return BankAcconutResponse(bank_account).data
        return None


class MerchantRefundDetailsResponse(serializers.ModelSerializer):
    refund_type = serializers.ChoiceCharEnumSerializer(read_only=True)
    status = serializers.ChoiceEnumSerializer(read_only=True)
    payment_tracking_id = serializers.CharField(
        source="payment.payment_tracking_id", read_only=True
    )
    customer = CustomerDetailsResponse(
        source="payment.order.consumer", read_only=True
    )
    refund_reason = serializers.ChoiceCharEnumSerializer(read_only=True)
    transactions = RefundTransactionBasicInfoResponse(
        many=True, read_only=True
    )

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
            "transactions",
            "refund_reason",
            "refund_note",
        )
