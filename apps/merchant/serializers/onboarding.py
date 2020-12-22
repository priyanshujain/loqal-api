from api import serializers
from apps.account.models import MerchantAccount
from apps.merchant.models import (BeneficialOwner, ControllerDetails,
                                  IncorporationDetails)

__all__ = ("OnboardingDataSerializer",)


class IncorporationDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncorporationDetails
        fields = "__all__"


class ControllerDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ControllerDetails
        fields = "__all__"


class BeneficialOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeneficialOwner
        fields = "__all__"


class OnboardingDataSerializer(serializers.ModelSerializer):
    incorporation_details = IncorporationDetailsSerializer(
        source="incorporationdetails", read_only=True
    )
    controller_details = ControllerDetailsSerializer(
        source="controllerdetails", read_only=True
    )
    beneficial_owners = BeneficialOwnerSerializer(
        source="beneficialowner_set", many=True, read_only=True
    )

    class Meta:
        model = MerchantAccount
        fields = (
            "incorporation_details",
            "controller_details",
            "beneficial_owners",
        )
