import qrcode as qrcodelib
from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.views import StaffAPIView
from apps.account.dbapi import (get_consumer_account_by_uid,
                                get_merchant_account_by_uid)
from apps.payment.dbapi import (get_all_qrcodes, get_merchant_receive_limit,
                                get_payment_register, get_single_qrcode_by_id,
                                update_consumer_limit,
                                update_merchant_receive_limit)
from apps.payment.responses import (MerchantReceiveLimitResponse,
                                    PaymentRegisterResponse,
                                    StaffQrCodeResponse)
from apps.payment.validators import (MerchantReceiveLimitValidator,
                                     PaymentRegisterValidator)
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


class StaffConsumerBaseAPI(StaffAPIView):
    def validate_consumer(self, consumer_id):
        consumer_account = get_consumer_account_by_uid(
            consumer_uid=consumer_id
        )
        if not consumer_account:
            raise ValidationError(
                {"detail": ErrorDetail(_("Invalid consumer."))}
            )
        return consumer_account


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


class ConsumerPaymentLimitAPI(StaffConsumerBaseAPI):
    def get(self, request, consumer_id):
        consumer_account = self.validate_consumer(consumer_id=consumer_id)
        payment_register = get_payment_register(
            account_id=consumer_account.account.id
        )
        if not payment_register:
            return self.response()
        return self.response(PaymentRegisterResponse(payment_register).data)

    def put(self, request, consumer_id):
        consumer_account = self.validate_consumer(consumer_id=consumer_id)
        data = run_validator(PaymentRegisterValidator, self.request_data)
        daily_send_limit = data["daily_send_limit"]
        update_consumer_limit(
            account_id=consumer_account.account.id,
            daily_send_limit=daily_send_limit,
        )
        return self.response()


class MerchantReceiveLimitAPI(StaffMerchantBaseAPI):
    def get(self, request, merchant_id):
        merchant_account = self.validate_merchant(merchant_id=merchant_id)
        merchant_receive_limit = get_merchant_receive_limit(
            merchant_id=merchant_account.id
        )
        if not merchant_receive_limit:
            return self.response()
        return self.response(
            MerchantReceiveLimitResponse(merchant_receive_limit).data
        )

    def put(self, request, merchant_id):
        merchant_account = self.validate_merchant(merchant_id=merchant_id)
        data = run_validator(MerchantReceiveLimitValidator, self.request_data)
        transaction_limit = data["transaction_limit"]
        update_merchant_receive_limit(
            merchant_id=merchant_account.id,
            transaction_limit=transaction_limit,
        )
        return self.response()
