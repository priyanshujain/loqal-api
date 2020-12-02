from utils.choices import Choices


class PaymentRequestStatuses(Choices):
    APPROVAL_PENDING = "APPROVAL_PENDING"
    REJECTED = "REJECTED"
    EXECUTED = "EXECUTED"
    DEFAULT = "DEFAULT"


class TransactionStatus(Choices):
    IN_PROCESS = "IN_PROCESS"
    PROCESSED = "PROCESSED"
