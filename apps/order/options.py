from django.utils.translation import gettext as _

from db.models.fields import ChoiceCharEnum, ChoiceEnum


class OrderStatus(ChoiceCharEnum):
    DRAFT = "draft", _("Draft")
    UNCONFIRMED = "unconfirmed", _("Unconfirmed")
    UNFULFILLED = "unfulfilled", _("Unfulfilled")
    PARTIALLY_FULFILLED = "partially_fulfilled", _("Partially Fulfilled")
    FULFILLED = "fulfilled", _("Fulfilled")
    PARTIALLY_RETURNED = "partially_returned", _("Partially Returned")
    RETURNED = "returned", _("Returned")
    CANCELLED = "cancelled", _("Cancelled")


class OrderType(ChoiceCharEnum):
    IN_PERSON = "in_person", _("In Person")
    ONLINE = "online", _("Online")


class OrderEventType(ChoiceEnum):
    CONFIRMED = 0, _("confirmed")
    CANCELED = 1, _("canceled")
    ORDER_MARKED_AS_PAID = 2, _("order_marked_as_paid")
    ORDER_FULLY_PAID = 3, _("order_fully_paid")
