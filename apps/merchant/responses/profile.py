from apps.merchant.models import MerchantProfile
from api import serializers

__all__ = (
    "MerchantProfileResponse",
)


class MerchantProfileResponse(serializers.ModelSerializer):
    class Meta:
        model = MerchantProfile
        exclude = ("merchant",)