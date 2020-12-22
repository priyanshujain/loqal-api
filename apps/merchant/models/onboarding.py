from django.db import models
from django.utils.translation import gettext as _

from apps.account.models import MerchantAccount
from apps.box.models import BoxFile
from apps.merchant.options import (BeneficialOwnerStatus, BusinessDocumentType,
                                   BusinessTypes, IndividualDocumentType,
                                   VerificationDocumentStatus)
from db.models import AbstractBaseModel
from db.models.fields import ChoiceCharEnumField, ChoiceEnumField
from utils.shortcuts import generate_uuid_hex

__all__ = (
    "IncorporationConsent",
    "IncorporationDetails",
    "ControllerDetails",
    "BeneficialOwner",
)


class IncorporationDetails(AbstractBaseModel):
    merchant = models.OneToOneField(MerchantAccount, on_delete=models.CASCADE)
    legal_business_name = models.CharField(max_length=512)
    ein_number = models.CharField(max_length=11, blank=True)
    registered_address = models.JSONField()
    business_type = ChoiceCharEnumField(max_length=32, enum_type=BusinessTypes)
    business_classification = models.CharField(max_length=64)
    business_classification_id = models.CharField(max_length=64)
    verification_document_required = models.BooleanField(default=False)
    verification_document_type = ChoiceCharEnumField(
        max_length=32, blank=True, enum_type=BusinessDocumentType
    )
    verification_document_file = models.ForeignKey(
        BoxFile, on_delete=models.DO_NOTHING, blank=True, null=True
    )
    verification_document_status = ChoiceEnumField(
        enum_type=VerificationDocumentStatus,
        default=VerificationDocumentStatus.NOT_APPLICABLE,
        help_text=_("Status for the verification document with dwolla."),
    )
    dwolla_document_id = models.CharField(max_length=64, blank=True)

    def update_verification_document_status(self, status, save=True):
        self.verification_document_status = status
        if save:
            self.save()

    def update_verification_document_required(self, required, save=True):
        self.verification_document_required = required
        self.verification_document_status = VerificationDocumentStatus.PENDING
        if save:
            self.save()

    def add_dwolla_document_id(self, dwolla_id, save=True):
        self.dwolla_document_id = dwolla_id
        if save:
            self.save()

    class Meta:
        db_table = "merchant_onboarding_incorporation_details"


class IncorporationConsent(AbstractBaseModel):
    merchant = models.ForeignKey(MerchantAccount, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    ip_address = models.GenericIPAddressField()
    dwolla_correlation_id = models.CharField(
        max_length=40, default=generate_uuid_hex, editable=False, unique=True
    )

    class Meta:
        db_table = "merchant_onboarding_incorporation_consent"


class IndividualBase(AbstractBaseModel):
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    is_us_citizen = models.BooleanField()
    ssn = models.CharField(max_length=9, blank=True)
    dob = models.DateField()
    # TODO: Create a json schema validator for address
    address = models.JSONField()
    # TODO: Apply an enum validator for country code
    passport_country = models.CharField(max_length=2, blank=True)
    passport_number = models.CharField(max_length=32, blank=True)
    verification_document_type = ChoiceCharEnumField(
        max_length=32, blank=True, enum_type=IndividualDocumentType
    )
    verification_document_file = models.ForeignKey(
        BoxFile, on_delete=models.DO_NOTHING, blank=True, null=True
    )
    verification_document_status = ChoiceEnumField(
        enum_type=VerificationDocumentStatus,
        default=VerificationDocumentStatus.NOT_APPLICABLE,
        help_text=_("Status for the verification document with dwolla."),
    )
    dwolla_document_id = models.CharField(max_length=64, blank=True)

    def update_verification_document_status(self, status, save=True):
        self.verification_document_status = status
        if save:
            self.save()

    def add_dwolla_document_id(self, dwolla_id, save=True):
        self.dwolla_document_id = dwolla_id
        if save:
            self.save()

    class Meta:
        abstract = True


class ControllerDetails(IndividualBase):
    merchant = models.OneToOneField(MerchantAccount, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    verification_document_required = models.BooleanField(default=False)

    def update_verification_document_required(self, required, save=True):
        self.verification_document_required = required
        self.verification_document_status = VerificationDocumentStatus.PENDING
        if save:
            self.save()

    class Meta:
        db_table = "merchant_onboarding_controller_details"


class BeneficialOwner(IndividualBase):
    merchant = models.ForeignKey(MerchantAccount, on_delete=models.CASCADE)
    dwolla_id = models.CharField(max_length=64, blank=True)
    status = ChoiceEnumField(
        enum_type=BeneficialOwnerStatus,
        default=BeneficialOwnerStatus.PENDING,
        help_text=_("Status for the beneficial owner with dwolla."),
    )

    def add_dwolla_id(self, dwolla_id, save=True):
        """
        add dwolla id
        """
        self.dwolla_id = dwolla_id
        if save:
            self.save()

    def update_status(self, status, save=True):
        """
        update status
        """
        self.status = status
        if (
            status == BeneficialOwnerStatus.DOCUMENT_PENDING
            and not self.verification_document_file
        ):
            self.verification_document_status = (
                VerificationDocumentStatus.PENDING
            )
        if save:
            self.save()

    class Meta:
        db_table = "merchant_onboarding_beneficial_owner"
