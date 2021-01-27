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


class TransactionFailureReasonType(ChoiceCharEnum):
    TRANSACTION_DAILY_LIMIT_EXCEEDED = "transaction_daily_limit_exceeded", _(
        "Transaction daily limit exceeded."
    )
    TRANSACTION_WEEKLY_LIMIT_EXCEEDED = "transaction_weekly_limit_exceeded", _(
        "Transaction weekly limit exceeded."
    )
    BALANCE_CHECK_FAILED = "balance_check_failed", _("Balance check failed.")
    INSUFFICIENT_BALANCE = "insufficient_balance", _("Insufficient Balance.")
    PROVIDER_PAYMENT_SERVICE_FAILED = "provider_payment_service_failed", _(
        "Provider payment service failed."
    )
    INTERNAL_PAYMENT_SERVICE_FAILED = "internal_payment_service_failed", _(
        "Internal payment service failed."
    )
    PRE_SOURCE_ACH_FAILED = "pre_source_ach_failed", (
        "Pre transfer ACH return on source bank"
    )
    PRE_DESTINATION_ACH_FAILED = "pre_destination_ach_failed", (
        "Pre transfer ACH return on destination bank"
    )
    PRE_SETTLEMENT_INSUFFICIENT_BALANCE_AT_DESTINATION = (
        "pre_settlement_insufficient_balance_at_destination",
        ("Pre transfer ACH return on destination bank"),
    )
    PS_SOURCE_TRANSFER_FAILED = "ps_source_transfer_failed", _(
        "Post settlement ACH return on source bank"
    )
    OTHER = "other", _("Other")
    NA = "na", _("NA")


class TransactionStatus(ChoiceEnum):
    NOT_SENT = 0, _("Not Sent")
    PENDING = 1, _("Pending")
    PROCESSED = 2, _("Processed")
    FAILED = 3, _("Failed")
    CANCELLED = 4, _("Cancelled")
    UNKNOWN_PSP_ERROR = 5, _("Unknown PSP Error")
    INTERNAL_ERROR = 6, _("Internal Error")
    SENDER_COMPLETED = 7, _("Sender Completed")


class TransactionSenderStatus(ChoiceCharEnum):
    # UVC: unverified customer, VC: verified customer
    NOT_STARTED = "not_started", _("Not started")
    UVC_BANK_TRANSFER_CREATED = "uvc_bank_transfer_created", _(
        "Transfer created from bank"
    )
    UVC_BANK_TRANSFER_FAILED = "uvc_bank_transfer_failed", _(
        "Bank transfer failed"
    )
    UVC_BANK_TRANSFER_COMPLETED = "uvc_bank_transfer_completed", _(
        "Sender Transfer Completed"
    )
    UVC_BANK_TRANSFER_CANCELLED = "uvc_bank_transfer_cancelled", _(
        "Sender bank transfer Cancelled"
    )
    VC_BALANCE_TRANSFER_CREATED = "vc_bank_transfer_created", _(
        "Transfer created from balance"
    )
    VC_BANK_TRANSFER_CREATED = "vc_bank_transfer_created", _(
        "Sender bank transfer created"
    )
    VC_BANK_TRANSFER_CREATION_FAILED = "vc_bank_transfer_creation_failed", _(
        "Bank transfer creation failed"
    )
    VC_BANK_TRANSFER_CANCELLED = "vc_bank_transfer_failed", _(
        "Bank transfer cancelled"
    )
    VC_BANK_TRANSFER_FAILED = "vc_bank_transfer_failed", _(
        "Bank transfer failed"
    )
    VC_BANK_TRANSFER_COMPLETED = "vc_bank_transfer_completed", _(
        "Sender Transfer Completed"
    )
    VC_FROM_BALANCE_TRANSFER_CREATED = "vc_from_balance_transfer_created", _(
        "From Balance transfer created"
    )
    VC_FROM_BALANCE_TRANSFER_CANCELLED = (
        "vc_from_balance_transfer_cancelled",
        _("From Balance transfer cancelled"),
    )
    VC_FROM_BALANCE_TRANSFER_FAILED = "vc_from_balance_transfer_failed", _(
        "From Balance transfer failed"
    )
    VC_FROM_BALANCE_TRANSFER_COMPLETED = (
        "vc_from_balance_transfer_completed",
        _("From Balance transfer completed"),
    )
    VC_TO_BALANCE_TRANSFER_CANCELLED = "vc_to_balance_transfer_cancelled", _(
        "To Balance transfer cancelled"
    )
    VC_TO_BALANCE_TRANSFER_FAILED = "vc_to_balance_transfer_failed", _(
        "To Balance transfer failed"
    )


