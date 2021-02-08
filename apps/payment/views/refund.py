from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.utils.dates import InvalidParams, get_date_range_from_params
from api.views import MerchantAPIView
from apps.payment.dbapi import get_merchant_refund, get_merchant_refunds
from apps.payment.responses import RefundDetailsResponse, RefundHistoryResponse

__all__ = (
    "RefundListAPI",
    "RefundDetailsAPI",
)


class RefundListAPI(MerchantAPIView):
    def get(self, request):
        merchant_account = request.merchant_account
        start, end = self.validate_params(params=self.request_data)
        refunds = get_merchant_refunds(merchant_account=merchant_account)
        if start and end:
            refunds = refunds.filter(created_at__range=[start, end])
        return self.response(RefundHistoryResponse(refunds, many=True).data)

    def validate_params(self, params):
        try:
            start, end = get_date_range_from_params(
                params=params, optional=True
            )
        except InvalidParams as e:
            raise ValidationError({"detail": ErrorDetail(_(str(e)))})
        return start, end


class RefundDetailsAPI(MerchantAPIView):
    def get(self, request, refund_id):
        merchant_account = request.merchant_account
        refund = get_merchant_refund(
            merchant_account=merchant_account, refund_id=refund_id
        )
        if not refund:
            raise ValidationError(
                {"detail": ErrorDetail("refund_id is not valid.")}
            )
        return self.response(RefundDetailsResponse(refund).data)
