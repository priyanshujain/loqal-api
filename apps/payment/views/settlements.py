from apps.payment.models import transaction
from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.views import  MerchantAPIView
from apps.payment.dbapi.settlements import get_all_merchant_transanction
from apps.payment.responses import (ConsumerPaymentRequestResponse,
                                    MerchantTransactionHistoryResponse,
                                    PaymentRequestResponse,
                                    RecentStoresResponse,
                                    RefundHistoryResponse,
                                    TransactionDetailsResponse,
                                    TransactionHistoryResponse,
                                    TransactionResponse)


class ListMerchantTransactionsAPI(MerchantAPIView):
    def get(self, request):
        transactions = get_all_merchant_transanction(
            merchant_id=request.merchant_account.id
        )
        return self.response(
            PaymentRequestResponse(transactions, many=True).data
        )