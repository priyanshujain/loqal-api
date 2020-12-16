from django.utils.translation import gettext as _

from db.models.fields import ChoiceEnum

from apps.provider.options import DEFAULT_CURRENCY

FACILITATION_FEES_PERCENTAGE = 1.5
FACILITATION_FEES_CURRENCY = DEFAULT_CURRENCY


class TransactionStatus(ChoiceEnum):
    NOT_SENT = 0, _("Not Sent")
    PENDING = 1, _("Pending")
    PROCESSED = 2, _("Processed")
    FAILED = 3, _("Failed")
    CANCELLED = 4, _("Cancelled")


class PaymentRequestStatus(ChoiceEnum):
    REQUEST_SENT = 0, _("Request Sent")
    PROCESSED = 1, _("Request Processed")
    CANCELLED = 2, _("Request Cancelled")