class TransactionReceiverStatus(ChoiceCharEnum):
    # UVC: unverified customer, VC: verified customer
    NOT_STARTED = "not_started", _("Not started")
    VC_TO_BALANCE_TRANSFER_CREATED = "vc_to_balance_transfer_created", _(
        "To Balance transfer created"
    )
    VC_TO_BALANCE_TRANSFER_CANCELLED = "vc_to_balance_transfer_cancelled", _(
        "To Balance transfer cancelled"
    )
    VC_TO_BALANCE_TRANSFER_FAILED = "vc_to_balance_transfer_failed", _(
        "To Balance transfer failed"
    )
    VC_TO_BALANCE_TRANSFER_COMPLETED = "vc_to_balance_transfer_completed", _(
        "Receiver Balance Received"
    )
    VC_FROM_BALANCE_TRANSFER_CREATED = "vc_from_balance_transfer_created", _(
        "From Balance transfer created"
    )
    VC_FROM_BALANCE_TRANSFER_CANCELLED = (
        "vc_from_balance_transfer_cancelled",
        _("From Balance transfer cancelled"),
    )
    VC_FROM_BALANCE_TRANSFER_FAILED = "vc_from_balance_transfer_failed", _(
        "From Balance transfer failed"
    )
    VC_BANK_TRANSFER_CREATED = "vc_bank_transfer_created", _(
        "Bank transfer created"
    )
    VC_BANK_TRANSFER_CREATION_FAILED = "vc_bank_transfer_creation_failed", _(
        "Bank transfer creation failed"
    )
    VC_BANK_TRANSFER_CANCELLED = "vc_bank_transfer_cancelled", _(
        "Bank transfer Cancelled"
    )
    VC_BANK_TRANSFER_FAILED = "vc_bank_transfer_failed", _(
        "Bank transfer failed"
    )
    VC_BANK_TRANSFER_COMPLETED = "vc_bank_transfer_completed", _(
        "Bank transfer completed"
    )
    UVC_BANK_TRANSFER_CREATED = "uvc_bank_transfer_created", _(
        "Bank transfer Created"
    )
    UVC_BANK_TRANSFER_CANCELLED = "uvc_bank_transfer_cancelled", _(
        "Bank transfer Cancelled"
    )
    UVC_BANK_TRANSFER_FAILED = "uvc_bank_transfer_failed", _(
        "Bank transfer failed"
    )
    UVC_BANK_TRANSFER_COMPLETED = "uvc_bank_transfer_completed", _(
        "Bank transfer completed"
    )


