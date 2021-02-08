import uuid
from typing import Text

from django.db import models
from django.utils.timezone import now

from apps.account.models import Account
from apps.provider.options import PaymentAccountStatus
from db.models.abstract import AbstractBaseModel
from db.models.fields import EncryptedCharField
from utils.shortcuts import upload_to


class PaymentProvider(AbstractBaseModel):
    provider_slug = models.CharField(max_length=255, unique=True)
    display_name = models.CharField(max_length=255)
    website = models.URLField(max_length=255, unique=True)
    logo = models.FileField(
        upload_to=upload_to("paymentproviders/logo/", "image"), blank=True
    )

    class Meta:
        db_table = "payment_provider"


class PaymentProviderCred(AbstractBaseModel):
    provider = models.ForeignKey(PaymentProvider, on_delete=models.CASCADE)
    api_environment = models.CharField(max_length=255)
    api_password = EncryptedCharField(max_length=255, blank=True)
    api_key = EncryptedCharField(max_length=255, blank=True)
    api_login_id = EncryptedCharField(max_length=255, blank=True)

    class Meta:
        db_table = "payment_provider_cred"
        unique_together = (
            "provider",
            "api_environment",
        )


class PaymentProviderAuth(AbstractBaseModel):
    provider = models.OneToOneField(PaymentProvider, on_delete=models.CASCADE)
    auth_token = EncryptedCharField(max_length=1024)
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


class TermsDocument(AbstractBaseModel):
    provider = models.ForeignKey(
        PaymentProvider, on_delete=models.CASCADE, editable=False
    )
    document_type = models.CharField(max_length=255, editable=False)
    document_file = models.JSONField()
    is_active = models.BooleanField(default=True)
    country = models.CharField(max_length=2, editable=False)

    class Meta:
        db_table = "terms_document"


class ProviderWebhook(AbstractBaseModel):
    provider = models.ForeignKey(PaymentProvider, on_delete=models.CASCADE)
    webhook_secret = models.CharField(max_length=256)
    webhook_id = models.CharField(max_length=256, unique=True)
    dwolla_id = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "provider_webhook"

    def add_dwolla_id(self, dwolla_id, save=True):
        """
        docstring
        """
        self.dwolla_id = dwolla_id
        if save:
            self.save()

    def deactivate(self, save=True):
        self.is_active = False
        if save:
            self.save()


class ProviderWebhookEvent(AbstractBaseModel):
    webhook = models.ForeignKey(ProviderWebhook, on_delete=models.CASCADE)
    event_payload = models.JSONField(default=dict, null=True)
    dwolla_id = models.CharField(max_length=255, blank=True)
    is_processed = models.BooleanField(default=False)
    topic = models.CharField(max_length=255, blank=True)
    target_resource_dwolla_id = models.CharField(
        max_length=255, blank=True, null=True, default=None, db_index=True
    )
    event_timestamp = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "provider_webhook_event"

    def mark_processed(self, save=True):
        self.is_processed = True
        if save:
            self.save()
