from api import serializers
from apps.reference.models import ZipCode

__all__ = ("ZipCodeResponse",)


class ZipCodeResponse(serializers.ModelSerializer):
    class Meta:
        model = ZipCode
        fields = (
            "code",
            "city",
            "state",
            "county",
        )
