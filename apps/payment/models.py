from django.db import models

from apps.account.models import Account
from apps.beneficiary.models import Beneficiary
from apps.provider.models import PaymentAccount
from apps.provider.options import DEFAULT_CURRENCY
from db.models.abstract import AbstractBase
from db.postgres.fields import JSONField

from .options import PaymentRequestStatuses, TransactionStatus


class RateQuote(AbstractBase):
    payment_account = models.ForeignKey(
        PaymentAccount, on_delete=models.CASCADE
    )
    beneficiary = models.ForeignKey(
        Beneficiary, on_delete=models.DO_NOTHING, null=True, blank=True
    )
    provider_quote_id = models.CharField(max_length=1024)
    fee_value = models.FloatField(default=0.0)
    fee_currency = models.CharField(max_length=3, default="USD")
    rate = models.FloatField()
    expires_at = models.DateTimeField()
    quote_request_time = models.DateTimeField()
    quote_response_time = models.DateTimeField()
    target_amount = models.FloatField()
    rate_type = models.CharField(default="FIXED", max_length=5)
    source_currency = models.CharField(max_length=3)
    target_currency = models.CharField(max_length=3)
    expected_transaction_date = models.DateField()

    class Meta:
        db_table = "rate_quote"


class PaymentRequest(AbstractBase):
    account = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    # TODO: remove null from apps.payment.request bene
    beneficiary = models.ForeignKey(
        Beneficiary, on_delete=models.DO_NOTHING, null=True, blank=True
    )
    target_amount = models.FloatField()
    source_currency = models.CharField(max_length=3)
    ref_document = JSONField(null=True, blank=True)
    payment_reference = models.CharField(max_length=255, blank=True)
    purpose_of_payment = models.CharField(max_length=255)
    purpose_of_payment_code = models.CharField(max_length=512, blank=True)
    status = models.CharField(
        max_length=128, default=PaymentRequestStatuses.DEFAULT
    )

    def set_status(self, status):
        self.status = status
        self.save()

    def set_approval_pending(self):
        self.set_status(PaymentRequestStatuses.APPROVAL_PENDING)

    def set_executed(self):
        self.set_status(PaymentRequestStatuses.EXECUTED)

    def set_rejected(self):
        self.status = PaymentRequestStatuses.REJECTED
        self.save()

    class Meta:
        db_table = "payment_request"


class Transaction(AbstractBase):
    account = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    # TODO: remove null from apps.payment.request bene
    payment_request = models.OneToOneField(
        PaymentRequest, on_delete=models.CASCADE
    )
    quote = models.ForeignKey(RateQuote, on_delete=models.CASCADE)
    provider_transaction_id = models.CharField(max_length=255)
    fee_value = models.FloatField(default=0.0)
    fee_currency = models.CharField(max_length=3, default=DEFAULT_CURRENCY)
    status = models.CharField(
        max_length=128, default=TransactionStatus.IN_PROCESS
    )
    transaction_confirmation_file = JSONField(null=True, blank=True)

    def add_transaction_confirmation(self, file_data):
        self.transaction_confirmation_file = file_data
        self.save()

    def processed(self):
        self.status = TransactionStatus.PROCESSED
        self.save()

    class Meta:
        db_table = "transaction"


class TransactionCancellationRequest(AbstractBase):
    account = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    transaction = models.ForeignKey(Transaction, on_delete=models.DO_NOTHING)
    reason = models.TextField()

    class Meta:
        db_table = "transaction_cancellation_request"
