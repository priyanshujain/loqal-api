from apps.payment.options import PaymentProcess
from api import serializers
from apps.account.models import Account, ConsumerAccount, MerchantAccount
from apps.payment.models import DirectMerchantPayment, Payment, PaymentRequest, Refund, Transaction

__all__ = (
    "TransactionResponse",
    "PaymentRequestResponse",
    "ConsumerPaymentRequestResponse",
    "MerchantTransactionResponse",
    "PaymentResponse",
    "MerchantPaymentResponse",
    "RefundPaymentResponse",
    "TransactionHistoryResponse",
)


class PaymentRequestMerchantDetailsResponse(serializers.ModelSerializer):
    uid = serializers.UUIDField(source="u_id", read_only=True)
    full_name = serializers.CharField(
        source="merchantprofile.full_name", read_only=True
    )
    about = serializers.CharField(
        source="merchantprofile.about", read_only=True
    )
    category = serializers.CharField(
        source="merchantprofile.category", read_only=True
    )
    sub_category = serializers.CharField(
        source="merchantprofile.sub_category", read_only=True
    )
    hero_image = serializers.CharField(
        source="merchantprofile.hero_image", read_only=True
    )
    address = serializers.JSONField(
        source="merchantprofile.address", read_only=True
    )

    class Meta:
        model = MerchantAccount
        fields = (
            "uid",
            "full_name",
            "about",
            "category",
            "sub_category",
            "hero_image",
            "address",
        )


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
    uid = serializers.CharField(source="u_id", read_only=True)
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
            "uid",
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
    payment_status = serializers.CharField(source="payment.status.label", read_only=True)
    transaction_status = serializers.CharField(source="status.label", read_only=True)

    class Meta:
        model = Transaction
        fields = (
            "tracking_number",
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
        source="merchantprofile.full_name", read_only=True
    )
    category = serializers.CharField(
        source="merchantprofile.category", read_only=True
    )
    sub_category = serializers.CharField(
        source="merchantprofile.sub_category", read_only=True
    )
    address = serializers.JSONField(
        source="merchantprofile.address", read_only=True
    )

    class Meta:
        model = MerchantAccount
        fields = (
            "full_name",
            "category",
            "sub_category",
            "address"
        )



class TransactionHistoryResponse(serializers.ModelSerializer):
    payment_status = serializers.CharField(source="payment.status.label", read_only=True)
    merchant = MerchantDetailsResponse(source="payment.order.merchant", read_only=True)
    bank_logo = serializers.SerializerMethodField("get_bank_logo")
    is_credit = serializers.SerializerMethodField("is_credit_transaction")
    
    class Meta:
        model = Transaction
        fields = (
            "created_at",
            "amount",
            "currency",
            "payment_status",
            "is_success",
            "merchant",
            "bank_logo",
            "is_credit"
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