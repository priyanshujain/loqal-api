from api.views import APIView, MerchantAPIView
from apps.merchant.services import BusinessClassifications
from apps.merchant.constants import MERCHANT_CATEGORIES

__all__ = ("BusinessClassificationsAPI", "MerchantCategoriesAPI",)


class BusinessClassificationsAPI(MerchantAPIView):
    def get(self, request):
        account = request.account
        categories = BusinessClassifications(account_id=account.id).get()
        return self.response(categories)


class MerchantCategoriesAPI(APIView):
    def get(self, request):
        return self.response(MERCHANT_CATEGORIES)
