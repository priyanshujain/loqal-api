from enum import unique

from django.db import models
from django.utils.translation import gettext as _

from db.models import BaseModel
from db.models.fields import ChoiceCharEnumField

from .options import APIEnvironmentTypes, PlatformTypes
from db.models.fields import ChoiceCharEnumField
from .options import VerificationProvider


class AppMetaData(BaseModel):
    """
    This represents consumer app metadata 
    """

    min_allowed_version = models.CharField(max_length=128)
    new_version = models.CharField(max_length=128)
    platform = ChoiceCharEnumField(enum_type=PlatformTypes, max_length=8)
    store_url = models.URLField(max_length=256)
    api_env = ChoiceCharEnumField(enum_type=APIEnvironmentTypes, max_length=32)
    primary_banking_verification_provider = ChoiceCharEnumField(
        enum_type=VerificationProvider,
        default=VerificationProvider.PLAID,
        max_length=32,
    )

    class Meta:
        db_table = "app_metadata"



class MerchantWebMetaData(BaseModel):
    """
    This represents merchant web app metadata
    """

    primary_banking_verification_provider = ChoiceCharEnumField(
        enum_type=VerificationProvider,
        default=VerificationProvider.PLAID,
        max_length=32,
    )

    class Meta:
        db_table = "merchant_web_app_metadata"
