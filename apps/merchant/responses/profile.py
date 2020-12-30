from api import serializers
from apps.merchant.models import MerchantProfile
from apps.account.models import MerchantAccount

__all__ = ("MerchantProfileResponse",)


class MerchantProfileResponse(serializers.ModelSerializer):
    class Meta:
        model = MerchantProfile
        exclude = ("merchant",)


