from decimal import Decimal

from api import serializers
from apps.account.models import Account, ConsumerAccount, MerchantAccount
from apps.banking.models import BankAccount
from apps.merchant.models import MerchantCategory
from apps.order.models import Order
from apps.payment.models import (
    DirectMerchantPayment,
    Payment,
    PaymentRequest,
    Refund,
    Transaction,
)
from apps.payment.options import PaymentProcess, TransactionType
from apps.reward.models import RewardUsage

__all__ = (
    "TransactionResponse",
    "PaymentRequestResponse",
    "ConsumerPaymentRequestResponse",
    "MerchantTransactionResponse",
    "PaymentResponse",
    "MerchantPaymentResponse",
    "RefundPaymentResponse",
    "TransactionHistoryResponse",
    "TransactionDetailsResponse",
    "RecentStoresResponse",
    "TransactionErrorDetailsResponse",
    "MerchantDetailsResponse",
    "DirectMerchantPaymentConsumerResponse",
    "CreateTransactionResponse",
)


class MerchantCategoryResponse(serializers.ModelSerializer):
    class Meta:
        model = MerchantCategory
        fields = (
            "category",
            "sub_categories",
            "is_primary",
        )


class MerchantDetailsResponse(serializers.ModelSerializer):
    full_name = serializers.CharField(source="profile.full_name", read_only=True)
    categories = MerchantCategoryResponse(many=True, read_only=True)
    address = serializers.JSONField(source="profile.address", read_only=True)

    class Meta:
        model = MerchantAccount
        fields = ("full_name", "categories", "address")


class RewardUsageResponse(serializers.ModelSerializer):
    reward_value_type = serializers.ChoiceCharEnumSerializer(read_only=True)
    merchant = MerchantDetailsResponse(read_only=True)

    class Meta:
        model = RewardUsage
        fields = (
            "reward_value_type",
            "total_amount",
            "is_credit",
            "is_first_time_credited",
        )


class TransactionDiscountResponse(serializers.ModelSerializer):
    discount_type = serializers.ChoiceCharEnumSerializer(read_only=True)

    class Meta:
        model = Order
        fields = (
            "discount_amount",
            "discount_name",
            "discount_type",
        )


class PaymentRequestMerchantDetailsResponse(serializers.ModelSerializer):
    merchant_id = serializers.CharField(source="u_id", read_only=True)
    full_name = serializers.CharField(source="profile.full_name", read_only=True)
    about = serializers.CharField(source="profile.about", read_only=True)
    categories = MerchantCategoryResponse(many=True, read_only=True)
    avatar_file_id = serializers.CharField(
        source="profile.avatar_file.id", read_only=True
    )
    address = serializers.JSONField(source="profile.address", read_only=True)

    class Meta:
        model = MerchantAccount
        fields = (
            "merchant_id",
            "full_name",
            "about",
            "categories",
            "address",
            "avatar_file_id",
        )


# TODO: fix categories
class ConsumerPaymentRequestResponse(serializers.ModelSerializer):
    merchant = PaymentRequestMerchantDetailsResponse(
        source="account_from.merchant", read_only=True
    )
    status = serializers.CharField(source="status.label", read_only=True)
    payment_request_id = serializers.CharField(source="u_id", read_only=True)

    class Meta:
        model = PaymentRequest
        fields = (
            "payment_request_id",
            "created_at",
            "merchant",
            "amount",
            "currency",
            "status",
        )


class ConsumerBasicInfoResponse(serializers.ModelSerializer):
    first_name = serializers.CharField(
        source="consumer.user.first_name", read_only=True
    )
    last_name = serializers.SerializerMethodField("get_last_name")
    loqal_id = serializers.CharField(source="consumer.username", read_only=True)

    class Meta:
        model = Account
        fields = (
            "first_name",
            "last_name",
            "loqal_id",
        )

    def get_last_name(self, obj):
        last_name = obj.consumer.user.last_name
        if last_name:
            return last_name[0]
        return ""


class PaymentRequestResponse(serializers.ModelSerializer):
    status = serializers.CharField(source="status.label", read_only=True)
    account_to = ConsumerBasicInfoResponse(read_only=True)
    payment_request_id = serializers.CharField(source="u_id", read_only=True)
    payment_id = serializers.CharField(
        source="payment.payment_tracking_id", read_only=True
    )

    class Meta:
        model = PaymentRequest
        fields = (
            "account_to",
            "created_at",
            "amount",
            "currency",
            "status",
            "payment_id",
            "payment_request_id",
        )


