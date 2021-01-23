from api import serializers
from apps.account.models import MerchantAccount
from apps.merchant.models import (BeneficialOwner, ControllerDetails,
                                  ControllerVerificationDocument,
                                  IncorporationDetails,
                                  IncorporationVerificationDocument,
                                  OwnerVerificationDocument)

__all__ = ("OnboardingDataResponse",)


class IncorporationVerificationDocumentResponse(serializers.ModelSerializer):
    document_file_id = serializers.IntegerField(
        source="document_file.id", read_only=True
    )
    status = serializers.ChoiceCharEnumSerializer(read_only=True)
    document_type = serializers.ChoiceCharEnumSerializer(read_only=True)

    class Meta:
        model = IncorporationVerificationDocument
        fields = (
            "all_failure_reasons",
            "failure_reason",
            "document_type",
            "document_file_id",
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
            "document_file_id",
            "status",
        )


class IncorporationDetailsResponse(serializers.ModelSerializer):
    verification_document_status = serializers.CharField(
        source="verification_document_status.label", read_only=True
    )
    business_type = serializers.CharField(
        source="business_type.value", read_only=True
    )
    business_type_label = serializers.CharField(
        source="business_type.label", read_only=True
    )
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
    status = serializers.CharField(source="status.label", read_only=True)
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
