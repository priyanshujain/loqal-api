from utils.choices import Choices


class UserType(Choices):
    REGULAR_USER = "REGULAR_USER"
    REGULAR_STAFF = "REGULAR_STAFF"
    ADMIN_STAFF = "ADMIN_STAFF"


from django.utils.translation import gettext as _

from db.models.fields import ChoiceCharEnum


class CustomerTypes(ChoiceCharEnum):
    MERCHANT = "merchant", _("Merchant")
    CONSUMER = "consumer", _("Consumer")
    INTERNAL = "internal", _("Internal")
