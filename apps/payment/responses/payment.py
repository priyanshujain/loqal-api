from api import serializers
from apps.account.models import Account, MerchantAccount
from apps.account.responses import MerchantDetailsResponse
from apps.payment.models import PaymentRequest, Transaction

__all__ = (
    "TransactionResponse",
    "PaymentRequestResponse",
    "ConsumerPaymentRequestResponse",
)


class TransactionResponse(serializers.ModelSerializer):
    merchant = MerchantDetailsResponse(
        source="recipient.account.merchantaccount", read_only=True
    )
    uid = serializers.CharField(source="u_id", read_only=True)
    status = serializers.CharField(source="status.label", read_only=True)
    payment_qrcode_id = serializers.CharField(
        source="payment_qrcode.qrcode_id", read_only=True
    )

    class Meta:
        model = Transaction
        fields = (
            "id",
            "uid",
            "created_at",
            "merchant",
            "payment_amount",
            "tip_amount",
            "payment_currency",
            "status",
            "payment_qrcode_id",
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
            "payment_amount",
            "payment_currency",
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
    requested_to = ConsumerBasicInfoResponse(read_only=True)

    class Meta:
        model = PaymentRequest
        fields = (
            "id",
            "requested_to",
            "created_at",
            "payment_amount",
            "payment_currency",
            "status",
        )
