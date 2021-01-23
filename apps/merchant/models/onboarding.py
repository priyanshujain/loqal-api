from django.db import models
from django.utils.translation import gettext as _

from apps.account.models import MerchantAccount
from apps.box.models import BoxFile
from apps.merchant.options import (BeneficialOwnerStatus, BusinessDocumentType,
                                   BusinessTypes, IndividualDocumentType,
                                   VerificationDocumentStatus)
from db.models import AbstractBaseModel
from db.models.fields import ChoiceCharEnumField

__all__ = (
    "IncorporationDetails",
    "ControllerDetails",
    "BeneficialOwner",
    "IncorporationVerificationDocument",
    "ControllerVerificationDocument",
    "OwnerVerificationDocument",
)


class VerificationDocumentBase(AbstractBaseModel):
    all_failure_reasons = models.JSONField(default=dict)
    failure_reason = models.CharField(max_length=128, blank=True)
    document_type = ChoiceCharEnumField(
        max_length=32,
        default=IndividualDocumentType.NOT_APPLICABLE,
        enum_type=IndividualDocumentType,
    )
    document_file = models.ForeignKey(
        BoxFile, on_delete=models.DO_NOTHING, blank=True, null=True
    )
    status = ChoiceCharEnumField(
        max_length=128,
        enum_type=VerificationDocumentStatus,
        default=VerificationDocumentStatus.NOT_APPLICABLE,
        help_text=_("Status for the verification document with dwolla."),
    )
    dwolla_id = models.CharField(max_length=64, blank=True)

    def update_status(self, status, save=True):
        self.status = status
        if save:
            self.save()

    def add_dwolla_id(self, dwolla_id, save=True):
        self.dwolla_id = dwolla_id
        self.status = VerificationDocumentStatus.PENDING_REVIEW
        if save:
            self.save()

    def add_failure_reason(
        self, failure_reason, all_failure_reasons, save=True
    ):
        self.status = VerificationDocumentStatus.FAILED
        self.failure_reason = failure_reason
        self.all_failure_reasons = all_failure_reasons
        if save:
            self.save()

    class Meta:
        abstract = True


class IncorporationDetails(AbstractBaseModel):
    merchant = models.OneToOneField(
        MerchantAccount,
        related_name="incorporation_details",
        on_delete=models.CASCADE,
    )
    legal_business_name = models.CharField(max_length=512)
    ein_number = models.CharField(
        max_length=11, blank=True, null=True, default=None, unique=True
    )
    registered_address = models.JSONField()
    business_type = ChoiceCharEnumField(max_length=32, enum_type=BusinessTypes)
    business_classification = models.CharField(max_length=64)
    business_classification_id = models.CharField(max_length=64)
    industry_classification = models.CharField(max_length=64)
    industry_classification_id = models.CharField(max_length=64)
    verification_document_required = models.BooleanField(default=False)

    def update_verification_document_required(self, required, save=True):
        self.verification_document_required = required
        self.verification_document_status = VerificationDocumentStatus.PENDING
        if save:
            self.save()

    class Meta:
        db_table = "merchant_onboarding_incorporation_details"


class IncorporationVerificationDocument(VerificationDocumentBase):
    incorporation_details = models.ForeignKey(
        IncorporationDetails,
        related_name="documents",
        on_delete=models.CASCADE,
    )
    document_type = ChoiceCharEnumField(
        max_length=32,
        default=BusinessDocumentType.NOT_APPLICABLE,
        enum_type=BusinessDocumentType,
    )

    class Meta:
        db_table = "inc_details_verification_document"


class OnboardingConsent(AbstractBaseModel):
    merchant = models.ForeignKey(
        MerchantAccount,
        related_name="onboarding_consents",
        on_delete=models.CASCADE,
    )
    full_name = models.CharField(max_length=256)
    ip_address = models.GenericIPAddressField()

    class Meta:
        db_table = "merchant_onboarding_consent"


class IndividualBase(AbstractBaseModel):
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    is_us_citizen = models.BooleanField()
    ssn = models.CharField(max_length=11, blank=True)
    dob = models.DateField()
    # TODO: Create a json schema validator for address
    address = models.JSONField()
    # TODO: Apply an enum validator for country code
    passport_country = models.CharField(max_length=2, blank=True)
    passport_number = models.CharField(max_length=32, blank=True)

    class Meta:
        abstract = True


class ControllerDetails(IndividualBase):
    merchant = models.OneToOneField(
        MerchantAccount,
        related_name="controller_details",
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=256, blank=True)
    verification_document_required = models.BooleanField(default=False)

    def update_verification_document_required(self, required, save=True):
        self.verification_document_required = required
        self.verification_document_status = VerificationDocumentStatus.PENDING
        if save:
            self.save()

    class Meta:
        db_table = "merchant_onboarding_controller_details"


class BeneficialOwner(IndividualBase):
    merchant = models.ForeignKey(
        MerchantAccount,
        related_name="beneficial_owners",
        on_delete=models.CASCADE,
    )
    dwolla_id = models.CharField(max_length=64, blank=True)
    status = ChoiceCharEnumField(
        max_length=128,
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
        if save:
            self.save()

    class Meta:
        db_table = "merchant_onboarding_beneficial_owner"


class OwnerVerificationDocument(VerificationDocumentBase):
    owner = models.ForeignKey(
        BeneficialOwner, related_name="documents", on_delete=models.CASCADE
    )

    class Meta:
        db_table = "owner_verification_document"


class ControllerVerificationDocument(VerificationDocumentBase):
    controller = models.ForeignKey(
        ControllerDetails, related_name="documents", on_delete=models.CASCADE
    )

    class Meta:
        db_table = "controller_verification_document"
