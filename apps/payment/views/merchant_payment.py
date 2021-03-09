from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.utils.dates import InvalidParams, get_date_range_from_params
from api.views import MerchantAPIView
from apps.payment.dbapi import (get_customer_details, get_merchant_customers,
                                get_merchant_payment,
                                get_merchant_transactions)
from apps.payment.responses import (CustomerBasicDetailsResponse,
                                    DisputeListResponse,
                                    MerchantTransactionHistoryResponse,
                                    PaymentDetailsResponse,
                                    PaymentListResponse, RefundListResponse)

__all__ = (
    "MerchantPaymentHistoryAPI",
    "MerchantPaymentDetailsAPI",
    "MerchantCustomersAPI",
)


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
            raise ValidationError(
                {"detail": ErrorDetail(_("Invalid payment_id."))}
            )

        return self.response(PaymentDetailsResponse(payment).data)


class MerchantCustomersAPI(MerchantAPIView):
    def get(self, request):
        merchant_account = request.merchant_account
        customers_response = get_merchant_customers(
            merchant_account=merchant_account
        )
        return self.response(customers_response)


class MerchantCustomerDetailsAPI(MerchantAPIView):
    def get(self, request, customer_id):
        merchant_account = request.merchant_account
        customer_data = get_customer_details(
            merchant_account=merchant_account, customer_id=customer_id
        )
        if not customer_data:
            raise ValidationError(
                {"detail": ErrorDetail(_("Invalid customer_id."))}
            )
        consumer_account = customer_data["consumer_account"]
        payments = customer_data["payments"]
        refunds = customer_data["refunds"]
        disputes = customer_data["disputes"]
        return self.response(
            {
                **CustomerBasicDetailsResponse(consumer_account).data,
                "payments": PaymentListResponse(payments, many=True).data,
                "refunds": RefundListResponse(refunds, many=True).data,
                "disputes": DisputeListResponse(disputes, many=True).data,
            }
        )
