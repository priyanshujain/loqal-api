from api import serializers
from apps.core.models import AppMetaData


class AppMetaDataResponse(serializers.ModelSerializer):
    platform = serializers.ChoiceCharEnumSerializer(read_only=True)
    api_env = serializers.ChoiceCharEnumSerializer(read_only=True)

    class Meta:
        model = AppMetaData
        fields = (
            "min_allowed_version",
            "new_version",
            "platform",
            "store_url",
            "api_env",
        )
