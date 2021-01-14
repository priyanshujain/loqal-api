from api import serializers
from apps.account.models import MerchantAccount
from apps.merchant.models import (CodesAndProtocols, MerchantOperationHours,
                                  MerchantProfile, ServiceAvailability)

__all__ = (
    "MerchantProfileResponse",
    "MerchantOperationHoursResponse",
    "CodesAndProtocolsResponse",
    "ServiceAvailabilityResponse",
)


class MerchantProfileResponse(serializers.ModelSerializer):
    class Meta:
        model = MerchantProfile
        exclude = ("merchant",)


class MerchantOperationHoursResponse(serializers.ModelSerializer):
    day = serializers.CharField(source="day.value", read_only=True)

    class Meta:
        model = MerchantOperationHours
        fields = (
            "day",
            "open_time",
            "close_time",
            "is_closed",
        )


class CodesAndProtocolsResponse(serializers.ModelSerializer):
    cleaning_frequency = serializers.CharField(
        source="cleaning_frequency.value", read_only=True
    )

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


class ServiceAvailabilityResponse(serializers.ModelSerializer):
    class Meta:
        model = ServiceAvailability
        fields = (
            "curbside_pickup",
            "delivery",
            "takeout",
            "sitting_dining",
        )
