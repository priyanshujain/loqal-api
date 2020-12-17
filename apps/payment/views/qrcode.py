import qrcode as qrcodelib
from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.views import ConsumerAPIView, MerchantAPIView
from apps.payment.dbapi import (get_cashier_qrcode, get_merchant_qrcodes,
                                get_payment_qrcode)
from apps.payment.responses import (MerchantQrCodeResponse,
                                    QrCodeMerchantDetailsResponse,
                                    QrCodeResponse)
from apps.payment.services import AssignQrCode, CreateQrCode
from utils.shortcuts import img2base64


class CreateQrCodeAPI(MerchantAPIView):
    def post(self, request):
        qrcode = CreateQrCode().handle()
        return self.response(QrCodeResponse(qrcode).data, status=201)


class AssignQrCodeAPI(MerchantAPIView):
    def post(self, request):
        merchant_account = request.merchant_account
        AssignQrCode(
            merchant_id=merchant_account.id, data=self.request_data
        ).handle()
        return self.response(status=200)


class GetAllMerchantQrCodesAPI(MerchantAPIView):
    def get(self, request):
        merchant_account = request.merchant_account
        qrcodes = get_merchant_qrcodes(merchant_id=merchant_account.id)
        return self.response(MerchantQrCodeResponse(qrcodes, many=True).data)


class GetCashierQrCodesAPI(MerchantAPIView):
    def get(self, request):
        merchant_account_member = request.merchant_account_member
        qrcode = get_cashier_qrcode(
            merchant_id=merchant_account_member.merchant.id,
            cashier_id=merchant_account_member.id,
        )
        response_data = MerchantQrCodeResponse(qrcode).data
        image = qrcodelib.make(
            f"loqal://pay?qrcid={qrcode.qrcode_id}&type=merchant&currency={qrcode.currency}&gen={qrcode.created_at}"
        )
        response_data["image_base64"] = img2base64(image)
        return self.response(response_data)


class GetQrCodeMerchantDetailsAPI(ConsumerAPIView):
    def get(self, request):
        qrcode_id = self.request_data.get("qrcid")
        qrcode = get_payment_qrcode(qrcode_id=qrcode_id)
        if not qrcode or not qrcode.merchant:
            raise ValidationError(
                {"detail": ErrorDetail(_("Invalid QR code."))}
            )
        return self.response(
            QrCodeMerchantDetailsResponse(qrcode.merchant).data
        )
