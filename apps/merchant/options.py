from django.utils.translation import gettext as _

from db.models.fields import ChoiceCharEnum, ChoiceEnum

__all__ = (
    "BusinessTypes",
    "MemberType",
    "FeatureAcessTypes",
    "AllowedFeatureAcessTypes",
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
    CREATE = "create", _("Create")
    UPDATE = "update", _("Update")
    VIEW = "view", _("View")
    APPROVE = "approve", _("Approve")
    DELETE = "delete", _("Delete")


class AllowedFeatureAcessTypes:
    TEAM_AND_ROLES = ["CREATE", "UPDATE", "VIEW", "DELETE"]
    BENEFICIARIES = [
        "CREATE",
        "UPDATE",
        "VIEW",
        "APPROVE",
        "DELETE",
    ]
    TRANSACTIONS = [
        "CREATE",
        "UPDATE",
        "VIEW",
        "APPROVE",
    ]
    DIRECT_DEBIT_ACCOUNTS = [
        "CREATE",
        "UPDATE",
        "VIEW",
    ]
    SETTINGS = [
        "CREATE",
        "UPDATE",
        "VIEW",
    ]


class BeneficialOwnerStatus(ChoiceEnum):
    PENDING = 0, _("Pending")
    VERIFIED = 1, _("Verified")
    DOCUMENT_PENDING = 2, _("Document Pending")
    INCOMPLETE = 3, _("Incomplete")


class VerificationDocumentStatus(ChoiceEnum):
    PENDING = 0, _("Pending")
    VERIFIED = 1, _("Verified")
    INCOMPLETE = 2, _("Incomplete")
    RETRY = 3, _("Retry")
    NOT_APPLICABLE = 4, _("Not Applicable")
    UPLOADED = 5, _("Uploaded")
    SUBMITTED = 6, _("Submitted")
    PENDING_REVIEW = 7, _("Pending for review")
    REVIEWED = 8, _("Reviewed")


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
