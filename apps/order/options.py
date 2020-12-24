from db.models.fields import ChoiceCharEnum
from django.utils.translation import gettext as _

class OrderStatus(ChoiceCharEnum):
    DRAFT = "draft", _("Draft")
    UNCONFIRMED = "unconfirmed", _("Unconfirmed")
    UNFULFILLED = "unfulfilled", _("Unfulfilled")
    PARTIALLY_FULFILLED = "partially_fulfilled", _("Partially Fulfilled")
    FULFILLED = "fulfilled", _("Fulfilled")
    CANCELLED = "cancelled", _("Cancelled")


class OrderType(ChoiceCharEnum):
    IN_PERSON = "in_person", _("In Person")
    ONLINE = "online", _("Online")
