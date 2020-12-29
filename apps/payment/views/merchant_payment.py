from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.utils.dates import InvalidParams, get_date_range_from_params
from api.views import MerchantAPIView
from apps.payment.dbapi import get_merchant_transactions
from apps.payment.responses import MerchantTransactionHistoryResponse


__all__ = ("MerchantPaymentHistoryAPI",)


class MerchantPaymentHistoryAPI(MerchantAPIView):
    def get(self, request):
        merchant_account = request.merchant_account
        transactions = get_merchant_transactions(merchant_account=merchant_account)
        return self.response(
            MerchantTransactionHistoryResponse(transactions, many=True)
        )
