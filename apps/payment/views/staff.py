import qrcode as qrcodelib
from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.views import StaffAPIView
from apps.account.dbapi import get_merchant_account_by_uid
from apps.payment.dbapi import get_all_qrcodes, get_single_qrcode_by_id
from apps.payment.responses import StaffQrCodeResponse
from utils.shortcuts import img2base64


class StaffBaseAPI(StaffAPIView):
    def validate_merchant(self, merchant_id):
        merchant_account = get_merchant_account_by_uid(
            merchant_uid=merchant_id
        )
        if not merchant_account:
            raise ValidationError(
                {"detail": ErrorDetail(_("Invalid merchant."))}
            )
        return merchant_account


class GetAllQrCodesAPI(StaffAPIView):
    def get(self, request):
        qrcodes = get_all_qrcodes()
        return self.response(StaffQrCodeResponse(qrcodes, many=True).data)


class GetQrCodeImageAPI(StaffAPIView):
    def get(self, request, qrcode_id):
        qrcode = get_single_qrcode_by_id(
            qrcode_id=qrcode_id,
        )
        if not qrcode:
            raise ValidationError(
                {"detail": ErrorDetail(_("Invalid QR code."))}
            )
        response_data = StaffQrCodeResponse(qrcode).data
        image = qrcodelib.make(
            f"loqalapp://loqal/pay?qrcid={qrcode.qrcode_id}&type=merchant&currency={qrcode.currency}&gen={qrcode.created_at}/"
        )
        response_data["image_base64"] = img2base64(image)
        return self.response(response_data)
