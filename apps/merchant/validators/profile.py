from api import serializers
from apps.merchant.models import MerchantProfile

__all__ = ("MerchantProfileValidator",)


class MerchantProfileValidator(serializers.ModelSerializer):
    class Meta:
        model = MerchantProfile
        exclude = (
            "merchant",
            "id",
            "created_at",
            "updated_at",
            "deleted_at",
            "deleted",
            "created_by",
            "updated_by",
            "deleted_by",
        )
