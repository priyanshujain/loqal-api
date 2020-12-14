from apps.reference.models import ZipCode
from api import serializers

__all__ = (
    "ZipCodeResponse",
)

class ZipCodeResponse(serializers.ModelSerializer):
    class Meta:
        model = ZipCode
        fields = ("code", "city", "state", "county",)