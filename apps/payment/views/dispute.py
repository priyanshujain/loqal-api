from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.utils.dates import InvalidParams, get_date_range_from_params
from api.views import MerchantAPIView
from apps.payment.dbapi import get_merchant_disputes
from apps.payment.responses import DisputeHistoryResponse

__all__ = ("DisputeListAPI",)


class DisputeListAPI(MerchantAPIView):
    def get(self, request):
        merchant_account = request.merchant_account
        start, end = self.validate_params(params=self.request_data)
        disputes = get_merchant_disputes(
            merchant_account=merchant_account
        )
        if start and end:
            disputes = disputes.filter(created_at__range=[start, end])
        return self.response(
            DisputeHistoryResponse(disputes, many=True).data
        )

    def validate_params(self, params):
        try:
            start, end = get_date_range_from_params(
                params=params, optional=True
            )
        except InvalidParams as e:
            raise ValidationError({"detail": ErrorDetail(_(str(e)))})
        return start, end


