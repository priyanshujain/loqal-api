from os import stat
from typing import cast

from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.utils.dates import InvalidParams, get_date_range_from_params
from api.views import MerchantAPIView
from apps.payment.dbapi import get_merchant_payment, get_merchant_transactions
from apps.payment.responses import (MerchantTransactionHistoryResponse,
                                    PaymentDetailsResponse)

__all__ = ("MerchantPaymentHistoryAPI", "MerchantPaymentDetailsAPI")


class MerchantPaymentHistoryAPI(MerchantAPIView):
    def get(self, request):
        merchant_account = request.merchant_account
        start, end = self.validate_params(params=self.request_data)
        transactions = get_merchant_transactions(
            merchant_account=merchant_account
        )

        if start and end:
            transactions = transactions.filter(created_at__range=[start, end])
        return self.response(
            MerchantTransactionHistoryResponse(transactions, many=True).data
        )

    def validate_params(self, params):
        try:
            start, end = get_date_range_from_params(
                params=params, optional=True
            )
        except InvalidParams as e:
            raise ValidationError({"detail": ErrorDetail(_(str(e)))})
        return start, end


class MerchantPaymentDetailsAPI(MerchantAPIView):
    def get(self, request, payment_id):
        merchant_account = request.merchant_account
        payment = get_merchant_payment(
            merchant_account=merchant_account, payment_id=payment_id
        )
        if not payment:
            self.response(status=404)

        return self.response(PaymentDetailsResponse(payment).data)
