from apps.provider.options import DEFAULT_CURRENCY
from utils.choices import Choices

FACILITATION_FEES_PERCENTAGE = 1.5
FACILITATION_FEES_CURRENCY = DEFAULT_CURRENCY


class TransactionStatus(Choices):
    NOT_SENT = "NOT_SENT"
    PENDING = "PENDING"
    PROCESSED = "PROCESSED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
