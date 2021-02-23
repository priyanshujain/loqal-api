from django.utils.translation import gettext as _

from apps.provider.options import DEFAULT_CURRENCY
from db.models.fields import ChoiceCharEnum, ChoiceEnum
from db.models.fields.choice import ChoiceCharEnum

PAYMENT_FACILITATION_FEES_PERCENTAGE = 1.5
REFUND_FACILITATION_FEES_PERCENTAGE = 0.5
PAYMENT_FACILITATION_FEES_FIXED = 0.15
REFUND_FACILITATION_FEES_FIXED = 0.05

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
        "Pre transfer ACH return on source bank."
    )
    PRE_DESTINATION_ACH_FAILED = "pre_destination_ach_failed", (
        "Pre transfer ACH return on destination bank."
    )
    PRE_SETTLEMENT_INSUFFICIENT_BALANCE_AT_DESTINATION = (
        "pre_settlement_insufficient_balance_at_destination",
        ("Pre transfer ACH return on destination bank."),
    )
    PS_SOURCE_TRANSFER_FAILED = "ps_source_transfer_failed", _(
        "Post settlement ACH return on source bank."
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
        "A transfer has been created from sender bank."
    )
    UVC_BANK_TRANSFER_FAILED = "uvc_bank_transfer_failed", _(
        "The transfer from sender bank account has failed."
    )
    UVC_BANK_TRANSFER_COMPLETED = "uvc_bank_transfer_completed", _(
        "The transfer from sender bank account has completed."
    )
    UVC_BANK_TRANSFER_CANCELLED = "uvc_bank_transfer_cancelled", _(
        "The transfer from sender bank account has cancelled."
    )
    VC_BALANCE_TRANSFER_CREATED = "vc_bank_transfer_created", _(
        "A transfer has been created from sender's Loqal balance."
    )
    VC_BANK_TRANSFER_CREATED = "vc_bank_transfer_created", _(
        "A transfer has been created from sender bank account."
    )
    VC_BANK_TRANSFER_CREATION_FAILED = "vc_bank_transfer_creation_failed", _(
        "The transfer creation from sender bank account has failed."
    )
    VC_BANK_TRANSFER_CANCELLED = "vc_bank_transfer_failed", _(
        "The transfer from sender bank account has cancelled."
    )
    VC_BANK_TRANSFER_FAILED = "vc_bank_transfer_failed", _(
        "The transfer from sender bank account has failed."
    )
    VC_BANK_TRANSFER_COMPLETED = "vc_bank_transfer_completed", _(
        "The transfer from sender bank account has completed."
    )
    VC_FROM_BALANCE_TRANSFER_CREATED = "vc_from_balance_transfer_created", _(
        "A transfer has been created from sender's Loqal balance."
    )
    VC_FROM_BALANCE_TRANSFER_CANCELLED = (
        "vc_from_balance_transfer_cancelled",
        _("The transfer from sender's Loqal balance has cancelled."),
    )
    VC_FROM_BALANCE_TRANSFER_FAILED = "vc_from_balance_transfer_failed", _(
        "The transfer from sender's Loqal balance has failed."
    )
    VC_FROM_BALANCE_TRANSFER_COMPLETED = (
        "vc_from_balance_transfer_completed",
        _("The transfer has completed to sender's Loqal balance."),
    )
    VC_TO_BALANCE_TRANSFER_CANCELLED = "vc_to_balance_transfer_cancelled", _(
        "The transfer to sender's Loqal balance has cancelled."
    )
    VC_TO_BALANCE_TRANSFER_FAILED = "vc_to_balance_transfer_failed", _(
        "The transfer to sender's Loqal balance has failed."
    )


class TransactionReceiverStatus(ChoiceCharEnum):
    # UVC: unverified customer, VC: verified customer
    NOT_STARTED = "not_started", _("Not started")
    VC_TO_BALANCE_TRANSFER_CREATED = "vc_to_balance_transfer_created", _(
        "A transfer has been created to receiver's Loqal balance."
    )
    VC_TO_BALANCE_TRANSFER_CANCELLED = "vc_to_balance_transfer_cancelled", _(
        "The transfer to receiver's Loqal balance has cancelled."
    )
    VC_TO_BALANCE_TRANSFER_FAILED = "vc_to_balance_transfer_failed", _(
        "The transfer to receiver's Loqal balance has failed."
    )
    VC_TO_BALANCE_TRANSFER_COMPLETED = "vc_to_balance_transfer_completed", _(
        "The transfer to receiver's Loqal balance has completed."
    )
    VC_FROM_BALANCE_TRANSFER_CREATED = "vc_from_balance_transfer_created", _(
        "A transfer has been created from receiver's Loqal balance to bank account."
    )
    VC_FROM_BALANCE_TRANSFER_CANCELLED = (
        "vc_from_balance_transfer_cancelled",
        _("A transfer from receiver's Loqal balance has cancelled."),
    )
    VC_FROM_BALANCE_TRANSFER_FAILED = "vc_from_balance_transfer_failed", _(
        "The transfer from receiver's Loqal balance has failed."
    )
    VC_BANK_TRANSFER_CREATED = "vc_bank_transfer_created", _(
        "The transfer has been created from receiver's Loqal balance to bank account."
    )
    VC_BANK_TRANSFER_CREATION_FAILED = "vc_bank_transfer_creation_failed", _(
        "The transfer from from receiver's Loqal balance to bank account has failed."
    )
    VC_BANK_TRANSFER_CANCELLED = "vc_bank_transfer_cancelled", _(
        "The transfer from receiver's Loqal balance to bank account has cancelled."
    )
    VC_BANK_TRANSFER_FAILED = "vc_bank_transfer_failed", _(
        "The transfer from receiver's Loqal balance to bank account has failed."
    )
    VC_BANK_TRANSFER_COMPLETED = "vc_bank_transfer_completed", _(
        "The transfer from receiver's Loqal balance to bank account has completed."
    )
    UVC_BANK_TRANSFER_CREATED = "uvc_bank_transfer_created", _(
        "The transfer has been created to receiver bank account."
    )
    UVC_BANK_TRANSFER_CANCELLED = "uvc_bank_transfer_cancelled", _(
        "The transfer to receiver bank account has cancelled."
    )
    UVC_BANK_TRANSFER_FAILED = "uvc_bank_transfer_failed", _(
        "The transfer to receiver bank account has failed."
    )
    UVC_BANK_TRANSFER_COMPLETED = "uvc_bank_transfer_completed", _(
        "The transfer to receiver bank account has completed."
    )


