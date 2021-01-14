from api import serializers
from apps.account.models import MerchantAccount

__all__ = ("MerchantDetailsResponse",)


class MerchantDetailsResponse(serializers.ModelSerializer):
    account_status = serializers.CharField(
        source="account_status.label", read_only=True
    )
    uid = serializers.UUIDField(source="u_id", read_only=True)
    full_name = serializers.CharField(
        source="profile.full_name", read_only=True
    )
    about = serializers.CharField(source="profile.about", read_only=True)
    category = serializers.CharField(source="profile.category", read_only=True)
    sub_category = serializers.CharField(
        source="profile.sub_category", read_only=True
    )
    hero_image = serializers.CharField(
        source="profile.hero_image", read_only=True
    )
    address = serializers.JSONField(source="profile.address", read_only=True)

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
