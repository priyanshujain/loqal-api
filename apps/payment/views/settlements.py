from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.views import MerchantAPIView
from apps.payment.dbapi.settlements import (get_all_merchant_transanction,
                                            get_single_merchant_transanction)
from apps.payment.models import transaction
from apps.payment.responses.settlements import (SettlementDetailsResponse,
                                                SettlementListResponse)
from apps.provider.services.process_webhook.tasks import \
    process_past_webhooks_for_transaction


class ListMerchantSettlementsAPI(MerchantAPIView):
    def get(self, request):
        transactions = get_all_merchant_transanction(
            merchant_id=request.merchant_account.id
        )
        return self.paginate(
            request,
            queryset=transactions,
            order_by="-created_at",
            response_serializer=SettlementListResponse,
        )


class MerchantSettlementDetailsAPI(MerchantAPIView):
    def get(self, request, settlement_id):
        transaction = get_single_merchant_transanction(
            merchant_id=request.merchant_account.id,
            settlement_id=settlement_id,
        )
        process_past_webhooks_for_transaction(transaction)
        if not transaction:
            raise ValidationError(
                {"detail": ErrorDetail(_("Invalid settlement id."))}
            )
        return self.response(SettlementDetailsResponse(transaction).data)
