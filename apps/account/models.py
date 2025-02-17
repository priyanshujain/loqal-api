from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _
from timezone_field import TimeZoneField

from apps.account.options import (AccountCerficationStatus,
                                  ConsumerAccountStatus, DwollaCustomerStatus,
                                  DwollaCustomerVerificationStatus)
from apps.box.models import BoxFile
from db.models.abstract import AbstractBaseModel, BaseModel
from db.models.fields import ChoiceCharEnumField, ChoiceEnumField
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
    dwolla_customer_status = ChoiceCharEnumField(
        max_length=64,
        enum_type=DwollaCustomerStatus,
        default=DwollaCustomerStatus.NOT_SENT,
        help_text=_("Status for the account with dwolla."),
    )
    dwolla_customer_verification_status = ChoiceCharEnumField(
        max_length=64,
        enum_type=DwollaCustomerVerificationStatus,
        default=DwollaCustomerVerificationStatus.NOT_SENT,
        help_text=_("Status for the consumer account with dwolla."),
    )
    is_certification_required = models.BooleanField(default=None, null=True)
    is_reverification_needed = models.BooleanField(default=False)
    certification_status = ChoiceEnumField(
        enum_type=AccountCerficationStatus,
        default=AccountCerficationStatus.PENDING,
        help_text=_(
            "Status for the merchant beneficial owner certified with dwolla."
        ),
    )
    is_verified_dwolla_customer = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    zip_code = models.CharField(max_length=5, blank=True)

    def add_dwolla_id(self, dwolla_id, save=True):
        """
        docstring
        """
        self.dwolla_id = dwolla_id
        if save:
            self.save()

    def update_status(self, status=None, verification_status=None, save=True):
        """
        docstring
        """
        if status:
            self.dwolla_customer_status = status
        if verification_status:
            self.dwolla_customer_verification_status = verification_status
        if not (status or verification_status):
            return
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

    def set_reverification_needed(self, save=False):
        self.is_reverification_needed = True
        if save:
            self.save()

    def add_zip_code(self, zip_code, save=True):
        """
        docstring
        """
        self.zip_code = zip_code
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

    class Meta:
        db_table = "account"


class ConsumerAccount(AbstractBaseModel):
    account = models.OneToOneField(
        Account, related_name="consumer", on_delete=models.CASCADE
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="consumer_account",
    )
    username = models.CharField(
        max_length=32, default=None, null=True, unique=True
    )
    account_status = ChoiceEnumField(
        enum_type=ConsumerAccountStatus,
        default=ConsumerAccountStatus.UNVERIFIED,
        help_text=_("Status for the consumer account with dwolla."),
    )
    tz = TimeZoneField(default="Europe/London")

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
        Account,
        related_name="merchant",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    company_email = models.EmailField(max_length=255, blank=True)
    notification_email = models.EmailField(max_length=255, blank=True)
    tz = TimeZoneField(default="US/Eastern")

    class Meta:
        db_table = "merchant_account"

    @property
    def category(self):
        categories = self.categories
        categories = categories.filter(is_primary=True)
        if categories.exists():
            return categories.first()
        else:
            return None

    def update_company_email(self, email, save=True):
        if email != self.company_email:
            self.company_email = email
            if save:
                self.save()

    def update_notification_email(self, email, save=True):
        self.notification_email = email
        if save:
            self.save()


class PaymentAccountOpeningConsent(BaseModel):
    account = models.ForeignKey(
        Account, on_delete=models.DO_NOTHING, editable=False
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, editable=False
    )
    user_agent = models.TextField(editable=False)
    ip_address = models.GenericIPAddressField(editable=False)
    consent_timestamp = models.BigIntegerField(editable=False)
    payment_term_document = models.ForeignKey(
        BoxFile, on_delete=models.DO_NOTHING, null=True, blank=True
    )

    class Meta:
        db_table = "payment_account_opening_consent"

    def add_terms_file(self, boxfile, save=True):
        self.payment_term_document = boxfile
        if save:
            self.save()
