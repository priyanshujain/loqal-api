from django.utils.translation import gettext as _

from api.helpers import run_validator
from api.views import APIView, MerchantAPIView
from apps.account.responses import MerchantAccountProfileResponse
from apps.account.services import CreateMerchantAccount
from apps.account.validators import CreateMerchantAccountValidator

__all__ = (
    "MerchantSignupAPI",
    "MerchantProfileAPI",
)


class MerchantSignupAPI(APIView):
    def post(self, request):
        data = run_validator(CreateMerchantAccountValidator, self.request_data)
        self._run_services(data=data)
        return self.response(status=201)

    def _run_services(self, data):
        service = CreateMerchantAccount(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            company_name=data["company_name"],
            phone_number=data["phone_number"],
            password=data["password"],
        )
        service.handle()


class MerchantProfileAPI(MerchantAPIView):
    def get(self, request):
        merchant_account = request.merchant_account
        return self.response(
            MerchantAccountProfileResponse(merchant_account).data
        )
