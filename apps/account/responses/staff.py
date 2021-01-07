from api import serializers
from apps.account.models import MerchantAccount


class MerchantAccountProfileResponse(serializers.ModelSerializer):
    zip_code = serializers.CharField(source="account.zip_code", read_only=True)
    account_status = serializers.CharField(
        source="account_status.label", read_only=True
    )
    full_name = serializers.CharField(
        source="merchantprofile.full_name", read_only=True
    )
    uid = serializers.UUIDField(source="u_id", read_only=True)
    account_id = serializers.IntegerField(source="account.id", read_only=True)

    class Meta:
        model = MerchantAccount
        fields = (
            "created_at",
            "id",
            "zip_code",
            "company_email",
            "account_status",
            "uid",
            "full_name",
            "account_id",
        )
