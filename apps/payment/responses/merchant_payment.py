from decimal import Decimal

from api import serializers
from apps.account.models import ConsumerAccount
from apps.banking.models import BankAccount
from apps.payment.models import Transaction
from apps.payment.models.payment import Payment, PaymentEvent
from apps.payment.models.refund import Refund
from apps.payment.options import PaymentProcess

from .payment import RewardUsageResponse, TransactionDiscountResponse

__all__ = (
    "MerchantTransactionHistoryResponse",
    "PaymentDetailsResponse",
    "PaymentListResponse",
    "CustomerBasicDetailsResponse",
    "DirectMerchantPaymentResponse",
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


class CustomerBasicDetailsResponse(CustomerDetailsResponse):
    class Meta:
        model = ConsumerAccount
        fields = ("first_name", "last_name", "loqal_id", "created_at")


class MerchantTransactionHistoryResponse(serializers.ModelSerializer):
    payment_status = serializers.ChoiceEnumSerializer(
        source="payment.status", read_only=True
    )
    payment_tracking_id = serializers.CharField(
        source="payment.payment_tracking_id", read_only=True
    )
    transaction_status = serializers.ChoiceEnumSerializer(
        source="status", read_only=True
    )
    customer = CustomerDetailsResponse(
        source="payment.order.consumer", read_only=True
    )
    order_total_amount = serializers.CharField(
        source="payment.order.total_amount", read_only=True
    )
    order_net_amount = serializers.CharField(
        source="payment.order.total_net_amount", read_only=True
    )
    order_return_amount = serializers.CharField(
        source="payment.order.total_return_amount", read_only=True
    )
    amount = serializers.CharField(read_only=True)
    sender_source_type = serializers.ChoiceCharEnumSerializer(read_only=True)
    recipient_source_type = serializers.ChoiceCharEnumSerializer(
        read_only=True
    )
    reward_usage = RewardUsageResponse(read_only=True)
    discount = TransactionDiscountResponse(source="payment.order", read_only=True)

    class Meta:
        model = Transaction
        fields = (
            "created_at",
            "amount",
            "payment_tracking_id",
            "transaction_tracking_id",
            "currency",
            "payment_status",
            "transaction_status",
            "is_success",
            "customer",
            "order_total_amount",
            "order_net_amount",
            "order_return_amount",
            "sender_source_type",
            "recipient_source_type",
            "reward_usage",
            "discount",
        )


class DirectMerchantPaymentResponse(serializers.ModelSerializer):
    payment_status = serializers.ChoiceCharEnumSerializer(
        source="status", read_only=True
    )
    customer = CustomerDetailsResponse(source="order.consumer", read_only=True)
    amount = serializers.CharField(source="captured_amount", read_only=True)

    class Meta:
        model = Payment
        fields = (
            "created_at",
            "amount",
            "payment_tracking_id",
            "payment_status",
            "customer",
        )


class SenderAcconutResponse(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = (
            "bank_logo_base64",
            "bank_name",
            "account_number_suffix",
        )


class TransactionPaymentResponse(serializers.ModelSerializer):
    payment_account = SenderAcconutResponse(
        source="sender_bank_account", read_only=True
    )
    merchant_rating = serializers.BooleanField(
        source="merchant_rating.give_thanks", read_only=True
    )

    class Meta:
        model = Transaction
        fields = (
            "created_at",
            "amount",
            "currency",
            "is_success",
            "fee_amount",
            "fee_currency",
            "payment_account",
            "transaction_tracking_id",
            "merchant_rating",
        )


class RefundResponse(serializers.ModelSerializer):
    refund_type = serializers.CharField(
        source="refund_type.label", read_only=True
    )
    status = serializers.CharField(source="status.label", read_only=True)

    class Meta:
        model = Refund
        fields = (
            "created_at",
            "refund_type",
            "amount",
            "status",
        )


class PaymentEventResponse(serializers.ModelSerializer):
    event_type = serializers.CharField(
        source="event_type.label", read_only=True
    )

    class Meta:
        model = PaymentEvent
        fields = (
            "created_at",
            "event_type",
            "parameters",
        )


class PaymentDetailsResponse(serializers.ModelSerializer):
    refunds = RefundResponse(many=True, read_only=True)
    events = PaymentEventResponse(many=True, read_only=True)
    customer = CustomerDetailsResponse(source="order.consumer", read_only=True)
    charge_status = serializers.CharField(
        source="charge_status.label", read_only=True
    )
    payment_status = serializers.CharField(
        source="status.label", read_only=True
    )
    order_total_amount = serializers.CharField(
        source="order.total_amount", read_only=True
    )
    order_net_amount = serializers.CharField(
        source="order.total_net_amount", read_only=True
    )
    order_return_amount = serializers.CharField(
        source="order.total_return_amount", read_only=True
    )
    transaction = serializers.SerializerMethodField("get_transaction_details")
    tip_amount = serializers.SerializerMethodField("get_tip_amount")

    class Meta:
        model = Payment
        fields = (
            "created_at",
            "captured_amount",
            "refunds",
            "events",
            "payment_currency",
            "transaction",
            "charge_status",
            "payment_status",
            "customer",
            "tip_amount",
            "order_total_amount",
            "order_net_amount",
            "order_return_amount",
        )

    def get_transaction_details(self, obj):
        transaction = None
        self.tip_amount = Decimal(0.0)
        if obj.payment_process == PaymentProcess.PAYMENT_REQUEST:
            payment_requests = obj.payment_requests
            if not payment_requests.exists():
                return None
            payment_request = payment_requests.first()
            transaction = payment_request.transaction
            self.tip_amount = payment_request.tip_amount

        if obj.payment_process in [
            PaymentProcess.QRCODE,
            PaymentProcess.DIRECT_APP,
        ]:
            direct_merchant_payments = obj.direct_merchant_payments
            if not direct_merchant_payments.exists():
                return None
            direct_merchant_payment = direct_merchant_payments.first()
            transaction = direct_merchant_payment.transaction
            self.tip_amount = direct_merchant_payment.tip_amount

        if transaction:
            return TransactionPaymentResponse(transaction).data

        return None

    def get_tip_amount(self, obj):
        if self.tip_amount:
            return self.tip_amount
        return Decimal(0.0)


class PaymentListResponse(serializers.ModelSerializer):
    charge_status = serializers.CharField(
        source="charge_status.label", read_only=True
    )
    status = serializers.CharField(source="status.label", read_only=True)
    payment_process = serializers.CharField(
        source="payment_process.label", read_only=True
    )
    tip_amount = serializers.SerializerMethodField("get_tip_amount")

    class Meta:
        model = Payment
        fields = (
            "payment_tracking_id",
            "created_at",
            "status",
            "charge_status",
            "captured_amount",
            "payment_process",
            "tip_amount",
        )

    def get_tip_amount(self, obj):
        if obj.payment_process == PaymentProcess.PAYMENT_REQUEST:
            payment_requests = obj.payment_requests
            if not payment_requests.exists():
                return None
            payment_request = payment_requests.first()
            return payment_request.tip_amount

        if obj.payment_process in [
            PaymentProcess.QRCODE,
            PaymentProcess.DIRECT_APP,
        ]:
            direct_merchant_payments = obj.direct_merchant_payments
            if not direct_merchant_payments.exists():
                return None
            direct_merchant_payment = direct_merchant_payments.first()
            return direct_merchant_payment.tip_amount

        return Decimal(0.0)
