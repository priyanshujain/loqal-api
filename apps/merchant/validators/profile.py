from django.utils.translation import gettext as _

from api import serializers
from api.exceptions import ErrorDetail, ValidationError
from apps.box.dbapi import get_boxfile
from apps.merchant import models
from apps.merchant.models import (CodesAndProtocols, MerchantCategory,
                                  MerchantOperationHours, MerchantProfile,
                                  ServiceAvailability, StoreImage)
from apps.merchant.models.profile import MerchantCategory
from apps.merchant.shortcuts import (validate_profile_image_type,
                                     validate_subcategory)

__all__ = (
    "MerchantProfileValidator",
    "MerchantOperationHoursValidator",
    "CodesAndProtocolsValidator",
    "ServiceAvailabilityValidator",
    "StoreSearchValidator",
    "StoreImageValidator",
)


class MerchantCategoryValidator(serializers.ModelSerializer):
    is_primary = serializers.BooleanField(default=False)

    class Meta:
        model = MerchantCategory
        fields = ("category", "sub_categories", "is_primary")

    def validate(self, attrs):
        attrs = super().validate(attrs)
        category = attrs["category"]
        sub_categories = attrs["sub_categories"]

        for sub_category in sub_categories:
            if not validate_subcategory(
                category=category, sub_category=sub_category
            ):
                raise ValidationError(
                    {
                        "detail": ErrorDetail(
                            _(f"Invalid category {category}/ {sub_category}.")
                        )
                    }
                )
        return attrs


class MerchantProfileValidator(serializers.ModelSerializer):
    categories = serializers.ListField(required=True, allow_empty=False)
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

    def _validate_file(self, boxfile_id, field_key):
        boxfile = get_boxfile(boxfile_id=boxfile_id)
        if not boxfile:
            raise ValidationError(
                {field_key: [ErrorDetail(_("Given file is not valid."))]}
            )
        if boxfile.in_use:
            raise ValidationError(
                {
                    field_key: [
                        ErrorDetail(_("Given file is already being used."))
                    ]
                }
            )
        if not validate_profile_image_type(boxfile.content_type):
            raise ValidationError(
                {field_key: [ErrorDetail(_("Given file type is not valid."))]}
            )
        if boxfile.document_type != "merchant_profile":
            raise ValidationError(
                {
                    field_key: [
                        ErrorDetail(
                            _("Document type should be merchant_profile.")
                        )
                    ]
                }
            )

    def validate(self, attrs):
        attrs = super().validate(attrs)
        categories = attrs["categories"]
        updated_categories = []
        for category in categories:
            s = MerchantCategoryValidator(data=category)
            s.is_valid(raise_exception=True)
            updated_categories.append(s.data)
        attrs["categories"] = updated_categories

        avatar_file_id = attrs.get("avatar_file_id")
        if avatar_file_id:
            self._validate_file(avatar_file_id, "avatar_file_id")
        background_file_id = attrs.get("background_file_id")
        if background_file_id:
            self._validate_file(background_file_id, "background_file_id")

        return attrs


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
            "mask_required",
            "sanitizer_provided",
            "outdoor_seating",
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


class StoreSearchValidator(serializers.ValidationSerializer):
    category = serializers.CharField(required=False)
    keyword = serializers.CharField(required=False)
    latitude = serializers.FloatField(required=False)
    longitude = serializers.FloatField(required=False)


class StoreImageValidator(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = StoreImage
        fields = (
            "image",
            "alt",
        )

    def validate(self, data):
        if data.get("image") is None:
            raise ValidationError(
                {"detail": ErrorDetail(_("No store image were provided"))}
            )
        return data
