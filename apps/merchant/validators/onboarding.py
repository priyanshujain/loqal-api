from django.utils.translation import gettext as _

from api import serializers
from api.exceptions import ErrorDetail, ValidationError
from apps.account.models import MerchantAccount
from apps.merchant.models import (
    BeneficialOwner,
    ControllerDetails,
    IncorporationDetails,
)
from apps.merchant.options import (
    BusinessTypes,
    IndividualDocumentType,
    BusinessDocumentType,
)
from apps.box.dbapi import get_boxfile

from stdnum.us import ein


__all__ = (
    "IncorporationDetailsValidator",
    "ControllerValidator",
    "BeneficialOwnerValidator",
    "UpdateBeneficialOwnerValidator",
    "RemoveBeneficialOwnerValidator",
    "OnboardingDataValidator",
    "BeneficialOwnerDocumentValidator",
    "ControllerDocumentValidator",
    "BusinessDocumentValidator",
)


class IncorporationDetailsValidator(serializers.ModelSerializer):
    registered_address = serializers.AddressSerializer()
    business_type = serializers.ChoiceField(choices=BusinessTypes.choices)

    class Meta:
        model = IncorporationDetails
        exclude = (
            "merchant",
            "verification_document_type",
            "verification_document_file",
            "verification_document_status",
            "verification_document_required",
        )

    def validate(self, attrs):
        attrs = super().validate(attrs)
        business_type = attrs.get("business_type")
        ein_number = attrs.get("ein_number")

        if business_type != BusinessTypes.SOLE_PROPRIETORSHIP.value and not ein_number:
            raise ValidationError(
                {
                    "ein_number": [
                        ErrorDetail(
                            _(
                                "EIN number is required for business types other than sole proprietor."
                            )
                        )
                    ]
                }
            )

        if not ein.is_valid(ein_number):
            raise ValidationError(
                {"ein_number": [ErrorDetail(_("EIN number is not in currect format."))]}
            )
        attrs["ein_number"] = ein.format(ein_number)
        return attrs


class ControllerValidator(serializers.ModelSerializer):
    dob = serializers.DateField(format="%Y-%m-%d")
    address = serializers.AddressSerializer()

    class Meta:
        model = ControllerDetails
        exclude = (
            "merchant",
            "verification_document_type",
            "verification_document_file",
            "verification_document_status",
            "verification_document_required",
        )

    # def validate(attrs):
    # TODO: Add other validators for the controller


class BeneficialOwnerValidator(serializers.ModelSerializer):
    dob = serializers.DateField(format="%Y-%m-%d")
    address = serializers.AddressSerializer()

    class Meta:
        model = BeneficialOwner
        exclude = (
            "merchant",
            "verification_document_type",
            "verification_document_file",
            "verification_document_status",
        )


class UpdateBeneficialOwnerValidator(BeneficialOwnerValidator):
    id = serializers.IntegerField()


class RemoveBeneficialOwnerValidator(serializers.ValidationSerializer):
    id = serializers.IntegerField()


class OnboardingDataValidator(serializers.ModelSerializer):
    incorporation_details = IncorporationDetailsValidator()
    controller_details = ControllerValidator()

    class Meta:
        model = MerchantAccount
        fields = (
            "incorporation_details",
            "controller_details",
        )

    def validate(self, attrs):
        attrs = super().validate(attrs)
        incorporation_details = attrs.get("incorporation_details")
        controller_details = attrs.get("controller_details")
        business_type = incorporation_details["business_type"]
        if (
            business_type != BusinessTypes.SOLE_PROPRIETORSHIP.value
            and not controller_details["title"]
        ):
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _(
                            "Controller title is required if you are a llp or a corporation."
                        )
                    )
                }
            )
        return attrs


class DocumentFileValidator(serializers.ValidationSerializer):
    verification_document_file_id = serializers.IntegerField()
    verification_document_type = serializers.CharField()

    def validate(self, attrs):
        attrs = super().validate(attrs)
        verification_document_file_id = attrs.get("verification_document_file_id")
        verification_document_type = attrs.get("verification_document_type")
        boxfile = get_boxfile(boxfile_id=verification_document_file_id)
        if not boxfile:
            raise ValidationError(
                {
                    "verification_document_file_id": [
                        ErrorDetail(_("Given file is not valid."))
                    ]
                }
            )
        if boxfile.in_use:
            raise ValidationError(
                {
                    "verification_document_file_id": [
                        ErrorDetail(_("Given file is already being used."))
                    ]
                }
            )
        if boxfile.document_type != verification_document_type:
            raise ValidationError(
                {
                    "verification_document_type": [
                        ErrorDetail(_("Document type does not match."))
                    ]
                }
            )
        return attrs
            


class BeneficialOwnerDocumentValidator(DocumentFileValidator):
    beneficial_owner_id = serializers.IntegerField()
    verification_document_type = serializers.ChoiceField(
        choices=IndividualDocumentType.choices
    )


class ControllerDocumentValidator(DocumentFileValidator):
    verification_document_type = serializers.ChoiceField(
        choices=IndividualDocumentType.choices
    )


class BusinessDocumentValidator(DocumentFileValidator):
    verification_document_type = serializers.ChoiceField(
        choices=BusinessDocumentType.choices
    )
