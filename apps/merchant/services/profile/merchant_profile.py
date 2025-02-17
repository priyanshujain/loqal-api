import operator
from functools import reduce

from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.merchant.dbapi import (create_merchant_category,
                                 get_merchant_category_by_merchant,
                                 get_merchant_category_by_name,
                                 update_merchant_category,
                                 update_merchant_profile)
from apps.merchant.validators import MerchantProfileValidator

__all__ = ("UpdateMerchantProfile",)


class UpdateMerchantProfile(ServiceBase):
    def __init__(self, merchant, data):
        self.data = data
        self.merchant = merchant
        self.merchant_id = merchant.id

    def handle(self):
        data = self._validate_data()
        categories = data["categories"]
        del data["categories"]
        self._update_merchant_profile(data)
        self._update_categories(categories)

    def _validate_data(self):
        data = run_validator(MerchantProfileValidator, self.data)
        return data

    def _update_merchant_profile(self, data):
        update_merchant_profile(merchant_id=self.merchant_id, **data)

    def _update_categories(self, categories):
        if not any([category["is_primary"] for category in categories]):
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _("Please mark aleast one category as primary.")
                    )
                }
            )

        category_names = [category["category"] for category in categories]
        category_names = list(set(category_names))

        for category_name in category_names:
            sub_categories = [
                category["sub_categories"]
                for category in categories
                if category["category"] == category_name
            ]

            is_primary = all(
                [
                    category["is_primary"]
                    for category in categories
                    if category["category"] == category_name
                ]
            )
            sub_categories = reduce(operator.concat, sub_categories)
            sub_categories = list(set(sub_categories))
            category = get_merchant_category_by_name(
                merchant_id=self.merchant_id, category=category_name
            )
            if not category:
                create_merchant_category(
                    merchant_id=self.merchant_id,
                    category=category_name,
                    sub_categories=sub_categories,
                    is_primary=is_primary,
                )
            else:
                update_merchant_category(
                    merchant_id=self.merchant_id,
                    category=category_name,
                    sub_categories=sub_categories,
                    is_primary=is_primary,
                )

        # Delete merchant category if merchant category is not in updated categories
        exisiting_categories = get_merchant_category_by_merchant(
            merchant_id=self.merchant_id
        )
        for merchant_category in exisiting_categories:
            if not merchant_category.category in category_names:
                merchant_category.delete()
