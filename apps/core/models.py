from enum import unique

from django.db import models
from django.utils.translation import deactivate
from django.utils.translation import gettext as _

from apps.banking.options import VerificationProvider
from db.models import BaseModel
from db.models.fields import ChoiceCharEnumField

from .options import APIEnvironmentTypes, PlatformTypes


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


class MerchantMetaData(BaseModel):
    """
    This represents merchant app metadata
    """

    platform = ChoiceCharEnumField(enum_type=PlatformTypes, max_length=8)
    primary_banking_verification_provider = ChoiceCharEnumField(
        enum_type=VerificationProvider,
        default=VerificationProvider.PLAID,
        max_length=32,
    )
    min_allowed_version = models.CharField(default="0.0.1", max_length=128)
    new_version = models.CharField(default="0.0.1", max_length=128)
    store_url = models.URLField(max_length=256, blank=True)
    api_env = ChoiceCharEnumField(
        enum_type=APIEnvironmentTypes,
        default=APIEnvironmentTypes.DEVELOPMENT,
        max_length=32,
    )

    class Meta:
        db_table = "merchant_metadata"
