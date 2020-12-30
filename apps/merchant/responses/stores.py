from api import serializers
from apps.merchant.models import (
    MerchantProfile,
    MerchantOperationHours,
    CodesAndProtocols,
    ServiceAvailability,
)
from apps.account.models import MerchantAccount


__all__ = ("CategoryMerchantListResponse",)


class MerchantBasicProfileResponse(serializers.ModelSerializer):
    class Meta:
        model = MerchantProfile
        fields = (
            "category",
            "sub_category",
            "full_name",
        )


class MerchantOperatingHoursResponse(serializers.ModelSerializer):
    class Meta:
        model = MerchantOperationHours
        fields = (
            "day",
            "open_time",
            "close_time",
            "is_closed",
        )


class MerchantCodesProtocolsResponse(serializers.ModelSerializer):
    class Meta:
        model = CodesAndProtocols
        fields = (
            "contactless_payments",
            "mask_required",
            "sanitizer_provided",
            "outdoor_seating",
            "last_cleaned_at",
        )


class MerchantServicesResponse(serializers.ModelSerializer):
    class Meta:
        model = ServiceAvailability
        fields = (
            "curbside_pickup",
            "delivery",
            "takeout",
            "sitting_dining",
        )


class CategoryMerchantListResponse(serializers.ModelSerializer):
    profile = MerchantBasicProfileResponse(source="merchantprofile", read_only=True)
    hours = MerchantOperatingHoursResponse(
        source="merchantoperationhours", read_only=True
    )
    codes_and_protocols = MerchantCodesProtocolsResponse(
        source="codesandprotocols", read_only=True
    )
    services = MerchantServicesResponse(source="serviceavailability", read_only=True)

    class Meta:
        model = MerchantAccount
        fields = (
            "profile",
            "hours",
            "codes_and_protocols",
            "services",
        )