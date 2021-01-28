from types import ClassMethodDescriptorType

from api import serializers
from apps.account.models import Account, MerchantAccount
from apps.box.models import BoxFile
from apps.merchant.models import (BeneficialOwner, ControllerDetails,
                                  ControllerVerificationDocument,
                                  IncorporationDetails,
                                  IncorporationVerificationDocument,
                                  OwnerVerificationDocument)

__all__ = (
    "OnboardingDataResponse",
    "IncorporationVerificationDocumentResponse",
    "OwnerVerificationDocumentResponse",
    "ControllerVerificationDocumentResponse",
    "OnboardingStatusResponse",
)


class BoxFileResponse(serializers.ModelSerializer):
    class Meta:
        model = BoxFile
        fields = ("id", "file_name")


class IncorporationVerificationDocumentResponse(serializers.ModelSerializer):
    document_file = BoxFileResponse(read_only=True)
    status = serializers.ChoiceCharEnumSerializer(read_only=True)
    document_type = serializers.ChoiceCharEnumSerializer(read_only=True)
    document_id = serializers.CharField(source="u_id")

    class Meta:
        model = IncorporationVerificationDocument
        fields = (
            "all_failure_reasons",
            "failure_reason",
            "document_type",
            "document_file",
            "document_id",
            "status",
        )


class OwnerVerificationDocumentResponse(
    IncorporationVerificationDocumentResponse
):
    class Meta:
        model = OwnerVerificationDocument
        fields = (
            "all_failure_reasons",
            "failure_reason",
            "document_type",
            "document_file_id",
            "status",
            "document_id",
        )


class ControllerVerificationDocumentResponse(
    IncorporationVerificationDocumentResponse
):
    class Meta:
        model = ControllerVerificationDocument
        fields = (
            "all_failure_reasons",
            "failure_reason",
            "document_type",
            "document_file",
            "status",
            "document_id",
        )


class IncorporationDetailsResponse(serializers.ModelSerializer):
    business_type = serializers.ChoiceCharEnumSerializer(read_only=True)
    documents = IncorporationVerificationDocumentResponse(
        many=True, read_only=True
    )

    class Meta:
        model = IncorporationDetails
        fields = "__all__"


class ControllerDetailsResponse(serializers.ModelSerializer):
    documents = ControllerVerificationDocumentResponse(
        many=True, read_only=True
    )

    class Meta:
        model = ControllerDetails
        fields = "__all__"


class BeneficialOwnerResponse(serializers.ModelSerializer):
    status = serializers.ChoiceCharEnumSerializer(read_only=True)
    documents = OwnerVerificationDocumentResponse(many=True, read_only=True)

    class Meta:
        model = BeneficialOwner
        fields = "__all__"


class OnboardingDataResponse(serializers.ModelSerializer):
    account_status = serializers.ChoiceCharEnumSerializer(
        source="account.dwolla_customer_status", read_only=True
    )
    account_verification_status = serializers.ChoiceCharEnumSerializer(
        source="account.dwolla_customer_verification_status", read_only=True
    )
    incorporation_details = IncorporationDetailsResponse(read_only=True)
    controller_details = ControllerDetailsResponse(read_only=True)
    beneficial_owners = BeneficialOwnerResponse(
        many=True,
        read_only=True,
    )

    class Meta:
        model = MerchantAccount
        fields = (
            "account_status",
            "account_verification_status",
            "incorporation_details",
            "controller_details",
            "beneficial_owners",
        )


class OnboardingStatusResponse(serializers.ModelSerializer):
    account_status = serializers.ChoiceCharEnumSerializer(
        source="dwolla_customer_status", read_only=True
    )
    account_verification_status = serializers.ChoiceCharEnumSerializer(
        source="dwolla_customer_verification_status", read_only=True
    )

    class Meta:
        model = Account
        fields = (
            "account_status",
            "account_verification_status",
        )
