from api import serializers
from apps.account.models import ConsumerAccount
from apps.banking.models import BankAccount
from apps.payment.models import Transaction, TransactionEvent
from apps.payment.options import TransactionType


class BankAcconutResponse(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = (
            "bank_logo_base64",
            "bank_name",
            "account_number_suffix",
        )


class ConsumerResponse(serializers.ModelSerializer):
    first_name = serializers.CharField(
        source="user.first_name", read_only=True
    )
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    loqal_id = serializers.CharField(source="username", read_only=True)

    class Meta:
        model = ConsumerAccount
        fields = (
            "first_name",
            "last_name",
            "loqal_id",
        )


class TransactionEventResponse(serializers.ModelSerializer):
    event_type = serializers.ChoiceCharEnumSerializer(read_only=True)

    class Meta:
        model = TransactionEvent
        fields = (
            "created_at",
            "event_timestamp",
            "event_type",
            "parameters",
        )


class SettlementDetailsResponse(serializers.ModelSerializer):
    payment_tracking_id = serializers.CharField(
        source="payment.payment_tracking_id", read_only=True
    )
    banks_details = serializers.SerializerMethodField("get_bank_details")
    is_credit = serializers.SerializerMethodField("is_credit_transaction")
    failure_reason_type = serializers.ChoiceCharEnumSerializer(read_only=True)
    consumer = ConsumerResponse(
        source="payment.order.consumer", read_only=True
    )
    transaction_type = serializers.ChoiceCharEnumSerializer(read_only=True)
    status = serializers.ChoiceCharEnumSerializer(read_only=True)
    sender_status = serializers.ChoiceCharEnumSerializer(read_only=True)
    receiver_status = serializers.ChoiceCharEnumSerializer(read_only=True)
    events = TransactionEventResponse(many=True, read_only=True)

    class Meta:
        model = Transaction
        fields = (
            "created_at",
            "amount",
            "currency",
            "fee_amount",
            "fee_currency",
            "is_sender_tranfer_pending",
            "is_sender_failure",
            "payment_tracking_id",
            "is_success",
            "banks_details",
            "is_credit",
            "is_disputed",
            "failure_reason_type",
            "failure_reason_message",
            "ach_return_code",
            "ach_return_description",
            "ach_return_explaination",
            "consumer",
            "status",
            "sender_status",
            "receiver_status",
            "events",
            "transaction_type",
        )

    def get_bank_details(self, obj):
        bank_account = None
        self.refund = obj.refund_payment
        if self.refund:
            bank_account = obj.recipient_bank_account
        else:
            bank_account = obj.sender_bank_account
        return BankAcconutResponse(bank_account).data

    def is_credit_transaction(self, obj):
        if self.refund:
            return True
        if obj.transaction_type == TransactionType.CREDIT_REWARD_CASHBACK:
            return True
        return False


class SettlementListResponse(serializers.ModelSerializer):
    status = serializers.ChoiceCharEnumSerializer(read_only=True)
    payment_id = serializers.CharField(
        source="payment.payment_tracking_id", read_only=True
    )
    transaction_id = serializers.CharField(
        source="transaction_tracking_id", read_only=True
    )
    transaction_type = serializers.ChoiceCharEnumSerializer(read_only=True)
    consumer = ConsumerResponse(
        source="payment.order.consumer", read_only=True
    )

    class Meta:
        model = Transaction
        fields = (
            "created_at",
            "amount",
            "currency",
            "transaction_type",
            "status",
            "payment_id",
            "transaction_id",
            "is_success",
            "consumer",
        )
