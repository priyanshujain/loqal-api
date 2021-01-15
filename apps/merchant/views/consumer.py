from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.views import ConsumerAPIView
from apps.account.dbapi import get_merchant_account_by_uid
from apps.merchant.dbapi import get_merchants_by_category
from apps.merchant.responses import (CategoryMerchantListResponse,
                                     MerchantBasicDetailsResponse,
                                     MerchantFullDetailsResponse)
from apps.merchant.services import StoreSearch
from apps.merchant.shortcuts import validate_category

__all__ = (
    "MerchantBasicDetailsAPI",
    "MerchantSearchAPI",
    "ListCategoryMerchantsAPI",
)


class MerchantBasicDetailsAPI(ConsumerAPIView):
    def get(self, request, merchant_id):
        merchant_account = get_merchant_account_by_uid(
            merchant_uid=merchant_id
        )
        if not merchant_account:
            raise ValidationError(
                {"detail": ErrorDetail(_("Invalid merchant."))}
            )
        return self.response(
            MerchantBasicDetailsResponse(merchant_account).data
        )


class MerchantSearchAPI(ConsumerAPIView):
    def get(self, request):
        merchants = StoreSearch(
            data=self.request_data, consumer=request.consumer_account
        ).handle()
        return self.response(merchants)


class ListCategoryMerchantsAPI(ConsumerAPIView):
    def get(self, request):
        category = self.request_data.get("category", None)
        if not category:
            raise ValidationError(
                {"detail": ErrorDetail(_("category is required."))}
            )
        if not validate_category(category=category):
            raise ValidationError(
                {"detail": ErrorDetail(_("category is not valid."))}
            )

        merchants = get_merchants_by_category(category=category)
        return self.response(
            CategoryMerchantListResponse(merchants, many=True).data
        )


class StoreDetailsAPI(ConsumerAPIView):
    def get(self, request, merchant_id):
        merchant_account = get_merchant_account_by_uid(
            merchant_uid=merchant_id
        )
        if not merchant_account:
            raise ValidationError(
                {"detail": ErrorDetail(_("Invalid merchant."))}
            )
        return self.response(
            MerchantFullDetailsResponse(merchant_account).data
        )
