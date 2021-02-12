from django.db import models

from apps.account.models import Account
from db.models.abstract import AbstractBaseModel
from db.models.fields import ChoiceCharEnumField

from .options import (DwollaFundingSourceStatus, MicroDepositStatus,
                      PlaidBankAccountStatus, VerificationProvider,
                      VerificationType)


class BankAccount(AbstractBaseModel):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    plaid_access_token = models.CharField(max_length=255, blank=True)
    plaid_account_id = models.CharField(max_length=255, blank=True)
    account_number_suffix = models.CharField(max_length=4, blank=True)
    name = models.CharField(max_length=64)
    bank_name = models.CharField(max_length=1024)
    bank_logo_base64 = models.TextField(blank=True, null=True, default=None)
    currency = models.CharField(max_length=3, default="USD")
    is_disabled = models.BooleanField(default=False)
    is_primary = models.BooleanField(default=True)
    is_dwolla_removed = models.BooleanField(default=False)
    dwolla_id = models.CharField(max_length=255, blank=True)
    bank_account_type = models.CharField(max_length=32, default="checking")
    dwolla_funding_source_status = ChoiceCharEnumField(
        enum_type=DwollaFundingSourceStatus,
        default=DwollaFundingSourceStatus.NA,
        max_length=32,
    )
    verification_type = ChoiceCharEnumField(
        enum_type=VerificationType,
        default=VerificationType.INSTANT,
        max_length=32,
    )
    micro_deposit_status = ChoiceCharEnumField(
        enum_type=MicroDepositStatus,
        default=MicroDepositStatus.NA,
        max_length=32,
    )
    max_attempts_exceeded = models.BooleanField(default=False)
    verification_provider = ChoiceCharEnumField(
        enum_type=VerificationProvider,
        default=VerificationProvider.PLAID,
        max_length=32,
    )
    plaid_status = ChoiceCharEnumField(
        max_length=32,
        enum_type=PlaidBankAccountStatus,
        default=PlaidBankAccountStatus.PENDING,
    )

    class Meta:
        db_table = "bank_account"

    def add_dwolla_id(self, dwolla_id, status=None, save=True):
        self.dwolla_id = dwolla_id
        if status:
            self.dwolla_funding_source_status = status
        if save:
            self.save()

    def set_dwolla_removed(self):
        self.dwolla_funding_source_status = DwollaFundingSourceStatus.REMOVED
        self.is_dwolla_removed = True
        self.is_primary = False
        self.is_disabled = True
        self.save()

    def set_plaid_verified(self, save=True):
        self.plaid_status = PlaidBankAccountStatus.VERIFIED
        if save:
            self.save()

    def set_plaid_reverification(self, save=True):
        self.plaid_status = PlaidBankAccountStatus.REVERIFICATION_REQUIRED
        if save:
            self.save()

    def is_payment_allowed(self):
        if not self.is_primary:
            return False
        elif self.is_disabled:
            return False
        elif self.is_dwolla_removed:
            return False
        elif (
            self.dwolla_funding_source_status
            != DwollaFundingSourceStatus.VERIFIED
        ):
            return False
        elif self.plaid_status != PlaidBankAccountStatus.VERIFIED:
            return False
        return True

    def set_username_changed(self, save=True):
        self.plaid_status = PlaidBankAccountStatus.USERNAME_CHANGED
        if save:
            self.save()

    def set_micro_deposit_verified(self, save=True):
        self.micro_deposit_status = MicroDepositStatus.VERIFIED
        if save:
            self.save()

    def set_dwolla_verified(self, save=True):
        self.dwolla_funding_source_status = DwollaFundingSourceStatus.VERIFIED
        if save:
            self.save()

    def update_dwolla_status(self, status, save=True):
        self.dwolla_funding_source_status = status
        if save:
            self.save()
