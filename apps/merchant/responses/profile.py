from api import serializers
from apps.merchant.models import MerchantProfile

__all__ = ("MerchantProfileResponse",)


class MerchantProfileResponse(serializers.ModelSerializer):
    class Meta:
        model = MerchantProfile
        exclude = ("merchant",)
