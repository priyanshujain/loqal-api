from api.helpers import run_validator
from api.views import APIAccessLogView
from apps.invite.services import InviteConsumerBySMS
from apps.invite.validators import PhoneNumberValidator

__all__ = ("DownloadAppAPI",)


class DownloadAppAPI(APIAccessLogView):
    def post(self, request):
        data = run_validator(PhoneNumberValidator, self.request_data)
        phone_number = data["phone_number"]
        InviteConsumerBySMS(phone_number=phone_number).handle()
        return self.response()
