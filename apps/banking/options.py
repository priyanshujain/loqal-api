from django.utils.translation import gettext as _

from db.models.fields import ChoiceCharEnum


class PlaidBankAccountStatus(ChoiceCharEnum):
    NOT_APPLICABLE = "not_applicable", _("Not Applicable")
    PENDING = "pending", _("Pending")
    VERIFIED = "verified", _("Verified")
    REVERIFICATION_REQUIRED = "re_verification_required", _(
        "Reverification Required"
    )
    SUSPENDED = "suspended", _("Suspended")
    USERNAME_CHANGED = "username_changed", _("Username Changed")


class DwollaFundingSourceStatus(ChoiceCharEnum):
    NA = "na", _("NA")
    ADDED = "added", _("Added")
    REMOVED = "removed", _("Removed")
    VERIFIED = "verified", _("Verified")
    UNVERIFIED = "unverified", _("Unverified")
    NEGATIVE_BALANCE = "negative_balance", _("Negative Balance")
    UPDATED = "updated", _("Updated")


class VerificationProvider(ChoiceCharEnum):
    DWOLLA = "dwolla", _("Dwolla")
    PLAID = "plaid", _("Plaid")


class VerificationType(ChoiceCharEnum):
    MICRO_DEPOSIT = "micro_deposit", _("Micro Deposit")
    INSTANT = "instant", _("Instant Verification")


class MicroDepositStatus(ChoiceCharEnum):
    NA = "na", _("NA")
    PENDING = "pending", _("Pending")
    AWAITING_VERIFICATION = "awaiting_verification", _("Awaiting Verification")
    VERIFIED = "verified", _("Verified")
    FAILED = "failed", _("Failed")
