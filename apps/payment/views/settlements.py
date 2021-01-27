from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.views import MerchantAPIView
from apps.payment.dbapi.settlements import (get_all_merchant_transanction,
                                            get_single_merchant_transanction)
from apps.payment.models import transaction
from apps.payment.responses.settlements import (SettlementDetailsResponse,
                                                SettlementListResponse)


class ListMerchantSettlementsAPI(MerchantAPIView):
    def get(self, request):
        transactions = get_all_merchant_transanction(
            merchant_id=request.merchant_account.id
        )
        return self.response(
            SettlementListResponse(transactions, many=True).data
        )


class MerchantSettlementDetailsAPI(MerchantAPIView):
    def get(self, request, settlement_id):
        transaction = get_single_merchant_transanction(
            merchant_id=request.merchant_account.id,
            settlement_id=settlement_id,
        )
        if not transaction:
            raise ValidationError(
                {"detail": ErrorDetail(_("Invalid settlement id."))}
            )
        return self.response(SettlementDetailsResponse(transaction).data)
