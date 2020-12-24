from django.utils.translation import gettext as _

from apps.provider.options import DEFAULT_CURRENCY
from db.models.fields import ChoiceCharEnum, ChoiceEnum
from db.models.fields.choice import ChoiceCharEnum

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
    ACCEPTED = 1, _("Request Accepted")
    REJECTED = 2, _("Request Rejected")


class TransactionTypes(ChoiceCharEnum):
    PAYMENT = "payment", _("Payment")
    REFUND = "refund", _("Refund")


class RefundType(ChoiceCharEnum):
    PARTIAL = "partial", _("Partial Refund")
    FULL = "full", _("Full Refund")


class RefundStatus(ChoiceEnum):
    SUCCESS = 0, _("Success")
    FAILED = 1, _("Failed")


class PaymentStatus(ChoiceEnum):
    SUCCESS = 0, _("Success")
    IN_PROGRESS = 1, _("In Progress")
    FAILED = 2, _("Failed")


class PaymentMethodType(ChoiceCharEnum):
    ACH = "ach", _("ACH")


class QrCodePaymentStatus(ChoiceEnum):
    SUCCESS = 0, _("Success")
    IN_PROGRESS = 1, _("In Progress")
    FAILED = 2, _("Failed")