from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _

from apps.account.models import MerchantAccount
from db.models import AbstractBaseModel
from db.models.fields import ChoiceCharEnumField


class Product(AbstractBaseModel):
    name = models.CharField(max_length=250)

    class Meta:
        db_table = "product"