class ConsumerResponse(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    loqal_id = serializers.CharField(source="username", read_only=True)

    class Meta:
        model = ConsumerAccount
        fields = (
            "first_name",
            "last_name",
            "loqal_id",
        )


class MerchantTransactionResponse(serializers.ModelSerializer):
    user = ConsumerResponse(source="sender.account.consumer", read_only=True)
    transaction_id = serializers.CharField(
        source="transaction_tracking_id", read_only=True
    )
    status = serializers.CharField(source="status.label", read_only=True)
    payment_qrcode_id = serializers.CharField(
        source="payment_qrcode.qrcode_id", read_only=True
    )
    transaction_type = serializers.CharField(
        source="transaction_type.label", read_only=True
    )

    class Meta:
        model = Transaction
        fields = (
            "id",
            "transaction_id",
            "created_at",
            "user",
            "amount",
            "tip_amount",
            "currency",
            "status",
            "payment_qrcode_id",
            "transaction_type",
        )


class TransactionResponse(serializers.ModelSerializer):
    payment_status = serializers.CharField(
        source="payment.status.label", read_only=True
    )
    transaction_status = serializers.CharField(source="status.label", read_only=True)

    class Meta:
        model = Transaction
        fields = (
            "transaction_tracking_id",
            "created_at",
            "amount",
            "currency",
            "transaction_status",
            "payment_status",
            "is_success",
        )


class PaymentResponse(serializers.ModelSerializer):
    transactions = TransactionResponse(many=True, read_only=True)

    class Meta:
        model = Payment
        fields = (
            "id",
            "created_at",
            "transactions",
        )


class MerchantPaymentResponse(serializers.ModelSerializer):
    transaction = TransactionResponse(read_only=True)

    class Meta:
        model = DirectMerchantPayment
        fields = (
            "id",
            "created_at",
            "transaction",
        )


class RefundPaymentResponse(serializers.ModelSerializer):
    transaction = TransactionResponse(read_only=True)

    class Meta:
        model = Refund
        fields = (
            "id",
            "created_at",
            "transaction",
        )


class DirectMerchantPaymentConsumerResponse(serializers.ModelSerializer):
    amount = serializers.CharField(source="captured_amount", read_only=True)

    class Meta:
        model = Payment
        fields = (
            "created_at",
            "amount",
            "total_tip_amount",
            "payment_tracking_id",
        )


class TransactionHistoryResponse(serializers.ModelSerializer):
    payment_status = serializers.CharField(
        source="payment.status.label", read_only=True
    )
    transaction_id = serializers.CharField(
        source="transaction_tracking_id", read_only=True
    )
    merchant = MerchantDetailsResponse(source="payment.order.merchant", read_only=True)
    merchant_id = serializers.CharField(
        source="payment.order.merchant.u_id", read_only=True
    )
    bank_logo = serializers.SerializerMethodField("get_bank_logo")
    is_credit = serializers.SerializerMethodField("is_credit_transaction")
    order_total_amount = serializers.CharField(
        source="payment.order.total_amount", read_only=True
    )
    order_net_amount = serializers.CharField(
        source="payment.order.total_net_amount", read_only=True
    )
    order_return_amount = serializers.CharField(
        source="payment.order.total_return_amount", read_only=True
    )
    sender_source_type = serializers.ChoiceCharEnumSerializer(read_only=True)
    recipient_source_type = serializers.ChoiceCharEnumSerializer(read_only=True)
    reward_usage = RewardUsageResponse(read_only=True)

    class Meta:
        model = Transaction
        fields = (
            "created_at",
            "amount",
            "currency",
            "payment_status",
            "transaction_id",
            "is_success",
            "merchant",
            "bank_logo",
            "is_credit",
            "merchant_id",
            "order_total_amount",
            "order_net_amount",
            "order_return_amount",
            "sender_source_type",
            "recipient_source_type",
            "reward_usage",
        )

    def get_bank_logo(self, obj):
        self.refund = None
        self.bank_account = None
        self.refund = obj.refund_payment
        if self.refund:
            self.bank_account = obj.recipient_bank_account
        else:
            self.bank_account = obj.sender_bank_account
        if self.bank_account:
            return self.bank_account.bank_logo_base64
        return None

    def is_credit_transaction(self, obj):
        if self.refund:
            return True
        if obj.transaction_type == TransactionType.CREDIT_REWARD_CASHBACK:
            return True
        return False


class CreateTransactionResponse(serializers.ModelSerializer):
    payment_status = serializers.CharField(
        source="payment.status.label", read_only=True
    )
    transaction_id = serializers.CharField(
        source="transaction_tracking_id", read_only=True
    )
    merchant = MerchantDetailsResponse(source="payment.order.merchant", read_only=True)
    merchant_id = serializers.CharField(
        source="payment.order.merchant.u_id", read_only=True
    )
    bank_logo = serializers.SerializerMethodField("get_bank_logo")
    is_credit = serializers.SerializerMethodField("is_credit_transaction")
    discount = TransactionDiscountResponse(source="payment.order", read_only=True)
    sender_source_type = serializers.ChoiceCharEnumSerializer(read_only=True)
    recipient_source_type = serializers.ChoiceCharEnumSerializer(read_only=True)
    reward_usage = RewardUsageResponse(read_only=True)

    class Meta:
        model = Transaction
        fields = (
            "created_at",
            "amount",
            "currency",
            "payment_status",
            "transaction_id",
            "is_success",
            "merchant",
            "bank_logo",
            "is_credit",
            "merchant_id",
            "discount",
            "sender_source_type",
            "recipient_source_type",
            "reward_usage",
        )

    def get_bank_logo(self, obj):
        self.bank_account = None
        self.refund = obj.refund_payment
        if self.refund:
            self.bank_account = obj.recipient_bank_account
        else:
            self.bank_account = obj.sender_bank_account
        if self.bank_account:
            return self.bank_account.bank_logo_base64
        return None

    def is_credit_transaction(self, obj):
        if self.refund:
            return True
        if obj.transaction_type == TransactionType.CREDIT_REWARD_CASHBACK:
            return True
        return False


class BankAcconutResponse(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = (
            "bank_logo_base64",
            "bank_name",
            "account_number_suffix",
        )


class TransactionDetailsResponse(serializers.ModelSerializer):
    payment_status = serializers.CharField(
        source="payment.status.label", read_only=True
    )
    payment_tracking_id = serializers.CharField(
        source="payment.payment_tracking_id", read_only=True
    )
    merchant = MerchantDetailsResponse(source="payment.order.merchant", read_only=True)
    banks_details = serializers.SerializerMethodField("get_bank_details")
    tip_amount = serializers.SerializerMethodField("get_tip_amount")
    is_credit = serializers.SerializerMethodField("is_credit_transaction")
    failure_reason_type_label = serializers.CharField(
        source="failure_reason_type.label", read_only=True
    )
    failure_reason_type_value = serializers.CharField(
        source="failure_reason_type.value", read_only=True
    )
    merchant_rating = serializers.BooleanField(
        source="merchant_rating.give_thanks", read_only=True
    )
    discount = TransactionDiscountResponse(source="payment.order", read_only=True)
    sender_source_type = serializers.ChoiceCharEnumSerializer(read_only=True)
    recipient_source_type = serializers.ChoiceCharEnumSerializer(read_only=True)
    reward_usage = RewardUsageResponse(read_only=True)

    class Meta:
        model = Transaction
        fields = (
            "created_at",
            "amount",
            "currency",
            "payment_status",
            "payment_tracking_id",
            "transaction_tracking_id",
            "is_success",
            "merchant",
            "banks_details",
            "is_credit",
            "tip_amount",
            "is_disputed",
            "failure_reason_type_label",
            "failure_reason_type_value",
            "failure_reason_message",
            "merchant_rating",
            "discount",
            "sender_source_type",
            "recipient_source_type",
            "reward_usage",
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

    def get_tip_amount(self, obj):
        payment = obj.payment
        if payment:
            if payment.payment_process == PaymentProcess.PAYMENT_REQUEST:
                payment_requests = payment.payment_requests
                if not payment_requests.exists():
                    return None
                payment_request = payment_requests.first()
                return payment_request.tip_amount

            if payment.payment_process in [
                PaymentProcess.QRCODE,
                PaymentProcess.DIRECT_APP,
            ]:
                direct_merchant_payments = payment.direct_merchant_payments
                if not direct_merchant_payments.exists():
                    return None
                direct_merchant_payment = direct_merchant_payments.first()
                return direct_merchant_payment.tip_amount
        return Decimal(0.0)


class RecentStoresResponse(serializers.ModelSerializer):
    amount = serializers.CharField(source="payment.captured_amount", read_only=True)
    address = serializers.JSONField(source="merchant.profile.address", read_only=True)
    full_name = serializers.CharField(
        source="merchant.profile.full_name", read_only=True
    )
    categories = MerchantCategoryResponse(
        source="merchant.categories", many=True, read_only=True
    )
    merchant_id = serializers.CharField(source="merchant.u_id", read_only=True)

    class Meta:
        model = Order
        fields = (
            "amount",
            "categories",
            "address",
            "full_name",
            "created_at",
            "updated_at",
            "merchant_id",
        )


class TransactionErrorDetailsResponse(serializers.ModelSerializer):
    payment_status = serializers.CharField(
        source="payment.status.label", read_only=True
    )
    payment_tracking_id = serializers.CharField(
        source="payment.payment_tracking_id", read_only=True
    )
    merchant = MerchantDetailsResponse(source="payment.order.merchant", read_only=True)
    failure_reason_type_label = serializers.CharField(
        source="failure_reason_type.label", read_only=True
    )
    failure_reason_type_value = serializers.CharField(
        source="failure_reason_type.value", read_only=True
    )
    transaction_id = serializers.CharField(
        source="transaction_tracking_id", read_only=True
    )

    class Meta:
        model = Transaction
        fields = (
            "created_at",
            "amount",
            "currency",
            "payment_status",
            "payment_tracking_id",
            "transaction_id",
            "is_success",
            "merchant",
            "is_disputed",
            "failure_reason_type_label",
            "failure_reason_type_value",
            "failure_reason_message",
        )
