from django.utils.translation import gettext as _

from apps.provider.options import DEFAULT_CURRENCY
from db.models.fields import ChoiceCharEnum, ChoiceEnum
from db.models.fields.choice import ChoiceCharEnum

FACILITATION_FEES_PERCENTAGE = 1.5
FACILITATION_FEES_CURRENCY = DEFAULT_CURRENCY


class TransactionType(ChoiceCharEnum):
    PAYMENT_REQUEST = "payment_request", _("Payment Request")
    DIRECT_MERCHANT_PAYMENT = "direct_merchant_payment", _(
        "Direct Merchant Payment"
    )
    REFUND_PAYMENT = "refund_payment", _("Refund Payment")
    OTHER = "other", _("Other")


class TransactionStatus(ChoiceEnum):
    NOT_SENT = 0, _("Not Sent")
    PENDING = 1, _("Pending")
    PROCESSED = 2, _("Processed")
    FAILED = 3, _("Failed")
    CANCELLED = 4, _("Cancelled")
    INTERNAL_PSP_ERROR = 5, _("Internal PSP Error")


class TransactionEventType(ChoiceEnum):
    TRANSACTION_SENT = 0, _("Tranasction Sent")
    TRANSACTION_FAILED = 1, _("Transaction Failed")
    TRANSACTION_PEDNING = 2, _("Transaction Pending")
    TRANSACTION_PROCESSED = 3, _("Transaction Processed")
    TRANSACTION_CANCELLED = 4, _("Transaction Cancelled")
    TRANSACTION_INTERNAL_ERROR = 5, _("Internal Error")


class PaymentStatus(ChoiceEnum):
    CAPTURED = 0, _("Captured")
    IN_PROGRESS = 1, _("In Progress")
    FAILED = 2, _("Failed")


class PaymentEventType(ChoiceEnum):
    PAYMENT_INTIATED = 0, _("Payment Initiated")
    PAYMENT_CAPTURED = 1, _("Payment Captured")
    PAYMENT_FAILED = 2, _("Payment Failed")
    PAYMENT_PARTIALLY_REFUNDED = 3, _("Partially Refunded")
    PAYMENT_FULLY_REFUNDED = 4, _("Fully Refunded")
    PAYMENT_DISPUTED = 4, _("Payment Disputed")


class PaymentRequestStatus(ChoiceEnum):
    REQUEST_SENT = 0, _("Request Sent")
    ACCEPTED = 1, _("Request Accepted")
    REJECTED = 2, _("Request Rejected")


class RefundType(ChoiceCharEnum):
    PARTIAL = "partial", _("Partial Refund")
    FULL = "full", _("Full Refund")


class RefundStatus(ChoiceEnum):
    PROCESSED = 0, _("Processed")
    FAILED = 1, _("Failed")


class PaymentMethodType(ChoiceCharEnum):
    ACH = "ach", _("ACH")


class ChargeStatus(ChoiceEnum):
    NOT_CHARGED = 0, _("Not Charged")
    PENDING = 1, _("Pending")
    PARTIALLY_CHARGED = 2, _("Partially Charged")
    FULLY_CHARGED = 3, _("Fully Charged")
    PARTIALLY_REFUNDED = 4, _("Partially Refunded")
    FULLY_REFUNDED = 5, _("Fully Refunded")
    REFUSED = 6, _("Refused")
    CANCELLED = 7, _("Cancelled")


class PaymentProcess(ChoiceEnum):
    QRCODE = 0, _("QR Code")
    DIRECT_APP = 1, _("App")
    PAYMENT_REQUEST = 2, _("Payment Request")
    NOT_PROVIDED = 3, _("Not Provided")


class DisputeStatus(ChoiceEnum):
    OPEN = 0, _("Open")
    INTERNAL_REVIEW = 1, _("Internal Review")
    BANK_REVIEW = 2, _("BANK_REVIEW")
    CHARGEBACK_ACCEPTED = 3, _("Chargeback Accepted")
    CHARGEBACK_REJECTED = 4, _("Chargeback Rejected")


class DisputeStatus(ChoiceEnum):
    OPEN = 0, _("Open")
    INTERNAL_REVIEW = 1, _("Internal Review")
    BANK_REVIEW = 2, _("BANK_REVIEW")
    CHARGEBACK_ACCEPTED = 3, _("Chargeback Accepted")
    CHARGEBACK_REJECTED = 4, _("Chargeback Rejected")


class DisputeType(ChoiceCharEnum):
    CHARGEBACK = "chargeback", _("Chargeback")
    FRAUD = "fraud", _("Fraud")


class DisputeReasonType(ChoiceCharEnum):
    MONEY_NOT_REACHED = "money_not_reached", _(
        "Money has not reached to merchant"
    )
    PAID_TWICE = "paid_twice", _("Paid twice for the order")
    OTHER = "other", _("Other issues")