class TransactionEventType(ChoiceCharEnum):
    # UVC: unverified customer, VC: verified customer
    SENDER_NOT_STARTED = "sender_not_started", _("Not started")
    SENDER_UVC_BANK_TRANSFER_CREATED = "sender_uvc_bank_transfer_created", _(
        "Transfer created from bank"
    )
    SENDER_UVC_BANK_TRANSFER_FAILED = "sender_uvc_bank_transfer_failed", _(
        "Bank transfer failed"
    )
    SENDER_UVC_BANK_TRANSFER_COMPLETED = (
        "sender_uvc_bank_transfer_completed",
        _("Sender Transfer Completed"),
    )
    SENDER_UVC_BANK_TRANSFER_CANCELLED = (
        "sender_uvc_bank_transfer_cancelled",
        _("Sender bank transfer Cancelled"),
    )
    SENDER_VC_BALANCE_TRANSFER_CREATED = "sender_vc_bank_transfer_created", _(
        "Transfer created from balance"
    )
    SENDER_VC_BANK_TRANSFER_CREATED = "sender_vc_bank_transfer_created", _(
        "Sender bank transfer created"
    )
    SENDER_VC_BANK_TRANSFER_CREATION_FAILED = (
        "sender_vc_bank_transfer_creation_failed",
        _("Bank transfer creation failed"),
    )
    SENDER_VC_BANK_TRANSFER_CANCELLED = "sender_vc_bank_transfer_failed", _(
        "Bank transfer cancelled"
    )
    SENDER_VC_BANK_TRANSFER_FAILED = "sender_vc_bank_transfer_failed", _(
        "Bank transfer failed"
    )
    SENDER_VC_BANK_TRANSFER_COMPLETED = "sender_vc_bank_transfer_completed", _(
        "Sender Transfer Completed"
    )
    SENDER_VC_FROM_BALANCE_TRANSFER_CREATED = (
        "sender_vc_from_balance_transfer_created",
        _("From Balance transfer created"),
    )
    SENDER_VC_FROM_BALANCE_TRANSFER_CANCELLED = (
        "sender_vc_from_balance_transfer_cancelled",
        _("From Balance transfer cancelled"),
    )
    SENDER_VC_FROM_BALANCE_TRANSFER_FAILED = (
        "sender_vc_from_balance_transfer_failed",
        _("From Balance transfer failed"),
    )
    SENDER_VC_FROM_BALANCE_TRANSFER_COMPLETED = (
        "sender_vc_from_balance_transfer_completed",
        _("From Balance transfer completed"),
    )
    SENDER_VC_TO_BALANCE_TRANSFER_CANCELLED = (
        "sender_vc_to_balance_transfer_cancelled",
        _("To Balance transfer cancelled"),
    )
    SENDER_VC_TO_BALANCE_TRANSFER_FAILED = (
        "sender_vc_to_balance_transfer_failed",
        _("To Balance transfer failed"),
    )
    # UVC: unverified customer, VC: verified customer
    RECEIVER_NOT_STARTED = "receiver_not_started", _("Not started")
    RECEIVER_VC_TO_BALANCE_TRANSFER_CREATED = (
        "receiver_vc_to_balance_transfer_created",
        _("To Balance transfer created"),
    )
    RECEIVER_VC_TO_BALANCE_TRANSFER_CANCELLED = (
        "receiver_vc_to_balance_transfer_cancelled",
        _("To Balance transfer cancelled"),
    )
    RECEIVER_VC_TO_BALANCE_TRANSFER_FAILED = (
        "receiver_vc_to_balance_transfer_failed",
        _("To Balance transfer failed"),
    )
    RECEIVER_VC_TO_BALANCE_TRANSFER_COMPLETED = (
        "receiver_vc_to_balance_transfer_completed",
        _("Receiver Balance Received"),
    )
    RECEIVER_VC_FROM_BALANCE_TRANSFER_CREATED = (
        "receiver_vc_from_balance_transfer_created",
        _("From Balance transfer created"),
    )
    RECEIVER_VC_FROM_BALANCE_TRANSFER_CANCELLED = (
        "receiver_vc_from_balance_transfer_cancelled",
        _("From Balance transfer cancelled"),
    )
    RECEIVER_VC_FROM_BALANCE_TRANSFER_FAILED = (
        "receiver_vc_from_balance_transfer_failed",
        _("From Balance transfer failed"),
    )
    RECEIVER_VC_BANK_TRANSFER_CREATED = "receiver_vc_bank_transfer_created", _(
        "Bank transfer created"
    )
    RECEIVER_VC_BANK_TRANSFER_CREATION_FAILED = (
        "vc_bank_transfer_creation_failed",
        _("Bank transfer creation failed"),
    )
    RECEIVER_VC_BANK_TRANSFER_CANCELLED = (
        "receiver_vc_bank_transfer_cancelled",
        _("Bank transfer Cancelled"),
    )
    RECEIVER_VC_BANK_TRANSFER_FAILED = "receiver_vc_bank_transfer_failed", _(
        "Bank transfer failed"
    )
    RECEIVER_VC_BANK_TRANSFER_COMPLETED = (
        "receiver_vc_bank_transfer_completed",
        _("Bank transfer completed"),
    )
    RECEIVER_UVC_BANK_TRANSFER_CREATED = (
        "receiver_uvc_bank_transfer_created",
        _("Bank transfer Created"),
    )
    RECEIVER_UVC_BANK_TRANSFER_CANCELLED = (
        "receiver_uvc_bank_transfer_cancelled",
        _("Bank transfer Cancelled"),
    )
    RECEIVER_UVC_BANK_TRANSFER_FAILED = "receiver_uvc_bank_transfer_failed", _(
        "Bank transfer failed"
    )
    RECEIVER_UVC_BANK_TRANSFER_COMPLETED = (
        "receiver_uvc_bank_transfer_completed",
        _("Bank transfer completed"),
    )


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
    PAYMENT_DISPUTED = 5, _("Payment Disputed")
    REFUND_FAILED = 6, _("Refund Failed")
    PAYMENT_CANCELLED = 7, _("Payment Cancelled")


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
    OTHER = 8, _("Other")


class PaymentProcess(ChoiceEnum):
    QRCODE = 0, _("QR Code")
    DIRECT_APP = 1, _("App")
    PAYMENT_REQUEST = 2, _("Payment Request")
    NOT_PROVIDED = 3, _("Not Provided")


class DisputeStatus(ChoiceEnum):
    OPEN = 0, _("Open")
    INTERNAL_REVIEW = 1, _("Internal Review")
    BANK_REVIEW = 2, _("Bank Review")
    MERCHANT_REVIEW = 5, _("Merchany Review")
    CHARGEBACK_ACCEPTED = 3, _("Chargeback Accepted")
    CHARGEBACK_REJECTED = 4, _("Chargeback Rejected")


class DisputeType(ChoiceCharEnum):
    CHARGEBACK = "chargeback", _("Chargeback")
    FRAUD = "fraud", _("Fraud")
    RETRIEVAL = "retrieval", _("Retrieval")


class DisputeReasonType(ChoiceCharEnum):
    MONEY_NOT_REACHED = "money_not_reached", _(
        "Money has not reached to merchant"
    )
    PAID_TWICE = "paid_twice", _("Paid twice for the order")
    MORE_DETAILS_REQUIRED = "more_details_required", _(
        "Require more details on transaction"
    )
    DID_NOT_PERFORM = "did_not_perform", _(
        "I did not perform this transaction"
    )
    OTHER = "other", _("Other issues")


class DisputeReasonTypeMap:
    MONEY_NOT_REACHED = DisputeType.CHARGEBACK
    PAID_TWICE = DisputeType.CHARGEBACK
    MORE_DETAILS_REQUIRED = DisputeType.RETRIEVAL
    DID_NOT_PERFORM = DisputeType.FRAUD
    OTHER = DisputeType.RETRIEVAL
