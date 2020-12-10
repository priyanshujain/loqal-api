from django.db import models

from apps.box.models import BoxFile
from db.models import AbstractBaseModel

__all__ = ("MerchantCategory",)


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
