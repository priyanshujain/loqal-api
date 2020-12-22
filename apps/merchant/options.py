from django.utils.translation import gettext as _

from db.models.fields import ChoiceEnum

__all__ = (
    "BusinessTypes",
    "MemberType",
    "FeatureAcessTypes",
    "AllowedFeatureAcessTypes",
)


class BusinessTypes(ChoiceEnum):
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


class BenficialOwnerStatus(ChoiceEnum):
    PENDING = 0, _("Pending")
    VERIFIED = 1, _("Verified")
    DOCUMENT_PENDING = 2, _("Document Pending")
    INCOMPLETE = 3, _("Incomplete")


class VerificationDocumentStatus(ChoiceEnum):
    PENDING = 0, _("Pending")
    VERIFIED = 1, _("Verified")
    INCOMPLETE = 2, _("Incomplete")
    RETRY = 3, _("Retry")
    NOT_APPLICABLE = 4, ("Not Applicable")
