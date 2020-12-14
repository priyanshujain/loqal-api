from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.provider.lib.actions import ProviderAPIActionBase
from apps.reference.dbapi import (get_country, get_region_states,
                                  partial_search_city)
from apps.reference.validators import (CitySearchSerializer,
                                       RegionStateSerializer)

__all__ = (
    "CitySearch",
    "RegionStateList",
)


class CitySearch(ServiceBase):
    def __init__(self, data):
        self.data = data

    def _validate_data(self):
        run_validator(CitySearchSerializer, self.data)
        country_code = self.data["country"]
        if not get_country(country_code=country_code):
            raise ValidationError(
                {"country": [ErrorDetail(_("country is not valid."))]}
            )
        return True

    def handle(self):
        self._validate_data()
        country = self.data["country"]
        city = self.data["city"]
        return partial_search_city(
            country_code=country, partial_city_name=city
        )


class RegionStateList(ServiceBase):
    def __init__(self, data):
        self.data = data

    def _validate_data(self):
        run_validator(RegionStateSerializer, self.data)
        country_code = self.data["country"]
        if not get_country(country_code=country_code):
            raise ValidationError(
                {"country": [ErrorDetail(_("country is not valid."))]}
            )
        return True

    def handle(self):
        self._validate_data()
        country = self.data["country"]
        region_state_qs = get_region_states(country_code=country)
        return [
            {"name": region_obj.name, "region_code": region_obj.region_code}
            for region_obj in region_state_qs
        ]
