from django.utils.translation import gettext as _

from db.models.fields import ChoiceEnum


class IssueTypes(ChoiceEnum):
    PATMENT = 0, _("Payment")
    CONSUMER_ACCOUNT = 1, _("Conusmer Account")
    MERCHANT_ACCOUNT = 2, _("Merchant Account")
    BANK_ACCOUNT = 3, _("Bank Account")
    OTHER = 4, _("Other")
