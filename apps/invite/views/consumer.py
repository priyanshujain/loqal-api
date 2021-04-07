from api.helpers import run_validator
from api.views import APIAccessLogView, ConsumerAPIView
from apps.invite.dbapi import get_c2c_invites
from apps.invite.responses import ConsumerInviteResponse
from apps.invite.services import (FilterNonLoqalConsumers, InviteConsumer,
                                  InviteConsumerBySMS)
from apps.invite.validators import (C2CInviteValidator,
                                    PhoneNumberListValidator,
                                    PhoneNumberValidator)

__all__ = (
    "DownloadAppAPI",
    "FilterNonLoqalConsumersAPI",
    "InviteConsumerAPI",
    "ResendConsumerInviteAPI",
    "ConsumerInvitesAPI",
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


class InviteConsumerAPI(ConsumerAPIView):
    def post(self, request):
        data = run_validator(C2CInviteValidator, self.request_data)
        phone_number = data.get("phone_number")
        consumer = request.consumer_account
        c2c_invite = InviteConsumer(
            phone_number=phone_number, consumer=consumer
        ).handle()
        return self.response(
            ConsumerInviteResponse(c2c_invite).data, status=201
        )


class ResendConsumerInviteAPI(ConsumerAPIView):
    def post(self, request):
        data = run_validator(C2CInviteValidator, self.request_data)
        phone_number = data.get("phone_number")
        consumer = request.consumer_account
        InviteConsumer(
            phone_number=phone_number, consumer=consumer, resend=True
        ).handle()
        return self.response()


class ConsumerInvitesAPI(ConsumerAPIView):
    def get(self, request):
        consumer = request.consumer_account
        c2c_invites = get_c2c_invites(consumer_id=consumer.id)
        return self.response(
            ConsumerInviteResponse(c2c_invites, many=True).data
        )
