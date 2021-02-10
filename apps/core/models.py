from enum import unique

from django.db import models
from django.utils.translation import gettext as _

from db.models import BaseModel
from db.models.fields import ChoiceCharEnumField

from .options import APIEnvironmentTypes, PlatformTypes


class AppMetaData(BaseModel):
    """
    This represents user device for push notification
    """

    min_allowed_version = models.CharField(max_length=128)
    new_version = models.CharField(max_length=128)
    platform = ChoiceCharEnumField(enum_type=PlatformTypes, max_length=8)
    store_url = models.URLField(max_length=256)
    api_env = ChoiceCharEnumField(enum_type=APIEnvironmentTypes, max_length=32)

    class Meta:
        db_table = "app_metadata"
