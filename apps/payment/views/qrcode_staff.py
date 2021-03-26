import qrcode as qrcodelib
from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.views import StaffAPIView
from apps.account.dbapi import get_merchant_account_by_uid
from apps.payment.dbapi import get_merchant_qrcodes, get_payment_qrcode_by_id
from apps.payment.responses import MerchantQrCodeResponse
from apps.payment.services import AssignQrCode
from utils.shortcuts import img2base64


class StaffMerchantBaseAPI(StaffAPIView):
    def validate_merchant(self, merchant_id):
        merchant_account = get_merchant_account_by_uid(
            merchant_uid=merchant_id
        )
        if not merchant_account:
            raise ValidationError(
                {"detail": ErrorDetail(_("Invalid merchant."))}
            )
        return merchant_account


class AssignQrCodeAPI(StaffMerchantBaseAPI):
    def post(self, request, merchant_id):
        merchant_account = self.validate_merchant(merchant_id=merchant_id)
        AssignQrCode(
            merchant_id=merchant_account.id, data=self.request_data
        ).handle()
        return self.response(status=200)


class GetAllMerchantQrCodesAPI(StaffMerchantBaseAPI):
    def get(self, request, merchant_id):
        merchant_account = self.validate_merchant(merchant_id=merchant_id)
        qrcodes = get_merchant_qrcodes(merchant_id=merchant_account.id)
        return self.response(MerchantQrCodeResponse(qrcodes, many=True).data)


class GetQrCodeImageAPI(StaffMerchantBaseAPI):
    def get(self, request, merchant_id):
        qrcode_id = self.request_data.get("qrcode_id")
        merchant = self.validate_merchant(merchant_id=merchant_id)
        qrcode = get_payment_qrcode_by_id(
            qrcode_id=qrcode_id,
            merchant_id=merchant.id,
        )
        if not qrcode:
            raise ValidationError(
                {"detail": ErrorDetail(_("Invalid QR code."))}
            )
        response_data = MerchantQrCodeResponse(qrcode).data
        image = qrcodelib.make(
            f"loqalapp://loqal/pay?qrcid={qrcode.qrcode_id}&type=merchant&currency={qrcode.currency}&gen={qrcode.created_at}/"
        )
        response_data["image_base64"] = img2base64(image)
        return self.response(response_data)
