from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.utils.dates import InvalidParams, get_date_range_from_params
from api.views import ConsumerAPIView, MerchantAPIView
from apps.payment.dbapi import (get_consumer_dispute_by_transaction,
                                get_dispute_by_id, get_merchant_disputes)
from apps.payment.dbapi.payment import get_consumer_transaction
from apps.payment.options import DisputeReasonType
from apps.payment.responses import (ConsumerDisputeDetailsResponse,
                                    DisputeHistoryResponse,
                                    MerchantDisputeDetailsResponse)
from apps.payment.services import CreateDispute


class DisputeListAPI(MerchantAPIView):
    def get(self, request):
        merchant_account = request.merchant_account
        start, end = self.validate_params(params=self.request_data)
        disputes = get_merchant_disputes(merchant_account=merchant_account)
        if start and end:
            disputes = disputes.filter(created_at__range=[start, end])
        return self.response(DisputeHistoryResponse(disputes, many=True).data)

    def validate_params(self, params):
        try:
            start, end = get_date_range_from_params(
                params=params, optional=True
            )
        except InvalidParams as e:
            raise ValidationError({"detail": ErrorDetail(_(str(e)))})
        return start, end


class CreateDisputeAPI(ConsumerAPIView):
    def post(self, request):
        consumer_account = request.consumer_account
        dispute = CreateDispute(
            consumer_account=consumer_account,
            data=self.request_data,
        ).handle()
        return self.response(
            {"dispute_tracking_id": dispute.dispute_tracking_id}, status=201
        )


class DisputeReasonTypesAPI(ConsumerAPIView):
    def get(self, request):
        return self.response(
            [
                {
                    "dispute_reason_type_label": v,
                    "dispute_reason_type_value": k,
                }
                for k, v in DisputeReasonType.choices
            ]
        )


class ConsumerDisputeDetailsAPI(ConsumerAPIView):
    def get(self, request):
        consumer_account = request.consumer_account
        transaction_id = self.request_data.get("transaction_id")
        if not transaction_id:
            raise ValidationError(
                {"detail": ErrorDetail(_("transaction_id is required."))}
            )
        transaction = get_consumer_transaction(
            consumer_account=consumer_account,
            transaction_tracking_id=transaction_id,
        )
        if not transaction:
            raise ValidationError(
                {"detail": ErrorDetail(_("transaction_id is not valid."))}
            )
        dispute = get_consumer_dispute_by_transaction(
            consumer_account=consumer_account, transaction_id=transaction.id
        )
        if not dispute:
            raise ValidationError({"detail": ErrorDetail(_("No dispute."))})
        return self.response(ConsumerDisputeDetailsResponse(dispute).data)


class MerchantDisputeDetailsAPI(MerchantAPIView):
    def get(self, request, dispute_id):
        merchant_account = request.merchant_account
        dispute = get_dispute_by_id(
            merchant_account=merchant_account, dispute_id=dispute_id
        )
        if not dispute:
            raise ValidationError({"detail": ErrorDetail(_("No dispute."))})
        return self.response(MerchantDisputeDetailsResponse(dispute).data)
