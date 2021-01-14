from django.utils.translation import gettext as _

from db.models.fields import ChoiceEnum


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
