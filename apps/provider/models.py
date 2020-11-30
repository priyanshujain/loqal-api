import uuid

from django.db import models
from django.utils.timezone import now

from apps.account.models import Account
from apps.provider.options import PaymentAccountStatus
from db.models.abstract import AbstractBase
from db.postgres.fields import JSONField
from utils.shortcuts import upload_to


class PaymentProvider(AbstractBase):
    provider_slug = models.CharField(max_length=255, unique=True)
    display_name = models.CharField(max_length=255)
    website = models.URLField(max_length=255, unique=True)
    logo = models.FileField(
        upload_to=upload_to("paymentproviders/logo/", "image"), blank=True
    )

    class Meta:
        db_table = "payment_provider"


class PaymentProviderCred(AbstractBase):
    provider = models.ForeignKey(PaymentProvider, on_delete=models.CASCADE)
    api_environment = models.CharField(max_length=255)
    api_password = models.CharField(max_length=255, blank=True)
    api_key = models.CharField(max_length=255, blank=True)
    api_login_id = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "payment_provider_cred"
        unique_together = (
            "provider",
            "api_environment",
        )


class PaymentProviderAuth(AbstractBase):
    provider = models.OneToOneField(PaymentProvider, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=1024)
    expires_at = models.DateTimeField()

    class Meta:
        db_table = "payment_provider_auth"
        unique_together = (
            "provider",
            "auth_token",
            "expires_at",
        )

    @property
    def is_expired(self):
        """Check if auth_token is expired"""
        return self.expires_at < now()


class TermsDocument(AbstractBase):
    provider = models.ForeignKey(
        PaymentProvider, on_delete=models.CASCADE, editable=False
    )
    document_type = models.CharField(max_length=255, editable=False)
    document_file = JSONField()
    is_active = models.BooleanField(default=True)
    country = models.CharField(max_length=2, editable=False)

    class Meta:
        db_table = "terms_document"


class PaymentAccount(AbstractBase):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    provider = models.ForeignKey(PaymentProvider, on_delete=models.CASCADE)
    correlation_id = models.UUIDField(
        primary_key=False, default=uuid.uuid4, editable=False
    )
    status = models.CharField(
        max_length=255, default=PaymentAccountStatus.TERMS_ACCEPTED
    )

    def update_status_onboarding_data_sent(self):
        self.status = PaymentAccountStatus.ONBOARDING_DATA_SENT
        self.save()

    def approve_account(self):
        self.status = PaymentAccountStatus.KEYS_PROVIDED
        self.save()

    class Meta:
        db_table = "payment_account"
        unique_together = (
            "account",
            "provider",
        )


class PaymentAccountOpeningConsent(AbstractBase):
    payment_account = models.ForeignKey(
        PaymentAccount, on_delete=models.CASCADE
    )
    user_agent = models.TextField()
    ip = models.GenericIPAddressField()
    consent_timestamp = models.BigIntegerField()
    term = models.ForeignKey(TermsDocument, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "payment_account_opening_consent"


class PaymentAccountOpeningCreds(AbstractBase):
    payment_account = models.OneToOneField(
        PaymentAccount,
        related_name="account_opening_creds",
        on_delete=models.CASCADE,
    )
    api_key = models.TextField(blank=True)
    account_number = models.CharField(max_length=64, blank=True)

    class Meta:
        db_table = "payment_account_opening_creds"


class ProviderUpdateWebhook(AbstractBase):
    provider = models.ForeignKey(PaymentProvider, on_delete=models.CASCADE)
    webhook_secret = models.CharField(max_length=256)
    webhook_id = models.CharField(max_length=256, unique=True)
    api_key = models.CharField(max_length=256)

    class Meta:
        db_table = "provider_update_webhook"
