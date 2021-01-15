from django.utils.translation import gettext as _

from db.models.fields import ChoiceCharEnum


class BankAccountStatus(ChoiceCharEnum):
    PENDING = "pending", _("Pending")
    VERIFIED = "verified", _("Verified")
    REVERIFICATION_REQUIRED = "re_verification_required", _(
        "Reverification Required"
    )
    SUSPENDED = "suspended", _("Suspended")
    USERNAME_CHANGED = "username_changed", _("Username Changed")
