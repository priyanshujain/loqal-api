from django.utils.translation import gettext as _
from django.db import models

from db.models import AbstractBaseModel
from apps.box.models import BoxFile
from apps.account.models import MerchantAccount
from utils.shortcuts import generate_uuid_hex

__all__ = (
    'IncorporationConsent',
    'IncorporationDetails',
    'ControllerDetails',
    "BeneficialOwner",
)

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