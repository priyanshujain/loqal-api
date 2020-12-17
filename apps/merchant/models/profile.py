from django.db import models
from django.db.models.deletion import DO_NOTHING
from django.utils.translation import gettext as _

from apps.account.models import MerchantAccount
from apps.box.models import BoxFile
from apps.merchant.constants import MERCHANT_CATEGORIES
from db.models import AbstractBaseModel
from db.postgres.fields import ArrayField

__all__ = (
    "MerchantProfile",
    "MerchantOperationHours",
    "CodesAndProtocols",
    "ServiceAvailability",
)


class MerchantProfile(AbstractBaseModel):
    merchant = models.OneToOneField(MerchantAccount, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=256)
    about = models.TextField(blank=True)
    category = models.CharField(
        max_length=64, default=MERCHANT_CATEGORIES[0]["category_slug"]
    )
    sub_category = models.CharField(
        max_length=64,
        default=MERCHANT_CATEGORIES[0]["subcategories"][0]["slug"],
    )
    hero_image = models.ForeignKey(
        BoxFile, on_delete=models.DO_NOTHING, blank=True, null=True
    )
    address = models.JSONField()
    neighborhood = models.CharField(
        max_length=128,
        blank=True,
        help_text=_("Ex. Navy Yard"),
    )
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


class MerchantOperationHours(AbstractBaseModel):
    merchant = models.ForeignKey(MerchantAccount, on_delete=models.CASCADE)
    day = models.CharField(max_length=32)
    open_time = models.TimeField()
    close_time = models.TimeField()
    is_closed = models.BooleanField(default=False)


class CodesAndProtocols(AbstractBaseModel):
    merchant = models.OneToOneField(MerchantAccount, on_delete=models.CASCADE)
    contactless_payments = models.BooleanField(default=True)
    mask_required = models.BooleanField(default=True)
    sanitizer_provided = models.BooleanField(default=True)
    ourdoor_seating = models.BooleanField(default=True)
    last_cleaned_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "merchant_codes_and_protocols"


class ServiceAvailability(AbstractBaseModel):
    merchant = models.OneToOneField(MerchantAccount, on_delete=models.CASCADE)
    curbside_pickup = models.BooleanField(default=True)
    delivery = models.BooleanField(default=True)
    takeout = models.BooleanField(default=True)
    sitting_dining = models.BooleanField(default=True)

    class Meta:
        db_table = "merchant_service_availability"
