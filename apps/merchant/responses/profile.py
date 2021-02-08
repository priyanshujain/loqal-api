from api import serializers
from apps.account.models import MerchantAccount
from apps.merchant.constants import categories
from apps.merchant.models import (CodesAndProtocols, MerchantCategory,
                                  MerchantOperationHours, MerchantProfile,
                                  ServiceAvailability)

__all__ = (
    "MerchantProfileResponse",
    "MerchantOperationHoursResponse",
    "CodesAndProtocolsResponse",
    "ServiceAvailabilityResponse",
)


class MerchantCategoryResponse(serializers.ModelSerializer):
    class Meta:
        model = MerchantCategory
        fields = ("category", "sub_categories", "is_primary")


class MerchantProfileResponse(serializers.ModelSerializer):
    avatar_file_id = serializers.IntegerField(
        source="avatar_file.id", read_only=True
    )
    background_file_id = serializers.IntegerField(
        source="background_file.id", read_only=True
    )
    categories = MerchantCategoryResponse(
        source="merchant.categories", many=True, read_only=True
    )

    class Meta:
        model = MerchantProfile
        exclude = ("merchant", "avatar_file", "background_file")


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
            "mask_required",
            "sanitizer_provided",
            "outdoor_seating",
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
