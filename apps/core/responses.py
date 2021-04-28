from api import serializers
from apps.core.models import AppMetaData, MerchantMetaData


class AppMetaDataResponse(serializers.ModelSerializer):
    platform = serializers.ChoiceCharEnumSerializer(read_only=True)
    api_env = serializers.ChoiceCharEnumSerializer(read_only=True)
    primary_banking_verification_provider = (
        serializers.ChoiceCharEnumSerializer(read_only=True)
    )

    class Meta:
        model = AppMetaData
        fields = (
            "min_allowed_version",
            "new_version",
            "platform",
            "store_url",
            "api_env",
            "primary_banking_verification_provider",
        )


class MerchantMetaDataResponse(serializers.ModelSerializer):
    platform = serializers.ChoiceCharEnumSerializer(read_only=True)
    api_env = serializers.ChoiceCharEnumSerializer(read_only=True)
    primary_banking_verification_provider = (
        serializers.ChoiceCharEnumSerializer(read_only=True)
    )

    class Meta:
        model = MerchantMetaData
        fields = (
            "min_allowed_version",
            "new_version",
            "platform",
            "store_url",
            "api_env",
            "primary_banking_verification_provider",
        )
