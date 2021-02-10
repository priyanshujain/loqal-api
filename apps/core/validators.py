from api import serializers
from apps.core.models import AppMetaData

from .options import APIEnvironmentTypes, PlatformTypes

__all__ = ("AppMetaDataValidator",)


class AppMetaDataValidator(serializers.ModelSerializer):
    platform = serializers.ChoiceField(choices=PlatformTypes.choices)
    api_env = serializers.ChoiceField(choices=APIEnvironmentTypes.choices)

    class Meta:
        model = AppMetaData
        fields = (
            "platform",
            "api_env",
            "min_allowed_version",
            "new_version",
            "store_url",
        )
