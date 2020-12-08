import uuid

from django.db import models
from django.utils.timezone import now

from apps.account.models import Account
from apps.provider.options import PaymentAccountStatus
from db.models.abstract import AbstractBaseModel
from db.postgres.fields import JSONField
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
    api_password = models.CharField(max_length=255, blank=True)
    api_key = models.CharField(max_length=255, blank=True)
    api_login_id = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "payment_provider_cred"
        unique_together = (
            "provider",
            "api_environment",
        )


class PaymentProviderAuth(AbstractBaseModel):
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


class TermsDocument(AbstractBaseModel):
    provider = models.ForeignKey(
        PaymentProvider, on_delete=models.CASCADE, editable=False
    )
    document_type = models.CharField(max_length=255, editable=False)
    document_file = JSONField()
    is_active = models.BooleanField(default=True)
    country = models.CharField(max_length=2, editable=False)

    class Meta:
        db_table = "terms_document"
