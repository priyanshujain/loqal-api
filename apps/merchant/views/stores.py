from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.views import ConsumerAPIView
from apps.merchant.responses import  CategoryMerchantListResponse
from apps.merchant.dbapi import get_merchants_by_category
from apps.merchant.shortcuts import validate_category


__all__ = (
    "ListCategoryMerchantsAPI",
)

class ListCategoryMerchantsAPI(ConsumerAPIView):
    def get(self, request):
        category = self.request_data.get("category", None)
        if not category:
            raise ValidationError({
                "detail": ErrorDetail(_("category is required."))
            })
        if not validate_category(category=category):
            raise ValidationError({
                "detail": ErrorDetail(_("category is not valid."))
            }) 
        
        merchants = get_merchants_by_category(category=category)
        return self.response(CategoryMerchantListResponse(merchants, many=True).data)
        