class TransactionEventType(ChoiceCharEnum):
    # UVC: unverified customer, VC: verified customer
    SENDER_NOT_STARTED = "sender_not_started", _("Not started")
    SENDER_UVC_BANK_TRANSFER_CREATED = "sender_uvc_bank_transfer_created", _(
        "A transfer has been created from sender bank."
    )
    SENDER_UVC_BANK_TRANSFER_FAILED = "sender_uvc_bank_transfer_failed", _(
        "The transfer from sender bank account has failed."
    )
    SENDER_UVC_BANK_TRANSFER_COMPLETED = (
        "sender_uvc_bank_transfer_completed",
        _("The transfer from sender bank account has completed."),
    )
    SENDER_UVC_BANK_TRANSFER_CANCELLED = (
        "sender_uvc_bank_transfer_cancelled",
        _("The transfer from sender bank account has cancelled."),
    )
    SENDER_VC_BALANCE_TRANSFER_CREATED = "sender_vc_bank_transfer_created", _(
        "A transfer has been created from sender's Loqal balance."
    )
    SENDER_VC_BANK_TRANSFER_CREATED = "sender_vc_bank_transfer_created", _(
        "A transfer has been created from sender bank account."
    )
    SENDER_VC_BANK_TRANSFER_CREATION_FAILED = (
        "sender_vc_bank_transfer_creation_failed",
        _("The transfer creation from sender bank account has failed."),
    )
    SENDER_VC_BANK_TRANSFER_CANCELLED = "sender_vc_bank_transfer_failed", _(
        "The transfer from sender bank account has cancelled."
    )
    SENDER_VC_BANK_TRANSFER_FAILED = "sender_vc_bank_transfer_failed", _(
        "The transfer from sender bank account has failed."
    )
    SENDER_VC_BANK_TRANSFER_COMPLETED = "sender_vc_bank_transfer_completed", _(
        "The transfer from sender bank account has completed."
    )
    SENDER_VC_FROM_BALANCE_TRANSFER_CREATED = (
        "sender_vc_from_balance_transfer_created",
        _("A transfer has been created from sender's Loqal balance."),
    )
    SENDER_VC_FROM_BALANCE_TRANSFER_CANCELLED = (
        "sender_vc_from_balance_transfer_cancelled",
        _("The transfer from sender's Loqal balance has cancelled."),
    )
    SENDER_VC_FROM_BALANCE_TRANSFER_FAILED = (
        "sender_vc_from_balance_transfer_failed",
        _("The transfer from sender's Loqal balance has failed."),
    )
    SENDER_VC_FROM_BALANCE_TRANSFER_COMPLETED = (
        "sender_vc_from_balance_transfer_completed",
        _("The transfer has completed to sender's Loqal balance."),
    )
    SENDER_VC_TO_BALANCE_TRANSFER_CANCELLED = (
        "sender_vc_to_balance_transfer_cancelled",
        _("The transfer to sender's Loqal balance has cancelled."),
    )
    SENDER_VC_TO_BALANCE_TRANSFER_FAILED = (
        "sender_vc_to_balance_transfer_failed",
        _("The transfer to sender's Loqal balance has failed."),
    )
    # UVC: unverified customer, VC: verified customer
    RECEIVER_NOT_STARTED = "receiver_not_started", _("Not started")
    RECEIVER_VC_TO_BALANCE_TRANSFER_CREATED = (
        "receiver_vc_to_balance_transfer_created",
        _("A transfer has been created to receiver's Loqal balance."),
    )
    RECEIVER_VC_TO_BALANCE_TRANSFER_CANCELLED = (
        "receiver_vc_to_balance_transfer_cancelled",
        _("The transfer to receiver's Loqal balance has cancelled."),
    )
    RECEIVER_VC_TO_BALANCE_TRANSFER_FAILED = (
        "receiver_vc_to_balance_transfer_failed",
        _("The transfer to receiver's Loqal balance has failed."),
    )
    RECEIVER_VC_TO_BALANCE_TRANSFER_COMPLETED = (
        "receiver_vc_to_balance_transfer_completed",
        _("The transfer to receiver's Loqal balance has completed."),
    )
    RECEIVER_VC_FROM_BALANCE_TRANSFER_CREATED = (
        "receiver_vc_from_balance_transfer_created",
        _("A transfer has been created from receiver's Loqal balance to bank account."),
    )
    RECEIVER_VC_FROM_BALANCE_TRANSFER_CANCELLED = (
        "receiver_vc_from_balance_transfer_cancelled",
        _("The transfer from receiver's Loqal balance has cancelled."),
    )
    RECEIVER_VC_FROM_BALANCE_TRANSFER_FAILED = (
        "receiver_vc_from_balance_transfer_failed",
        _("The transfer from receiver's Loqal balance has failed."),
    )
    RECEIVER_VC_BANK_TRANSFER_CREATED = "receiver_vc_bank_transfer_created", _(
        "A transfer has been created from receiver's Loqal balance to bank account."
    )
    RECEIVER_VC_BANK_TRANSFER_CREATION_FAILED = (
        "vc_bank_transfer_creation_failed",
        _("The transfer from from receiver's Loqal balance to bank account has failed"),
    )
    RECEIVER_VC_BANK_TRANSFER_CANCELLED = (
        "receiver_vc_bank_transfer_cancelled",
        _("The transfer from receiver's Loqal balance to bank account has cancelled."),
    )
    RECEIVER_VC_BANK_TRANSFER_FAILED = "receiver_vc_bank_transfer_failed", _(
        "The transfer from receiver's Loqal balance to bank account has failed."
    )
    RECEIVER_VC_BANK_TRANSFER_COMPLETED = (
        "receiver_vc_bank_transfer_completed",
        _("The transfer from receiver's Loqal balance to bank account has completed."),
    )
    RECEIVER_UVC_BANK_TRANSFER_CREATED = (
        "receiver_uvc_bank_transfer_created",
        _("A transfer has been created to receiver bank account."),
    )
    RECEIVER_UVC_BANK_TRANSFER_CANCELLED = (
        "receiver_uvc_bank_transfer_cancelled",
        _("The transfer to receiver bank account has cancelled."),
    )
    RECEIVER_UVC_BANK_TRANSFER_FAILED = "receiver_uvc_bank_transfer_failed", _(
        "The transfer to receiver bank account has failed."
    )
    RECEIVER_UVC_BANK_TRANSFER_COMPLETED = (
        "receiver_uvc_bank_transfer_completed",
        _("The transfer to receiver bank account has completed."),
    )


