from api import serializers
from apps.account.models import MerchantAccount


class MerchantAccountProfileResponse(serializers.ModelSerializer):
    zip_code = serializers.CharField(
        source="profile.address.zip_code", read_only=True
    )
    account_status = serializers.ChoiceCharEnumSerializer(
        source="account.dwolla_customer_status", read_only=True
    )
    account_verification_status = serializers.ChoiceCharEnumSerializer(
        source="account.dwolla_customer_verification_status", read_only=True
    )
    full_name = serializers.CharField(
        source="profile.full_name", read_only=True
    )
    merchant_id = serializers.CharField(source="u_id", read_only=True)
    account_id = serializers.IntegerField(source="account.id", read_only=True)

    class Meta:
        model = MerchantAccount
        fields = (
            "created_at",
            "id",
            "zip_code",
            "company_email",
            "full_name",
            "account_id",
            "merchant_id",
            "is_active",
            "account_status",
            "account_verification_status",
        )
