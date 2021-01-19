from decimal import Decimal

from api import serializers
from apps.account.models import Account, ConsumerAccount, MerchantAccount
from apps.banking.models import BankAccount
from apps.merchant.models import MerchantCategory
from apps.order.models import Order
from apps.payment.models import (DirectMerchantPayment, Payment,
                                 PaymentRequest, Refund, Transaction, transaction)
from apps.payment.options import PaymentProcess

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
)


class MerchantCategoryResponse(serializers.ModelSerializer):
    class Meta:
        model = MerchantCategory
        fields = (
            "category",
            "sub_categories",
            "is_primary",
        )


class PaymentRequestMerchantDetailsResponse(serializers.ModelSerializer):
    merchant_id = serializers.CharField(source="u_id", read_only=True)
    full_name = serializers.CharField(
        source="profile.full_name", read_only=True
    )
    about = serializers.CharField(source="profile.about", read_only=True)
    categories = MerchantCategoryResponse(many=True, read_only=True)
    hero_image = serializers.CharField(
        source="profile.hero_image", read_only=True
    )
    address = serializers.JSONField(source="profile.address", read_only=True)

    class Meta:
        model = MerchantAccount
        fields = (
            "merchant_id",
            "full_name",
            "about",
            "categories",
            "hero_image",
            "address",
        )


# TODO: fix categories
class ConsumerPaymentRequestResponse(serializers.ModelSerializer):
    merchant = PaymentRequestMerchantDetailsResponse(
        source="account.merchantaccount", read_only=True
    )
    status = serializers.CharField(source="status.label", read_only=True)

    class Meta:
        model = PaymentRequest
        fields = (
            "id",
            "created_at",
            "merchant",
            "amount",
            "currency",
            "status",
        )


class ConsumerBasicInfoResponse(serializers.ModelSerializer):
    first_name = serializers.CharField(
        source="consumeraccount.user.first_name", read_only=True
    )
    last_name = serializers.CharField(
        source="consumeraccount.user.last_name", read_only=True
    )

    class Meta:
        model = Account
        fields = (
            "first_name",
            "last_name",
        )


class PaymentRequestResponse(serializers.ModelSerializer):
    status = serializers.CharField(source="status.label", read_only=True)
    account_to = ConsumerBasicInfoResponse(read_only=True)

    class Meta:
        model = PaymentRequest
        fields = (
            "id",
            "account_to",
            "created_at",
            "amount",
            "currency",
            "status",
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


class MerchantTransactionResponse(serializers.ModelSerializer):
    user = ConsumerResponse(
        source="sender.account.consumeraccount", read_only=True
    )
    transaction_id = serializers.CharField(source="transaction_tracking_id", read_only=True)
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
    transaction_status = serializers.CharField(
        source="status.label", read_only=True
    )

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


class MerchantDetailsResponse(serializers.ModelSerializer):
    full_name = serializers.CharField(
        source="profile.full_name", read_only=True
    )
    categories = MerchantCategoryResponse(many=True, read_only=True)
    address = serializers.JSONField(source="profile.address", read_only=True)

    class Meta:
        model = MerchantAccount
        fields = ("full_name", "categories", "address")


class TransactionHistoryResponse(serializers.ModelSerializer):
    payment_status = serializers.CharField(
        source="payment.status.label", read_only=True
    )
    transaction_id = serializers.CharField(
        source="transaction_tracking_id", read_only=True
    )
    merchant = MerchantDetailsResponse(
        source="payment.order.merchant", read_only=True
    )
    merchant_id = serializers.CharField(
        source="payment.order.merchant.u_id", read_only=True
    )
    bank_logo = serializers.SerializerMethodField("get_bank_logo")
    is_credit = serializers.SerializerMethodField("is_credit_transaction")

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
        )

    def get_bank_logo(self, obj):
        self.refund = None
        try:
            self.refund = obj.refund
            return obj.recipient_bank_account.bank_logo_base64
        except Refund.DoesNotExist:
            return obj.sender_bank_account.bank_logo_base64

    def is_credit_transaction(self, obj):
        if self.refund:
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
    merchant = MerchantDetailsResponse(
        source="payment.order.merchant", read_only=True
    )
    banks_details = serializers.SerializerMethodField("get_bank_details")
    tip_amount = serializers.SerializerMethodField("get_tip_amount")
    is_credit = serializers.SerializerMethodField("is_credit_transaction")
    failure_reason_type_label = serializers.CharField(
        source="failure_reason_type.label", read_only=True
    )
    failure_reason_type_value = serializers.CharField(
        source="failure_reason_type.value", read_only=True
    )

    class Meta:
        model = Transaction
        fields = (
            "created_at",
            "amount",
            "currency",
            "payment_status",
            "payment_tracking_id",
            "is_success",
            "merchant",
            "banks_details",
            "is_credit",
            "tip_amount",
            "is_disputed",
            "failure_reason_type_label",
            "failure_reason_type_value",
            "failure_reason_message",
        )

    def get_bank_details(self, obj):
        self.refund = None
        bank_account = None
        try:
            self.refund = obj.refund
            bank_account = obj.recipient_bank_account
        except Refund.DoesNotExist:
            bank_account = obj.sender_bank_account
        return BankAcconutResponse(bank_account).data

    def is_credit_transaction(self, obj):
        if self.refund:
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
    amount = serializers.CharField(
        source="payment.captured_amount", read_only=True
    )
    address = serializers.JSONField(
        source="merchant.profile.address", read_only=True
    )
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
            "merchant_id",
        )


class TransactionErrorDetailsResponse(serializers.ModelSerializer):
    payment_status = serializers.CharField(
        source="payment.status.label", read_only=True
    )
    payment_tracking_id = serializers.CharField(
        source="payment.payment_tracking_id", read_only=True
    )
    merchant = MerchantDetailsResponse(
        source="payment.order.merchant", read_only=True
    )
    failure_reason_type_label = serializers.CharField(
        source="failure_reason_type.label", read_only=True
    )
    failure_reason_type_value = serializers.CharField(
        source="failure_reason_type.value", read_only=True
    )
    transaction_id = serializers.CharField(source="transaction_tracking_id", read_only=True)

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
