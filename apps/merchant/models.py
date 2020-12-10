from django.utils.translation import gettext as _
from django.db import models
from django.db.models.deletion import DO_NOTHING

from db.models import AbstractBaseModel
from db.postgres.fields import ArrayField
from apps.box.models import BoxFile
from apps.account.models import MerchantAccount
from utils.shortcuts import generate_uuid_hex


class MerchantCategory(AbstractBaseModel):
    """
    # Examples: https://pixelcutlabs.com/blog/google-my-business-categories/
    """

    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True)
    description = models.TextField(blank=True)
    background_image = models.ForeignKey(
        BoxFile, on_delete=models.DO_NOTHING, blank=True, null=True
    )
    background_color = models.CharField(max_length=128, blank=True)

    class Meta:
        db_table = "merchant_category"


class MerchantProfile(AbstractBaseModel):
    merchant = models.OneToOneField(MerchantAccount, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=256)
    about = models.TextField(blank=True)
    category = models.ForeignKey(MerchantCategory, on_delete=DO_NOTHING)
    logo = models.ForeignKey(
        BoxFile, on_delete=models.DO_NOTHING, blank=True, null=True
    )
    address = models.JSONField()
    neighborhood = models.CharField(
        max_length=128,
        blank=True,
        help_text=_(
            "Ex. Navy Yard"
        ),
    )
    website = models.URLField(blank=True)
    facebook_page = models.URLField(blank=True)
    istagram_page = models.URLField(blank=True)
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
        help_text=_(
            "Ex. Smart Casual"
        ),
    )
    dining_styles =  models.CharField(
        max_length=1024,
        blank=True,
        help_text=_(
            "Ex. Casual Dining"
        ),
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


"""
# Onboarding models
"""


class IncorporationDetails(AbstractBaseModel):
    merchant = models.OneToOneField(MerchantAccount, on_delete=models.CASCADE)
    legal_business_name = models.CharField(max_length=512)
    ein_number = models.CharField(max_length=11)
    registered_address = models.JSONField()
    business_type = models.CharField(max_length=32)
    business_classification = models.CharField(max_length=64)
    verification_document_type = models.CharField(max_length=32, blank=True)
    verification_document_file = models.ForeignKey(
        BoxFile, on_delete=models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        db_table = "merchant_onboarding_incorporation_details"


class IncorporationConsent(AbstractBaseModel):
    merchant = models.ForeignKey(MerchantAccount, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    ip_address = models.GenericIPAddressField()
    dwolla_correlation_id = models.CharField(
        max_length=40, default=generate_uuid_hex, editable=False, unique=True
    )

    class Meta:
        db_table = "merchant_onboarding_incorporation_consent"


class IndividualBase(AbstractBaseModel):
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    is_us_citizen = models.BooleanField()
    ssn = models.CharField(max_length=9, blank=True)
    dob = models.DateField()
    address = models.JSONField()
    passport_country = models.CharField(max_length=2, blank=True)
    passport_number = models.CharField(max_length=32)
    verification_document_type = models.CharField(max_length=32, blank=True)
    verification_document_file = models.ForeignKey(
        BoxFile, on_delete=models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        abstract = True


class ControllerDetails(IndividualBase):
    merchant = models.OneToOneField(MerchantAccount, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)

    class Meta:
        db_table = "merchant_onboarding_controller_details"


class BeneficialOwner(IndividualBase):
    merchant = models.ForeignKey(MerchantAccount, on_delete=models.CASCADE)

    class Meta:
        db_table = "merchant_onboarding_beneficial_owner"