from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.views import LoggedInAPIView

from .dbapi import create_support_ticket, get_support_tickets
from .emails import SendSupportEmail
from .repsonses import SupportTicketHistoryResponse
from .validators import SupportTicketValidator


class SupportRequestAPI(LoggedInAPIView):
    def post(self, request):
        user = request.user
        data = run_validator(
            validator=SupportTicketValidator, data=self.request_data
        )
        support_ticket = create_support_ticket(
            user_id=user.id, message=data["message"]
        )
        SendSupportEmail(
            user=user,
            message=support_ticket.message,
            issue_tracking_id=support_ticket.issue_tracking_id,
        ).send()
        return self.response(status=201)


class SupportRequestHistoryAPI(LoggedInAPIView):
    def get(self, request):
        user = request.user
        support_tickets = get_support_tickets(user_id=user.id)
        return self.response(
            SupportTicketHistoryResponse(support_tickets, many=True).data
        )
