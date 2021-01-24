from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.views import APIView, MerchantAPIView
from apps.account.responses import MerchantAccountProfileResponse
from apps.account.services import CreateMerchantAccount
from apps.account.validators import CreateMerchantAccountValidator
from apps.user.services import AfterLogin
from utils.auth import login

__all__ = (
    "MerchantSignupAPI",
    "MerchantProfileAPI",
)


class MerchantSignupAPI(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            raise ValidationError(
                {"details": ErrorDetail(_("User has aleady logged in."))}
            )

        data = run_validator(CreateMerchantAccountValidator, self.request_data)
        self._run_services(data=data)
        return self.response(status=201)

    def _run_services(self, data):
        service = CreateMerchantAccount(data=data)
        account_member = service.handle()
        login(request=self.request, user=account_member.user)
        AfterLogin(
            request=self.request, user=account_member.user, send_alert=False
        )


class MerchantProfileAPI(MerchantAPIView):
    def get(self, request):
        merchant_account = request.merchant_account
        return self.response(
            MerchantAccountProfileResponse(merchant_account).data
        )
