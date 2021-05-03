from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.views import PosStaffAPIView
from apps.payment.dbapi import get_merchant_payment, get_pos_payments
from apps.payment.responses import (MerchantPaymentDetailsResponse,
                                    MerchantPaymentHistoryResponse)


class PosPaymentHistoryAPI(PosStaffAPIView):
    def get(self, request):
        pos_staff = request.pos_staff
        payments = get_pos_payments(register_id=pos_staff.register.id)
        return self.response(
            MerchantPaymentHistoryResponse(payments, many=True).data
        )


class PosPaymentDetailsAPI(PosStaffAPIView):
    def get(self, request, payment_id):
        merchant_account = request.merchant_account
        payment = get_merchant_payment(
            merchant_account=merchant_account, payment_id=payment_id
        )
        if not payment:
            raise ValidationError(
                {"detail": ErrorDetail(_("Invalid payment_id."))}
            )

        return self.response(MerchantPaymentDetailsResponse(payment).data)
