from __future__ import unicode_literals, absolute_import

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, ValidationError
from utils.imports import import_string

_default_password_validators = None


def get_default_password_validators():
    global _default_password_validators
    if _default_password_validators is None:
        _default_password_validators = get_password_validators(settings.AUTH_PASSWORD_VALIDATORS)
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