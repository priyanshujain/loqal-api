from api import serializers
from apps.account.models import MerchantAccount
from apps.merchant.models import (BeneficialOwner, ControllerDetails,
                                  IncorporationDetails)

__all__ = ("OnboardingDataResponse",)


class IncorporationDetailsResponse(serializers.ModelSerializer):
    verification_document_status = serializers.CharField(source="verification_document_status.label", read_only=True)

    class Meta:
        model = IncorporationDetails
        fields = "__all__"


class ControllerDetailsResponse(serializers.ModelSerializer):
    verification_document_status = serializers.CharField(source="verification_document_status.label", read_only=True)

    class Meta:
        model = ControllerDetails
        fields = "__all__"


class BeneficialOwnerResponse(serializers.ModelSerializer):
    status = serializers.CharField(source="status.label", read_only=True)
    verification_document_status = serializers.CharField(source="verification_document_status.label", read_only=True)

    class Meta:
        model = BeneficialOwner
        fields = "__all__"


class OnboardingDataResponse(serializers.ModelSerializer):
    account_status = serializers.CharField(
        source="account_status.label", read_only=True
    )
    incorporation_details = IncorporationDetailsResponse(
        source="incorporationdetails", read_only=True
    )
    controller_details = ControllerDetailsResponse(
        source="controllerdetails", read_only=True
    )
    beneficial_owners = BeneficialOwnerResponse(
        source="beneficialowner_set",
        many=True,
        read_only=True,
    )

    class Meta:
        model = MerchantAccount
        fields = (
            "account_status",
            "incorporation_details",
            "controller_details",
            "beneficial_owners",
        )
