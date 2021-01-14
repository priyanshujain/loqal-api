from api import serializers
from apps.account.models import MerchantAccount
from apps.merchant.models import MerchantCategory

__all__ = (
    "MerchantAccountProfileResponse",
    "MerchantDetailsResponse",
)


class MerchantAccountProfileResponse(serializers.ModelSerializer):
    zip_code = serializers.CharField(source="account.zip_code", read_only=True)
    account_status = serializers.CharField(
        source="account_status.label", read_only=True
    )
    full_name = serializers.CharField(
        source="profile.full_name", read_only=True
    )
    uid = serializers.UUIDField(source="u_id", read_only=True)

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
        )


class MerchantCategoryResponse(serializers.ModelSerializer):
    class Meta:
        model = MerchantCategory
        fields = (
            "category",
            "sub_categories",
        )


class MerchantDetailsResponse(serializers.ModelSerializer):
    uid = serializers.CharField(source="u_id", read_only=True)
    full_name = serializers.CharField(
        source="profile.full_name", read_only=True
    )
    categories = MerchantCategoryResponse(many=True, read_only=True)

    class Meta:
        model = MerchantAccount
        fields = (
            "uid",
            "full_name",
            "categories",
        )


class MerchantSearchResponse(serializers.ModelSerializer):
    uid = serializers.CharField(source="u_id", read_only=True)
    full_name = serializers.CharField(
        source="profile.full_name", read_only=True
    )
    category = serializers.CharField(source="profile.category", read_only=True)
    sub_category = serializers.CharField(
        source="profile.sub_category", read_only=True
    )

    class Meta:
        model = MerchantAccount
        fields = (
            "uid",
            "full_name",
            "category",
            "sub_category",
        )
