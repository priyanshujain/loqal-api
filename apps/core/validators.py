from api import serializers
from apps.banking.options import VerificationProvider
from apps.core.models import AppMetaData, MerchantMetaData

from .options import APIEnvironmentTypes, PlatformTypes

__all__ = (
    "AppMetaDataValidator",
    "MerchantMetaDataValidator",
)


class AppMetaDataValidator(serializers.ModelSerializer):
    platform = serializers.ChoiceField(choices=PlatformTypes.choices)
    api_env = serializers.ChoiceField(choices=APIEnvironmentTypes.choices)
    primary_banking_verification_provider = serializers.ChoiceField(
        choices=VerificationProvider.choices
    )

    class Meta:
        model = AppMetaData
        fields = (
            "platform",
            "api_env",
            "min_allowed_version",
            "new_version",
            "store_url",
            "primary_banking_verification_provider",
        )


class MerchantMetaDataValidator(serializers.ModelSerializer):
    platform = serializers.ChoiceField(choices=PlatformTypes.choices)
    api_env = serializers.ChoiceField(choices=APIEnvironmentTypes.choices)
    primary_banking_verification_provider = serializers.ChoiceField(
        choices=VerificationProvider.choices
    )

    class Meta:
        model = MerchantMetaData
        fields = (
            "platform",
            "api_env",
            "min_allowed_version",
            "new_version",
            "store_url",
            "primary_banking_verification_provider",
        )
