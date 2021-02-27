import math

from django.db import models
from django.db.models.deletion import DO_NOTHING
from django.utils.translation import gettext as _
from versatileimagefield.fields import PPOIField, VersatileImageField

from apps.account.models import MerchantAccount
from apps.box.models import BoxFile
from apps.merchant.constants import MERCHANT_CATEGORIES
from apps.merchant.options import BusinessDayType, CleaningFrequencyType
from apps.merchant.shortcuts import coordinate_distance
from db.models import AbstractBaseModel
from db.models.fields import ChoiceCharEnumField
from db.postgres.fields import ArrayField

__all__ = (
    "MerchantProfile",
    "MerchantOperationHours",
    "CodesAndProtocols",
    "ServiceAvailability",
    "MerchantCategory",
    "StoreImage",
)


class MerchantCategory(AbstractBaseModel):
    merchant = models.ForeignKey(
        MerchantAccount, on_delete=models.CASCADE, related_name="categories"
    )
    category = models.CharField(max_length=64)
    is_primary = models.BooleanField(default=False)
    sub_categories = ArrayField(models.CharField(max_length=255))

    class Meta:
        db_table = "merchant_category"
        unique_together = (
            "merchant",
            "category",
        )


class StoreImage(AbstractBaseModel):
    merchant = models.ForeignKey(
        MerchantAccount, on_delete=models.CASCADE, related_name="images"
    )
    image = VersatileImageField(
        upload_to="store-images/", ppoi_field="ppoi", blank=False
    )
    ppoi = PPOIField()
    alt = models.CharField(max_length=128, blank=True)

    class Meta:
        db_table = "store_photo"


class MerchantProfile(AbstractBaseModel):
    merchant = models.OneToOneField(
        MerchantAccount, on_delete=models.CASCADE, related_name="profile"
    )
    full_name = models.CharField(max_length=256)
    about = models.TextField(blank=True)
    background_file = models.ForeignKey(
        BoxFile,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="merchant_background_file",
    )
    avatar_file = models.ForeignKey(
        BoxFile,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="merchant_avatar_file",
    )
    address = models.JSONField()
    website = models.URLField(blank=True)
    facebook_page = models.URLField(blank=True)
    instagram_page = models.URLField(blank=True)
    youtube_page = models.URLField(blank=True)
    yelp_page = models.URLField(blank=True)
    phone_number = models.CharField(max_length=15)
    parking_details = models.TextField(
        blank=True,
        help_text=_(
            "Where can cusotmers park their vehicles"
            "Ex. The Yards Lot Q; Limited street parking"
        ),
    )
    dress_code = models.CharField(
        max_length=1024,
        blank=True,
        help_text=_("Ex. Smart Casual"),
    )
    dining_styles = models.CharField(
        max_length=1024,
        blank=True,
        help_text=_("Ex. Casual Dining"),
    )
    cuisines = ArrayField(
        models.CharField(max_length=64), default=list, blank=True
    )
    amenities = ArrayField(
        models.CharField(max_length=64), default=list, blank=True
    )
    additional_details = models.TextField(blank=True)

    class Meta:
        db_table = "merchant_profile"

    def distance(self, latitude, longitude):
        if not self.address:
            return 0
        address_lat = self.address.get("latitude")
        address_lon = self.address.get("longitude")

        if not (address_lon and address_lat):
            return None
        return math.fabs(
            coordinate_distance(latitude, longitude, address_lat, address_lon)
        )


class MerchantOperationHours(AbstractBaseModel):
    merchant = models.ForeignKey(MerchantAccount, on_delete=models.CASCADE)
    day = ChoiceCharEnumField(max_length=3, enum_type=BusinessDayType)
    open_time = models.TimeField(null=True)
    close_time = models.TimeField(null=True)
    is_closed = models.BooleanField(default=False)

    class Meta:
        db_table = "merchant_operation_hours"
        unique_together = (
            "merchant",
            "day",
        )


class CodesAndProtocols(AbstractBaseModel):
    merchant = models.OneToOneField(MerchantAccount, on_delete=models.CASCADE)
    mask_required = models.BooleanField(default=False)
    sanitizer_provided = models.BooleanField(default=False)
    outdoor_seating = models.BooleanField(default=False)
    cleaning_frequency = ChoiceCharEnumField(
        max_length=32,
        enum_type=CleaningFrequencyType,
        default=CleaningFrequencyType.NOT_PROVIDED,
    )
    last_cleaned_at = models.DateTimeField(null=True)

    class Meta:
        db_table = "merchant_codes_and_protocols"


class ServiceAvailability(AbstractBaseModel):
    # Add parking/ valet to the list
    merchant = models.OneToOneField(MerchantAccount, on_delete=models.CASCADE)
    curbside_pickup = models.BooleanField(default=False)
    delivery = models.BooleanField(default=False)
    takeout = models.BooleanField(default=False)
    sitting_dining = models.BooleanField(default=False)

    class Meta:
        db_table = "merchant_service_availability"
