from rest_framework.settings import IMPORT_STRINGS

from api.helpers import run_validator
from api.views import MerchantAPIView, PosStaffAPIView
from apps.merchant.services import InviteConsumerBySMS
from apps.merchant.validators import PhoneNumberValidator

__all__ = (
    "InviteConsumerAPI",
    "InvitePosConsumerAPI",
)


class InviteConsumerAPI(MerchantAPIView):
    def post(self, request):
        merchant = request.merchant_account
        data = run_validator(PhoneNumberValidator, self.request_data)
        phone_number = data["phone_number"]
        InviteConsumerBySMS(
            merchant=merchant, phone_number=phone_number
        ).handle()
        return self.response()


class InvitePosConsumerAPI(PosStaffAPIView):
    pass
