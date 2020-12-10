from api import serializers
from apps.account.models import MerchantAccount

__all__ = ("MerchantAccountProfileResponse",)


class MerchantAccountProfileResponse(serializers.ModelSerializer):
    zip_code = serializers.CharField(source="account.zip_code", read_only=True)
    account_status = serializers.CharField(
        source="account_status.label", read_only=True
    )

    class Meta:
        model = MerchantAccount
        fields = (
            "created_at",
            "id",
            "zip_code",
            "company_name",
            "company_email",
            "account_status",
        )
