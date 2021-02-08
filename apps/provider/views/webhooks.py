from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.views import StaffAPIView
from apps.account.dbapi import get_merchant_account_by_uid
from apps.provider.dbapi import get_merchant_webhook_event, get_webhook_event
from apps.provider.responses import (ListMerchantWebhookEventsResponse,
                                     WebhookEventDetailsResponse)
from apps.provider.services.process_webhook.tasks import \
    process_single_webhook_event


class StaffBaseAPI(StaffAPIView):
    def validate_merchant(self, merchant_id):
        merchant_account = get_merchant_account_by_uid(
            merchant_uid=merchant_id
        )
        if not merchant_account:
            raise ValidationError(
                {"detail": ErrorDetail(_("Invalid merchant."))}
            )
        return merchant_account


class GetMerchantWebhookEventsAPI(StaffBaseAPI):
    def get(self, request, merchant_id):
        merchant_account = self.validate_merchant(merchant_id)
        if not merchant_account.account:
            raise ValidationError(
                {"detail": ErrorDetail(_("Invalid merchant."))}
            )
        events = get_merchant_webhook_event(merchant_account=merchant_account)
        return self.paginate(
            request,
            queryset=events,
            response_serializer=ListMerchantWebhookEventsResponse,
        )


class GetWebhookEventDetailsAPI(StaffBaseAPI):
    def get(self, request, event_id):
        event = get_webhook_event(id=event_id)
        if not event:
            raise ValidationError({"detail": ErrorDetail(_("Invalid event."))})
        return self.response(WebhookEventDetailsResponse(event).data)


class ProcessWebhookEventAPI(StaffBaseAPI):
    def post(self, request, event_id):
        event = get_webhook_event(id=event_id)
        if not event:
            raise ValidationError({"detail": ErrorDetail(_("Invalid event."))})
        process_single_webhook_event(event=event)
        return self.response()
