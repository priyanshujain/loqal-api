from django.utils.translation import gettext as _

from api.views import APIView, MerchantAPIView
from apps.merchant.dbapi import get_merchant_pos_staff
from apps.merchant.responses import (CreatePosStaffResponse,
                                     ListPosStaffResponse)
from apps.merchant.services import (CreatePosStaff,
                                    GenerateLoginQrCodePosStaff,
                                    GeneratePinPosStaff, UpdatePosStaff)


class CreatePosStaffAPI(MerchantAPIView):
    """
    Create new pos staff api
    """

    def post(self, request):
        merchant = request.merchant_account
        pos_staff = CreatePosStaff(
            merchant=merchant, data=self.request_data
        ).handle()
        return self.response(CreatePosStaffResponse(pos_staff).data)


class GeneratePosStaffPinAPI(MerchantAPIView):
    """
    Create new pos staff api
    """

    def post(self, request, pos_staff_id):
        merchant = request.merchant_account
        login_pin = GeneratePinPosStaff(
            merchant=merchant, pos_staff_id=pos_staff_id
        ).handle()
        return self.response(
            {
                "pos_staff_id": pos_staff_id,
                "pos_staff_login_pin": login_pin,
            }
        )


class GeneratePosStaffLoginQrCodeAPI(MerchantAPIView):
    """
    Generate pos staff login QR code api
    """

    def get(self, request, pos_staff_id):
        merchant = request.merchant_account
        login_qrcode = GenerateLoginQrCodePosStaff(
            merchant=merchant, pos_staff_id=pos_staff_id
        ).handle()
        return self.response(login_qrcode)


class UpdatePosStaffAPI(MerchantAPIView):
    """
    Create new pos staff api
    """

    def put(self, request, pos_staff_id):
        merchant = request.merchant_account
        login_pin = UpdatePosStaff(
            merchant=merchant,
            pos_staff_id=pos_staff_id,
            data=self.request_data,
        ).handle()
        return self.response(status=204)


class GetPosStaffAPI(MerchantAPIView):
    """
    Create new pos staff api
    """

    def get(self, request):
        merchant = request.merchant_account
        pos_staff = get_merchant_pos_staff(merchant_id=merchant.id)
        return self.response(ListPosStaffResponse(pos_staff, many=True).data)
