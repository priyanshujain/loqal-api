"""
# Taken from https://github.com/awesto/django-shop/blob/master/shop/models/fields.py
# TODO: Fix all licensing requirements
"""

import enum

from django.db import models
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _

__all__ = (
    "ChoiceEnum",
    "ChoiceEnumField",
)


class ChoiceEnumMeta(enum.EnumMeta):
    def __call__(cls, value, *args, **kwargs):
        if isinstance(value, str):
            try:
                value = cls.__members__[value]
            except KeyError:
                pass  # let the super method complain
        return super().__call__(value, *args, **kwargs)

    def __new__(metacls, classname, bases, classdict):
        labels = {}
        for key in classdict._member_names:
            source_value = classdict[key]
            if isinstance(source_value, (list, tuple)):
                try:
                    val, labels[key] = source_value
                except ValueError:
                    raise ValueError(
                        "Invalid ChoiceEnum member '{}'".format(key)
                    )
            else:
                val = source_value
                labels[key] = key.replace("_", " ").title()
            # Use dict.__setitem__() to suppress defenses against
            # double assignment in enum's classdict
            dict.__setitem__(classdict, key, val)
        cls = super().__new__(metacls, classname, bases, classdict)
        for key, label in labels.items():
            getattr(cls, key).label = label
        return cls

    @property
    def choices(cls):
        return [(k.value, k.label) for k in cls]

    @property
    def default(cls):
        try:
            return next(iter(cls))
        except StopIteration:
            return None


class ChoiceEnum(enum.Enum, metaclass=ChoiceEnumMeta):
    """
    Utility class to handle choices in Django model and/or form fields.
    Usage:
    class Color(ChoiceEnum):
        WHITE = 0, "White"
        RED = 1, "Red"
        GREEN = 2, "Green"
        BLUE = 3, "Blue"
    green = Color.GREEN
    color = forms.ChoiceField(
        choices=Color.choices,
        default=Color.default,
    )
    """

    def __str__(self):
        return force_str(self.label)


# TODO: Error it does not add default value in django migration
class ChoiceEnumField(models.PositiveSmallIntegerField):
    description = _("")

    def __init__(self, *args, **kwargs):
        self.enum_type = kwargs.pop(
            "enum_type", ChoiceEnum
        )  # fallback is required form migrations
        if not issubclass(self.enum_type, ChoiceEnum):
            raise ValueError("enum_type must be a subclass of `ChoiceEnum`.")
        kwargs.update(choices=self.enum_type.choices)
        kwargs.setdefault("default", self.enum_type.default)
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if "choices" in kwargs:
            del kwargs["choices"]
        if kwargs["default"] is self.enum_type.default:
            del kwargs["default"]
        elif isinstance(kwargs["default"], self.enum_type):
            kwargs["default"] = kwargs["default"].value
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection):
        try:
            return self.enum_type(value)
        except ValueError:
            return value

    def get_prep_value(self, state):
        if isinstance(state, self.enum_type):
            return state.value
        return state

    def to_python(self, state):
        return self.enum_type(state)

    def value_to_string(self, obj):
        value = getattr(obj, self.name, obj)
        if not isinstance(value, self.enum_type):
            raise ValueError("Value must be of type {}".format(self.enum_type))
        return value.name
