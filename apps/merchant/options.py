from django.utils.translation import gettext as _

from db.models.fields import ChoiceCharEnum, ChoiceEnum

__all__ = (
    "BusinessTypes",
    "MemberType",
    "FeatureAcessTypes",
    "AllowedFeatureAcessTypes",
    "BusinessDayType",
    "CleaningFrequencyType",
)


class BusinessTypes(ChoiceCharEnum):
    SOLE_PROPRIETORSHIP = "sole_proprietorship", _("Sole Proprietorship")
    LLC = "llc", _("LLC")
    CORPORATION = "corporation", _("Corporation")
    PARTNERSHIP = "partnership", _("Partnership")


class MemberType(ChoiceEnum):
    VIEW_ONLY = "view_only", _("View Only")
    APPROVER_ONLY = "approver_only", _("Approver Only")
    CREATOR_ONLY = "creator_only", _("Creator Only")
    STANDARD_USER = "standard_user", _("Standard User")
    ADMINISTRATOR = "administrator", _("Administrator")


class FeatureAcessTypes(ChoiceEnum):
    CREATE = "CREATE", _("Create")
    UPDATE = "UPDATE", _("Update")
    VIEW = "VIEW", _("View")
    PARTIAL_VIEW = "PARTIAL_VIEW", _("Partial View")
    DELETE = "DELETE", _("Delete")


class AllowedFeatureAcessTypes:
    PAYMENT_REQUESTS = ["CREATE", "VIEW"]
    PAYMENT_HISTORY = ["PARTIAL_VIEW", "VIEW"]
    SETTLEMENTS = ["VIEW", "PARTIAL_VIEW"]
    REFUNDS = ["CREATE", "VIEW", "PARTIAL_VIEW"]
    DISPUTES = ["PARTIAL_VIEW", "VIEW"]
    CUSTOMERS = ["PARTIAL_VIEW", "VIEW"]
    BANK_ACCOUNTS = ["CREATE", "VIEW", "DELETE"]
    QR_CODES = ["CREATE", "UPDATE", "VIEW"]
    STORE_PROFILE = ["UPDATE", "VIEW"]
    TEAM_MANAGEMENT = ["CREATE", "UPDATE", "VIEW", "DELETE"]


class BeneficialOwnerStatus(ChoiceCharEnum):
    PENDING = "pending", _("Pending")
    VERIFIED = "verified", _("Verified")
    DOCUMENT_PENDING = "document_pending", _("Document Pending")
    INCOMPLETE = "incomplete", _("Incomplete")


class VerificationDocumentStatus(ChoiceCharEnum):
    PENDING = "pending", _("Pending")
    VERIFIED = "verified", _("Verified")
    NOT_APPLICABLE = "not_applicable", _("Not Applicable")
    UPLOADED = "uploaded", _("Uploaded")
    PENDING_REVIEW = "pending_review", _("Pending for review")
    FAILED = "failed", _("Failed")


class IndividualDocumentType(ChoiceCharEnum):
    DRIVER_LICENSE = "driver_license", _("Driver’s License")
    US_PASSPORT = "us_passport", _("US Passport")
    FOREIGN_PASSPORT = "foreign_passport", _("Foreign Passport")
    US_VISA = "us_visa", _("US Visa")
    FEAC = "employment_authorization_card", _(
        "Federal Employment Authorization Card"
    )
    NOT_APPLICABLE = "not_applicable", _("Not Applicable")


class BusinessDocumentType(ChoiceCharEnum):
    EIN_LETTER = "ein_letter", _("EIN Letter")
    BUSINESS_LICENSE = "business_license", _("Business License")
    DRIVER_LICENSE = "driver_license", _("Driver’s License")
    US_PASSPORT = "us_passport", _("US Passport")
    NOT_APPLICABLE = "not_applicable", _("Not Applicable")


class BusinessDayType(ChoiceCharEnum):
    MONDAY = "mon", _("Monday")
    TUESDAY = "tue", _("Tuesday")
    WEDNESDAY = "wed", _("Wednesday")
    THURSDAY = "thu", _("Thursday")
    FRIDAY = "fri", _("Friday")
    SATURDAY = "sat", _("Saturday")
    SUNDAY = "sun", _("Sunday")


class CleaningFrequencyType(ChoiceCharEnum):
    DAILY = "daily", _("Daily")
    TWICE_A_DAY = "twice_a_day", _("Twice a day")
    EVERY_FOUR_HOURS = "every_four_hours", _("Every 4 hours")
    NOT_PROVIDED = "not_provided", _("Not provided")
