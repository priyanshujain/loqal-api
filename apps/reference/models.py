from django.db import models

from db.models import BaseModel
from db.models.base import BaseModel


class RegionState(BaseModel):
    name = models.CharField(max_length=256)
    region_code = models.CharField(max_length=5)
    country_code = models.CharField(max_length=2)

    class Meta:
        unique_together = (
            "region_code",
            "country_code",
        )
        db_table = "region_state"


class Country(BaseModel):
    name = models.CharField(max_length=256)
    iso_code = models.CharField(max_length=2, unique=True)

    class Meta:
        db_table = "country"


class City(BaseModel):
    name = models.CharField(max_length=512)
    country_code = models.CharField(max_length=2)

    class Meta:
        unique_together = (
            "name",
            "country_code",
        )
        db_table = "city"


class ZipCode(BaseModel):
    code = models.CharField(max_length=5, unique=True)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=2)
    county = models.CharField(max_length=64)

    class Meta:
        db_table = "zip_code"
