from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.merchant.dbapi import (get_all_merchants, get_merchants_by_category,
                                 merchant_search_by_keyword)
from apps.merchant.responses import StoreSearchResponse
from apps.merchant.shortcuts import validate_category
from apps.merchant.validators import StoreSearchValidator

__all__ = ("StoreSearch",)


class StoreSearch(ServiceBase):
    def __init__(self, consumer, data):
        self.data = data
        self.consummer = consumer

    def handle(self):
        data = self._validate_data()
        category = data.get("category")
        merchants = get_all_merchants()
        if category:
            if not validate_category(category):
                raise ValidationError(
                    {
                        "detail": ErrorDetail(
                            _("category paramter is not valid.")
                        )
                    }
                )

            merchants = get_merchants_by_category(
                merchant_qs=merchants, category=category
            )

        keyword = data.get("keyword")
        if keyword:
            merchants = merchant_search_by_keyword(merchants, keyword)

        latitude = data.get("latitude")
        longitude = data.get("longitude")

        # Show first 20 results
        merchants = merchants[:20]

        merchants_response = []
        for merchant in merchants:
            merchant_res = StoreSearchResponse(merchant).data
            if longitude and latitude:
                merchant_res["distance"] = merchant.profile.distance(
                    latitude, longitude
                )
            merchants_response.append(merchant_res)

        return sorted(merchants_response, key=lambda t: t["distance"])

    def _validate_data(self):
        data = run_validator(StoreSearchValidator, self.data)
        return data
