from django.utils.translation import gettext_lazy as _

from api.serializers.base import ChoiceField, DictField, UUIDField

__all__ = (
    "ChoiceField",
    "UUIDField",
    "DictField",
)


class ChoiceField(ChoiceField):
    default_error_messages = {
        "invalid_choice": _("{input} is not a supported.")
    }


class UUIDField(UUIDField):
    default_error_messages = {
        "invalid": _("Provided value is not in a valid format.")
    }


class DictField(DictField):
    default_error_messages = {
        "not_a_dict": _(
            "Provided value is not in a valid JSON dictionary format."
        ),
        "empty": _("This JSON dictionary may not be empty."),
    }
