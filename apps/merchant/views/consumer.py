from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.views import ConsumerAPIView
from apps.account.dbapi import get_merchant_account_by_uid
from apps.merchant.dbapi import get_merchant_qs_by_category
from apps.merchant.responses import (CategoryMerchantListResponse,
                                     ListStoreImageResponse,
                                     MerchantBasicDetailsResponse,
                                     MerchantFullDetailsResponse)
from apps.merchant.services import StoreSearch
from apps.merchant.shortcuts import validate_category
from apps.merchant.tasks import check_if_merchant_account_ready
from apps.reward.dbapi.merchant import get_current_loyalty_program
from apps.reward.responses import LoyaltyProgramResponse

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
        data = MerchantBasicDetailsResponse(merchant_account).data
        data["is_merchant_account_ready"] = check_if_merchant_account_ready(
            merchant=merchant_account
        )
        return self.response(data)


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

        merchants = get_merchant_qs_by_category(category=category)
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
        data = MerchantFullDetailsResponse(merchant_account).data
        data["is_merchant_account_ready"] = check_if_merchant_account_ready(
            merchant=merchant_account
        )
        images = merchant_account.images
        data["images"] = ListStoreImageResponse(images, many=True).data
        loyalty_program = get_current_loyalty_program(
            merchant_id=merchant_account.id
        )
        if loyalty_program:
            data["loyalty_program"] = LoyaltyProgramResponse(
                loyalty_program
            ).data
        return self.response(data)
