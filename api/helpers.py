from .exceptions import ValidationError


def run_validator(validator, data, context=None):
    s = validator(data=data, context=context)
    if s.is_valid():
        return s.data
    else:
        raise ValidationError(s.errors)
