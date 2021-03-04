from api import serializers
from apps.account.models import MerchantAccount
from apps.merchant.dbapi import profile
from apps.merchant.models import (CodesAndProtocols, MerchantCategory,
                                  MerchantOperationHours, MerchantProfile,
                                  ServiceAvailability)

__all__ = (
    "MerchantBasicDetailsResponse",
    "CategoryMerchantListResponse",
    "StoreSearchResponse",
    "MerchantFullDetailsResponse",
    "MerchantBasicDetailsResponse",
)


class MerchantCategoryResponse(serializers.ModelSerializer):
    class Meta:
        model = MerchantCategory
        fields = (
            "category",
            "sub_categories",
            "is_primary",
        )


class MerchantBasicDetailsResponse(serializers.ModelSerializer):
    account_status = serializers.ChoiceCharEnumSerializer(
        source="account.dwolla_customer_status", read_only=True
    )
    account_verification_status = serializers.ChoiceCharEnumSerializer(
        source="account.dwolla_customer_verification_status", read_only=True
    )
    merchant_id = serializers.CharField(source="u_id", read_only=True)
    full_name = serializers.CharField(
        source="profile.full_name", read_only=True
    )
    about = serializers.CharField(source="profile.about", read_only=True)
    categories = MerchantCategoryResponse(many=True, read_only=True)
    avatar_file_id = serializers.CharField(
        source="profile.avatar_file.id", read_only=True
    )
    address = serializers.JSONField(source="profile.address", read_only=True)
    is_loqal_enabled = serializers.BooleanField(
        source="account", read_only=True
    )

    class Meta:
        model = MerchantAccount
        fields = (
            "account_status",
            "account_verification_status",
            "merchant_id",
            "full_name",
            "about",
            "categories",
            "avatar_file_id",
            "address",
            "is_loqal_enabled",
        )


class MerchantBasicProfileResponse(serializers.ModelSerializer):
    class Meta:
        model = MerchantProfile
        fields = (
            "full_name",
            "address",
        )


class MerchantBasicDetailsResponse(serializers.ModelSerializer):
    full_name = serializers.CharField(
        source="profile.full_name", read_only=True
    )
    categories = MerchantCategoryResponse(many=True, read_only=True)
    address = serializers.JSONField(source="profile.address", read_only=True)

    class Meta:
        model = MerchantAccount
        fields = ("full_name", "categories", "address")


class MerchantOperatingHoursResponse(serializers.ModelSerializer):
    day = serializers.CharField(source="day.value", read_only=True)

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


class MerchantProfileResponse(serializers.ModelSerializer):
    background_file_id = serializers.IntegerField(required=False)
    avatar_file_id = serializers.IntegerField(required=False)

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
            "background_file",
            "avatar_file",
        )


class MerchantFullDetailsResponse(serializers.ModelSerializer):
    merchant_id = serializers.CharField(source="u_id", read_only=True)
    full_name = serializers.CharField(
        source="profile.full_name", read_only=True
    )
    profile = MerchantProfileResponse(read_only=True)
    categories = MerchantCategoryResponse(many=True, read_only=True)
    hours = MerchantOperatingHoursResponse(
        source="merchantoperationhours_set", many=True, read_only=True
    )
    codes_and_protocols = MerchantCodesProtocolsResponse(
        source="codesandprotocols", read_only=True
    )
    services = MerchantServicesResponse(
        source="serviceavailability", read_only=True
    )
    address = serializers.JSONField(source="profile.address", read_only=True)
    is_loqal_enabled = serializers.BooleanField(
        source="account", read_only=True
    )

    class Meta:
        model = MerchantAccount
        fields = (
            "merchant_id",
            "full_name",
            "profile",
            "categories",
            "address",
            "codes_and_protocols",
            "services",
            "hours",
            "is_loqal_enabled",
        )


class CategoryMerchantListResponse(serializers.ModelSerializer):
    profile = MerchantBasicProfileResponse(read_only=True)
    hours = MerchantOperatingHoursResponse(
        source="merchantoperationhours_set", many=True, read_only=True
    )
    codes_and_protocols = MerchantCodesProtocolsResponse(
        source="codesandprotocols", read_only=True
    )
    services = MerchantServicesResponse(
        source="serviceavailability", read_only=True
    )
    merchant_id = serializers.CharField(source="u_id", read_only=True)
    categories = MerchantCategoryResponse(many=True, read_only=True)
    is_loqal_enabled = serializers.BooleanField(
        source="account", read_only=True
    )

    class Meta:
        model = MerchantAccount
        fields = (
            "merchant_id",
            "profile",
            "hours",
            "codes_and_protocols",
            "services",
            "categories",
            "is_loqal_enabled",
        )


class StoreSearchResponse(serializers.ModelSerializer):
    full_name = serializers.CharField(
        source="profile.full_name", read_only=True
    )
    categories = MerchantCategoryResponse(many=True, read_only=True)
    about = serializers.CharField(source="profile.about", read_only=True)
    address = serializers.JSONField(source="profile.address", read_only=True)
    codes_and_protocols = MerchantCodesProtocolsResponse(
        source="codesandprotocols", read_only=True
    )
    services = MerchantServicesResponse(
        source="serviceavailability", read_only=True
    )
    hours = MerchantOperatingHoursResponse(
        source="merchantoperationhours_set", many=True, read_only=True
    )
    merchant_id = serializers.CharField(source="u_id", read_only=True)
    is_loqal_enabled = serializers.BooleanField(
        source="account", read_only=True
    )

    class Meta:
        model = MerchantAccount
        fields = (
            "full_name",
            "about",
            "address",
            "codes_and_protocols",
            "services",
            "hours",
            "categories",
            "merchant_id",
            "is_loqal_enabled",
        )
