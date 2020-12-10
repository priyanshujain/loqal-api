from api import serializers
from apps.box.validators import BoxFileIdSerializer
from apps.merchant.models import IncorporationDetails, ControllerDetails, BeneficialOwner
from apps.merchant.options import BusinessTypes


__all__ = (
    "IncorporationDetailsValidator",
    "ControllerValidator",
    'BeneficialOwnerValidator',
    'UpdateBeneficialOwnerValidator',
    'RemoveBeneficialOwnerValidator',    
)


class IncorporationDetailsValidator(serializers.ModelSerializer):
    registered_address = serializers.AddressSerializer()
    business_type = serializers.ChoiceField(choices=BusinessTypes.choices)

    class Meta:
        model = IncorporationDetails
        exclude = ("merchant", "verification_document_type", "verification_document_file",)


class ControllerValidator(serializers.ModelSerializer):
    dob = serializers.DateField(format="%Y-%m-%d")
    address = serializers.AddressSerializer()

    class Meta:
        model = ControllerDetails
        exclude = (
            "merchant",
        )


class BeneficialOwnerValidator(serializers.ModelSerializer):
    dob = serializers.DateField(format="%Y-%m-%d")
    address = serializers.AddressSerializer()

    class Meta:
        model = BeneficialOwner
        exclude = (
            "merchant",
        )


class UpdateBeneficialOwnerValidator(BeneficialOwnerValidator):
    id = serializers.IntegerField()


class RemoveBeneficialOwnerValidator(serializers.ValidationSerializer):
    id = serializers.IntegerField()
