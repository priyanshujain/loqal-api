from django.utils.translation import gettext as _

from db.models.fields import ChoiceCharEnum, ChoiceEnum


class MerchantAccountStatus(ChoiceEnum):
    PENDING = 0, _("Pending")
    VERIFIED = 1, _("Verified")
    DOCUMENT_PENDING = 2, _("Document Pending")
    RETRY = 3, _("Retry")
    SUSPENDED = 4, _("Suspended")
    DOCUMENT_REVIEW_PENDING = 5, _("Document Review Pending")
    NON_SIGNED_UP = 6, _("Non Signed Up")


class MerchantAccountCerficationStatus(ChoiceEnum):
    PENDING = 0, _("Pending")
    UNCERTIFIED = 1, _("Uncertified")
    RECERTIFY = 2, _("Recertify")
    CERTIFIED = 3, _("Certified")


class ConsumerAccountStatus(ChoiceEnum):
    PENDING = 0, _("Pending")
    VERIFIED = 1, _("Verified")
    UNVERIFIED = 2, _("Unverified")


class DwollaCustomerVerificationStatus(ChoiceCharEnum):
    NOT_SENT = "not_sent", _("Not Sent")
    VERIFIED = "verified", _("Verified")
    UNVERIFIED = "unverified", _("Unverified")
    DOCUMENT_NEEDED = "document_needed", _("Document Needed")
    DOCUMENT_UPLOADED = "document_uploaded", _("Document Uploaded")
    DOCUMENT_FAILED = "document_failed", _("Document Failed")
    DOCUMENT_APPROVED = "document_approved", _("Document Approved")
    REVERIFICATION_NEEDED = "reverification_needed", _("Reverification Needed")
    RETRY = "retry", _("Retry")
    SUSPENDED = "suspended", _("Suspended")
    ACTIVATED = "activated", _("Activated")
    DEACTIVATED = "deactivated", _("Deactivated")


class DwollaCustomerStatus(ChoiceCharEnum):
    NOT_SENT = "not_sent", _("Not Sent")
    VERIFIED = "verified", _("Verified")
    UNVERIFIED = "unverified", _("Unverified")
    DOCUMENT = "document", _("Document")
    RETRY = "retry", _("Retry")
    SUSPENDED = "suspended", _("Suspended")
    DEACTIVATED = "deactivated", _("Deactivated")
