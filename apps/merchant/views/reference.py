from apps.merchant.services import BusinessClassifications
from api.exceptions import ValidationError, ErrorDetail

from django.utils.translation import gettext as _

from api.views import ConsumerAPIView, MerchantAPIView

__all__ = (
    "BusinessClassificationsAPI",
)


class BusinessClassificationsAPI(ConsumerAPIView):
    def get(self, request):
        account = request.account
        categories = BusinessClassifications(account_id=account.id).get()
        return self.response(categories)