class PaymentStatus(ChoiceEnum):
    CAPTURED = 0, _("Captured")
    IN_PROGRESS = 1, _("In Progress")
    FAILED = 2, _("Failed")
    CANCELLED = 3, _("Cancelled")


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
    FAILED = 3, _("Refund Failed")


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


class DisputeStatus(ChoiceCharEnum):
    REVIEW_WAITING = "review_waiting", _("Waiting for review")
    INTERNAL_REVIEW = "internal_review", _("Internal Review")
    BANK_REVIEW = "bank_review", _("Bank Review")
    MERCHANT_REVIEW = "merchant_review", _("Merchany Review")
    CHARGEBACK_ACCEPTED = "chargeback_accepted", _("Chargeback Accepted")
    CHARGEBACK_REJECTED = "chargeback_rejected", _("Chargeback Rejected")


class DisputeType(ChoiceCharEnum):
    CHARGEBACK = "chargeback", _("Chargeback")
    FRAUD = "fraud", _("Fraud")
    RETRIEVAL = "retrieval", _("Retrieval")


class DisputeReasonType(ChoiceCharEnum):
    MONEY_NOT_REACHED = "money_not_reached", _(
        "Money has not reached the merchant"
    )
    PAID_TWICE = "paid_twice", _("Paid twice for the order")
    MORE_DETAILS_REQUIRED = "more_details_required", _(
        "I require more details"
    )
    DID_NOT_PERFORM = "did_not_perform", _(
        "I did not perform this transaction"
    )
    FRAUDULENT_TRANSACTION = "fraudulent_transaction", _(
        "This transaction is fraudulent"
    )
    TRANSACTION_EXECUTED_ACCIDENTLY = "transaction_executed_accidently", _(
        "Transaction was executed by accident"
    )
    OTHER = "other", _("Other issues")


class DisputeReasonTypeMap:
    money_not_reached = DisputeType.CHARGEBACK
    paid_twice = DisputeType.CHARGEBACK
    more_details_required = DisputeType.RETRIEVAL
    did_not_perform = DisputeType.FRAUD
    fraudulent_transaction = DisputeType.FRAUD
    transaction_executed_accidently = DisputeType.CHARGEBACK
    other = DisputeType.RETRIEVAL
