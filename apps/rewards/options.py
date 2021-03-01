from django.utils.translation import gettext as _

from db.models.fields import ChoiceCharEnum, ChoiceEnum

__all__ = (
    "LoyaltyParameters",
    "RewardValueType",
    "RewardType",
)


class LoyaltyParameters(ChoiceCharEnum):
    NUMBER_OF_VISITS = "number_of_visits", _("Number of visits")
    AMOUNT_SPENT = "amount_spent", _("Amount Spent")


class RewardValueType(ChoiceCharEnum):
    FIXED_AMOUNT = "fixed_amount", _("Fixed Amount")
    PERCENTAGE = "percentage", _("Percentage")


class RewardType(ChoiceCharEnum):
    ENTIRE_SALE = "entire_sale", _("Entire Sale")
