from django.utils.translation import gettext_lazy as _
from rest_framework.fields import CharField

from api.serializers.base import ChoiceField, DictField, UUIDField

__all__ = (
    "ChoiceField",
    "UUIDField",
    "DictField",
    "EnumChoiceField",
    "EnumCharChoiceValueField",
    "EnumCharChoiceField",
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


class EnumChoiceField(ChoiceField):
    def __init__(self, enum_type, **kwargs):
        self.choices = enum_type.choices
        self.enum_choices = {str(key): value for key, value in enum_type.attrs}
        super().__init__(choices=self.choices, **kwargs)

    def to_representation(self, value):
        if value in ("", None):
            return value
        value = self.choice_strings_to_values.get(str(value), value)
        return self.enum_choices.get(value, value)


class EnumCharChoiceValueField(CharField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_representation(self, value):
        return getattr(value, "value", "")


class EnumCharChoiceField(ChoiceField):
    def __init__(self, choices, **kwargs):
        self.choices = [(k.value, k.label) for k in choices]
        super().__init__(choices=self.choices, **kwargs)
