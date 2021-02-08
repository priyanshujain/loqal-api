from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.utils.translation import gettext, ngettext

from utils.imports import import_string

_default_password_validators = None


def get_default_password_validators():
    global _default_password_validators
    if _default_password_validators is None:
        _default_password_validators = get_password_validators(
            settings.AUTH_PASSWORD_VALIDATORS
        )
    return _default_password_validators


def get_password_validators(validator_config):
    validators = []
    for validator in validator_config:
        try:
            klass = import_string(validator["NAME"])
        except ImportError:
            msg = "The module in NAME could not be imported: %s. Check your AUTH_PASSWORD_VALIDATORS setting."
            raise ImproperlyConfigured(msg % validator["NAME"])
        validators.append(klass(**validator.get("OPTIONS", {})))

    return validators


def validate_password(password, password_validators=None):
    """
    Validate whether the password meets all validator requirements.

    If the password is valid, return ``None``.
    If the password is invalid, raise ValidationError with all error messages.
    """
    errors = []
    if password_validators is None:
        password_validators = get_default_password_validators()
    for validator in password_validators:
        try:
            validator.validate(password)
        except ValidationError as error:
            errors.append(error)
    if errors:
        raise ValidationError(errors)


class ContainsUppercaseValidator(object):
    def __init__(self, min_uppercase=1):
        self.min_uppercase = min_uppercase

    def validate(self, password, user=None):
        if sum(c.isupper() for c in password) < self.min_uppercase:
            raise ValidationError(
                ngettext(
                    "Password must contain at least %(min_uppercase)d uppercase character.",
                    "Password must contain at least %(min_uppercase)d uppercase characters.",
                    self.min_uppercase,
                ),
                code="password_too_weak",
                params={"min_uppercase": self.min_uppercase},
            )

    def get_help_text(self):
        return (
            ngettext(
                "Your password must contain at least %(min_uppercase)d uppercase character.",
                "Your password must contain at least %(min_uppercase)d uppercase characters.",
                self.min_uppercase,
            )
            % {"min_uppercase": self.min_uppercase}
        )


class ContainsLowercaseValidator(object):
    def __init__(self, min_lowercase=1):
        self.min_lowercase = min_lowercase

    def validate(self, password, user=None):
        if sum(c.islower() for c in password) < self.min_lowercase:
            raise ValidationError(
                ngettext(
                    "Password must contain at least %(min_lowercase)d lowercase character.",
                    "Password must contain at least %(min_lowercase)d lowercase characters.",
                    self.min_lowercase,
                ),
                code="password_too_weak",
                params={"min_lowercase": self.min_lowercase},
            )

    def get_help_text(self):
        return (
            ngettext(
                "Your password must contain at least %(min_lowercase)d lowercase character.",
                "Your password must contain at least %(min_lowercase)d lowercase characters.",
                self.min_lowercase,
            )
            % {"min_lowercase": self.min_lowercase}
        )


class ContainsSpecialCharactersValidator(object):
    def __init__(self, min_characters=1):
        self.min_characters = min_characters
        self.characters = set(" !\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")

    def validate(self, password, user=None):
        if sum(c in self.characters for c in password) < self.min_characters:
            raise ValidationError(
                ngettext(
                    "Password must contain at least %(min_characters)d special character.",
                    "Password must contain at least %(min_characters)d special characters.",
                    self.min_characters,
                ),
                code="password_too_weak",
                params={"min_characters": self.min_characters},
            )

    def get_help_text(self):
        return (
            ngettext(
                "Your password must contain at least %(min_characters)d special character.",
                "Your password must contain at least %(min_characters)d special characters.",
                self.min_characters,
            )
            % {"min_characters": self.min_characters}
        )


class ContainsDigitsValidator(object):
    def __init__(self, min_digits=1):
        self.min_digits = min_digits

    def validate(self, password, user=None):
        if sum(c.isdigit() for c in password) < self.min_digits:
            raise ValidationError(
                ngettext(
                    "Password must contain at least %(min_digits)d number.",
                    "Password must contain at least %(min_digits)d numbers.",
                    self.min_digits,
                ),
                code="password_too_weak",
                params={"min_digits": self.min_digits},
            )

    def get_help_text(self):
        return (
            ngettext(
                "Your password must contain at least %(min_digits)d number.",
                "Your password must contain at least %(min_digits)d numbers.",
                self.min_digits,
            )
            % {"min_digits": self.min_digits}
        )
