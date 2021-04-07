from api.helpers import run_validator
from api.views import APIAccessLogView, ConsumerAPIView
from apps.invite.services import FilterNonLoqalConsumers, InviteConsumerBySMS
from apps.invite.validators import PhoneNumberValidator, PhoneNumberListValidator


__all__ = (
    "DownloadAppAPI",
    "FilterNonLoqalConsumersAPI",
)


class DownloadAppAPI(APIAccessLogView):
    def post(self, request):
        data = run_validator(PhoneNumberValidator, self.request_data)
        phone_number = data["phone_number"]
        InviteConsumerBySMS(phone_number=phone_number).handle()
        return self.response()


class FilterNonLoqalConsumersAPI(ConsumerAPIView):
    def post(self, request):
        data = run_validator(PhoneNumberListValidator, self.request_data)
        phone_numbers = data.get("phone_numbers", [])
        data = FilterNonLoqalConsumers(phone_numbers=phone_numbers).handle()
        return self.response(data)
