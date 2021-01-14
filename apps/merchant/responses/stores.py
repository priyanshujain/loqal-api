from api import serializers
from apps.account.models import MerchantAccount
from apps.merchant.models import (CodesAndProtocols, MerchantOperationHours,
                                  MerchantProfile, ServiceAvailability)

__all__ = ("CategoryMerchantListResponse", "StoreSearchResponse")


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
    profile = MerchantBasicProfileResponse(source="profile", read_only=True)
    hours = MerchantOperatingHoursResponse(
        source="merchantoperationhours", read_only=True
    )
    codes_and_protocols = MerchantCodesProtocolsResponse(
        source="codesandprotocols", read_only=True
    )
    services = MerchantServicesResponse(
        source="serviceavailability", read_only=True
    )

    class Meta:
        model = MerchantAccount
        fields = (
            "profile",
            "hours",
            "codes_and_protocols",
            "services",
        )


class StoreSearchResponse(serializers.ModelSerializer):
    uid = serializers.UUIDField(source="u_id", read_only=True)
    full_name = serializers.CharField(
        source="profile.full_name", read_only=True
    )
    about = serializers.CharField(source="profile.about", read_only=True)
    address = serializers.JSONField(source="profile.address", read_only=True)
    codes_and_protocols = MerchantCodesProtocolsResponse(
        source="codesandprotocols", read_only=True
    )
    services = MerchantServicesResponse(
        source="serviceavailability", read_only=True
    )
    hours = MerchantOperatingHoursResponse(
        source="merchantoperationhours", read_only=True
    )

    class Meta:
        model = MerchantAccount
        fields = (
            "uid",
            "full_name",
            "about",
            "address",
            "codes_and_protocols",
            "services",
            "hours",
        )
