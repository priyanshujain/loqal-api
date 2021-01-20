import uuid
from re import T

from django.db import models
from django.utils.translation import gettext as _
from rest_framework.fields import ModelField

from apps.account.options import (ConsumerAccountStatus,
                                  MerchantAccountCerficationStatus,
                                  MerchantAccountStatus)
from apps.box.models import BoxFile
from apps.user.models import User
from db.models.abstract import AbstractBaseModel, BaseModel
from db.models.fields import ChoiceEnumField
from utils.shortcuts import generate_uuid_hex

__all__ = (
    "Account",
    "FeatureAccess",
    "AccountSettings",
)


class Account(AbstractBaseModel):
    dwolla_correlation_id = models.CharField(
        max_length=40, default=generate_uuid_hex, editable=False, unique=True
    )
    dwolla_id = models.CharField(max_length=64, blank=True)
    is_verified_dwolla_customer = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    zip_code = models.CharField(max_length=5, blank=True)

    def add_dwolla_id(self, dwolla_id):
        """
        docstring
        """
        self.dwolla_id = dwolla_id
        self.save()

    def add_zip_code(self, zip_code):
        """
        docstring
        """
        self.zip_code = zip_code
        self.save()

    class Meta:
        db_table = "account"


class ConsumerAccount(AbstractBaseModel):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(
        max_length=32, default=None, null=True, unique=True
    )
    account_status = ChoiceEnumField(
        enum_type=ConsumerAccountStatus,
        default=ConsumerAccountStatus.UNVERIFIED,
        help_text=_("Status for the consumer account with dwolla."),
    )

    def change_username(self, username, save=True):
        self.username = username
        if save:
            self.save()

    class Meta:
        unique_together = (
            "account",
            "user",
        )
        db_table = "consumer_account"


class MerchantAccount(AbstractBaseModel):
    account = models.OneToOneField(
        Account, on_delete=models.CASCADE, null=True, blank=True
    )
    company_email = models.CharField(max_length=255, blank=True)
    account_status = ChoiceEnumField(
        enum_type=MerchantAccountStatus,
        default=MerchantAccountStatus.PENDING,
        help_text=_("Status for the merchant account with dwolla."),
    )
    is_certification_required = models.BooleanField(default=None, null=True)
    certification_status = ChoiceEnumField(
        enum_type=MerchantAccountCerficationStatus,
        default=MerchantAccountCerficationStatus.PENDING,
        help_text=_(
            "Status for the merchant beneficial owner certified with dwolla."
        ),
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "merchant_account"

    def update_status(self, status, save=True):
        self.account_status = status
        if save:
            self.save()

    def update_certification_status(self, status, save=True):
        self.certification_status = status
        if save:
            self.save()

    def update_certification_required(self, required, save=True):
        self.is_certification_required = required
        if save:
            self.save()

    def deactivate(self, save=True):
        self.is_active = False
        if save:
            self.save()

    def activate(self, save=True):
        self.is_active = True
        if save:
            self.save()


class PaymentAccountOpeningConsent(BaseModel):
    account = models.ForeignKey(
        Account, on_delete=models.DO_NOTHING, editable=False
    )
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, editable=False)
    user_agent = models.TextField(editable=False)
    ip_address = models.GenericIPAddressField(editable=False)
    consent_timestamp = models.BigIntegerField(editable=False)
    payment_term_document = models.ForeignKey(
        BoxFile, on_delete=models.DO_NOTHING, editable=False
    )

    class Meta:
        db_table = "payment_account_opening_consent"
