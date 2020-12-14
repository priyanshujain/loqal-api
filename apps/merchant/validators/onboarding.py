from django.utils.translation import gettext as _

from api import serializers
from api.exceptions import ErrorDetail, ValidationError
from apps.account.models import MerchantAccount
from apps.merchant.models import (BeneficialOwner, ControllerDetails,
                                  IncorporationDetails)
from apps.merchant.options import BusinessTypes

# from stdnum import ein


__all__ = (
    "IncorporationDetailsValidator",
    "ControllerValidator",
    "BeneficialOwnerValidator",
    "UpdateBeneficialOwnerValidator",
    "RemoveBeneficialOwnerValidator",
    "OnboardingDataValidator",
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
        )
    
    def validate_ein_number(self, ein_number):
        pass


class ControllerValidator(serializers.ModelSerializer):
    dob = serializers.DateField(format="%Y-%m-%d")
    address = serializers.AddressSerializer()

    class Meta:
        model = ControllerDetails
        exclude = ("merchant",)

    # def validate(attr):
    # TODO: Add other validators for the controller


class BeneficialOwnerValidator(serializers.ModelSerializer):
    dob = serializers.DateField(format="%Y-%m-%d")
    address = serializers.AddressSerializer()

    class Meta:
        model = BeneficialOwner
        exclude = ("merchant",)


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
