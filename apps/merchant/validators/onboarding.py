from django.utils.translation import gettext as _
from rest_framework import request
from stdnum.us import ein
from stdnum.us import ssn as _ssn

from api import serializers
from api.exceptions import ErrorDetail, ValidationError
from apps.account.models import MerchantAccount
from apps.box.dbapi import get_boxfile
from apps.merchant.models import (BeneficialOwner, ControllerDetails,
                                  IncorporationDetails)
from apps.merchant.options import (BusinessDocumentType, BusinessTypes,
                                   IndividualDocumentType)

__all__ = (
    "IncorporationDetailsValidator",
    "ControllerValidator",
    "BeneficialOwnerValidator",
    "UpdateBeneficialOwnerValidator",
    "RemoveBeneficialOwnerValidator",
    "BeneficialOwnerDocumentValidator",
    "ControllerDocumentValidator",
    "BusinessDocumentValidator",
)


class IncorporationDetailsValidator(serializers.ModelSerializer):
    registered_address = serializers.AddressSerializer()
    business_type = serializers.ChoiceField(choices=BusinessTypes.choices)

    class Meta:
        model = IncorporationDetails
        exclude = ("merchant",)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        business_type = attrs.get("business_type")
        ein_number = attrs.get("ein_number")

        if (
            business_type != BusinessTypes.SOLE_PROPRIETORSHIP.value
            and not ein_number
        ):
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

        if (
            business_type != BusinessTypes.SOLE_PROPRIETORSHIP.value
            and not ein.is_valid(ein_number)
        ):
            raise ValidationError(
                {
                    "ein_number": [
                        ErrorDetail(_("EIN number is not in correct format."))
                    ]
                }
            )
        if ein_number:
            attrs["ein_number"] = ein.format(ein_number)
        return attrs


class IndividualValidator(serializers.ValidationSerializer):
    dob = serializers.DateField(format="%Y-%m-%d")
    address = serializers.AddressSerializer()
    is_us_citizen = serializers.BooleanField()
    ssn_number = serializers.CharField(required=False)
    passport_country = serializers.CharField(max_length=2, required=False)
    passport_number = serializers.CharField(required=False)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        is_us_citizen = attrs.get("is_us_citizen")
        ssn = attrs.get("ssn")
        passport_country = attrs.get("passport_country")
        passport_number = attrs.get("passport_number")

        if is_us_citizen and not ssn:
            raise ValidationError(
                {"ssn": [ErrorDetail(_("SSN is required for US citizens."))]}
            )
        if ssn and not _ssn.is_valid(ssn):
            raise ValidationError(
                {"ssn": [ErrorDetail(_("SSN is not in correct format."))]}
            )

        if not ssn:
            if not (passport_country and passport_country):
                raise ValidationError(
                    {
                        "detail": ErrorDetail(
                            _("Atleast one of passport or SSN is required.")
                        )
                    }
                )
            if not passport_country:
                raise ValidationError(
                    {
                        "passport_country": [
                            ErrorDetail(
                                _(
                                    "If SSN is not provided passport country is required."
                                )
                            )
                        ]
                    }
                )
            if not passport_number:
                raise ValidationError(
                    {
                        "passport_number": [
                            ErrorDetail(
                                _(
                                    "If SSN is not provided passport number is required."
                                )
                            )
                        ]
                    }
                )
        if ssn:
            attrs["ssn"] = _ssn.format(ssn)
        return attrs


class ControllerValidator(IndividualValidator, serializers.ModelSerializer):
    class Meta:
        model = ControllerDetails
        exclude = ("merchant",)


class BeneficialOwnerValidator(
    IndividualValidator, serializers.ModelSerializer
):
    class Meta:
        model = BeneficialOwner
        exclude = ("merchant",)


class UpdateBeneficialOwnerValidator(BeneficialOwnerValidator):
    id = serializers.IntegerField()


class RemoveBeneficialOwnerValidator(serializers.ValidationSerializer):
    id = serializers.IntegerField()


class DocumentFileValidator(serializers.ValidationSerializer):
    document_file_id = serializers.IntegerField()
    document_type = serializers.CharField()
    document_id = serializers.UUIDField(required=False)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        document_file_id = attrs.get("document_file_id")
        document_type = attrs.get("document_type")
        boxfile = get_boxfile(boxfile_id=document_file_id)
        if not boxfile:
            raise ValidationError(
                {
                    "document_file_id": [
                        ErrorDetail(_("Given file is not valid."))
                    ]
                }
            )
        if boxfile.in_use:
            raise ValidationError(
                {
                    "document_file_id": [
                        ErrorDetail(_("Given file is already being used."))
                    ]
                }
            )
        if boxfile.document_type != document_type:
            raise ValidationError(
                {
                    "document_type": [
                        ErrorDetail(_("Document type does not match."))
                    ]
                }
            )
        return attrs


class BeneficialOwnerDocumentValidator(DocumentFileValidator):
    beneficial_owner_id = serializers.IntegerField()
    document_type = serializers.ChoiceField(
        choices=IndividualDocumentType.choices
    )


class ControllerDocumentValidator(DocumentFileValidator):
    document_type = serializers.ChoiceField(
        choices=IndividualDocumentType.choices
    )


class BusinessDocumentValidator(DocumentFileValidator):
    document_type = serializers.ChoiceField(
        choices=BusinessDocumentType.choices
    )
