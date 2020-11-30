from datetime import date

from django.utils.translation import gettext as _

from api.views import APIView
from apps.account.services import CreateConsumerAccount

__all__ = "ConsumerSignupAPI"


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
