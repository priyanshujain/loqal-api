from api import serializers
from apps.account.models import MerchantAccount
from apps.merchant import models
from apps.merchant.models import AccountMember
from apps.payment.models import PaymentQrCode

__all__ = (
    "QrCodeResponse",
    "MerchantQrCodeResponse",
    "QrCodeMerchantDetailsResponse",
)


class QrCodeResponse(serializers.ModelSerializer):
    class Meta:
        model = PaymentQrCode
        fields = (
            "qrcode_id",
            "is_expired",
            "currency",
        )


class CashierDetailsResponse(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)

    class Meta:
        model = AccountMember
        fields = ("first_name", "last_name",)

class MerchantQrCodeResponse(serializers.ModelSerializer):
    merchant_uid = serializers.CharField(
        source="merchant.u_id", read_only=True
    )
    merchant_id = serializers.IntegerField(
        source="merchant.id", read_only=True
    )
    cashier_id = serializers.IntegerField(source="cashier.id", read_only=True)
    cashier = CashierDetailsResponse(read_only=True)


    class Meta:
        model = PaymentQrCode
        fields = (
            "qrcode_id",
            "is_expired",
            "currency",
            "merchant_uid",
            "merchant_id",
            "cashier_id",
            "cashier",
            "updated_at",
            "created_at",
        )


class QrCodeMerchantDetailsResponse(serializers.ModelSerializer):
    account_status = serializers.CharField(
        source="account_status.label", read_only=True
    )
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
            "account_status",
            "uid",
            "full_name",
            "about",
            "category",
            "sub_category",
            "hero_image",
            "address",
        )
