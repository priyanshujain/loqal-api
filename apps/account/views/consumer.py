from datetime import date

from django.utils.translation import gettext as _

from api.views import APIView, UserAPIView
from apps.account.responses import ConsumerAccountProfileResponse
from apps.account.services import AddZipCode, CreateConsumerAccount

__all__ = (
    "ConsumerSignupAPI",
    "AddAccountZipCodeAPI",
    "ConsumerAccountProfileAPI",
)


class ConsumerSignupAPI(APIView):
    def post(self, request):
        self._run_services(ip_address=request.ip)
        return self.response(status=201)

    def _run_services(self, ip_address):
        data = self.request_data
        service = CreateConsumerAccount(
            data=self.request_data, ip_address=ip_address
        )
        service.execute()


class AddAccountZipCodeAPI(UserAPIView):
    def post(self, request):
        account = request.account
        self._run_services(account=account)
        return self.response()

    def _run_services(self, account):
        data = self.request_data
        service = AddZipCode(data=self.request_data, account=account)
        service.execute()


class ConsumerAccountProfileAPI(UserAPIView):
    def get(self, request):
        account = request.account
        return self.response(ConsumerAccountProfileResponse(account).data)
