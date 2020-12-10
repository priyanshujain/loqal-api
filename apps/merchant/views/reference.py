from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.views import ConsumerAPIView, MerchantAPIView
from apps.merchant.services import BusinessClassifications

__all__ = ("BusinessClassificationsAPI",)


class BusinessClassificationsAPI(ConsumerAPIView):
    def get(self, request):
        account = request.account
        categories = BusinessClassifications(account_id=account.id).get()
        return self.response(categories)
