from django.utils.translation import gettext as _

from db.models.fields import ChoiceEnum


class MerchantAccountStatus(ChoiceEnum):
    PENDING = 0, _("Pending")
    VERIFIED = 1, _("Verified")
    DOCUMENT_PENDING = 2, _("Document Pending")
    REJECTED = 3, _("Rejected")
