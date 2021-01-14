from api import serializers
from apps.merchant.models import (CodesAndProtocols, MerchantOperationHours,
                                  MerchantProfile, ServiceAvailability)

__all__ = (
    "MerchantProfileValidator",
    "MerchantOperationHoursValidator",
    "CodesAndProtocolsValidator",
    "ServiceAvailabilityValidator",
)


class MerchantProfileValidator(serializers.ModelSerializer):
    class Meta:
        model = MerchantProfile
        exclude = (
            "merchant",
            "id",
            "created_at",
            "updated_at",
            "deleted_at",
            "deleted",
            "created_by",
            "updated_by",
            "deleted_by",
        )


class MerchantOperationHoursValidator(serializers.ModelSerializer):
    class Meta:
        model = MerchantOperationHours
        fields = (
            "day",
            "open_time",
            "close_time",
            "is_closed",
        )


class CodesAndProtocolsValidator(serializers.ModelSerializer):
    class Meta:
        model = CodesAndProtocols
        fields = (
            "contactless_payments",
            "mask_required",
            "sanitizer_provided",
            "ourdoor_seating",
            "cleaning_frequency",
            "last_cleaned_at",
        )


class ServiceAvailabilityValidator(serializers.ModelSerializer):
    curbside_pickup = serializers.BooleanField()
    delivery = serializers.BooleanField()
    takeout = serializers.BooleanField()
    sitting_dining = serializers.BooleanField()

    class Meta:
        model = ServiceAvailability
        fields = (
            "curbside_pickup",
            "delivery",
            "takeout",
            "sitting_dining",
        )
