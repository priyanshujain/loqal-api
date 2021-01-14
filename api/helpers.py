from .exceptions import ValidationError


def run_validator(validator, data, context=None, many=False):
    s = validator(data=data, context=context, many=many)
    if s.is_valid():
        return s.data
    else:
        raise ValidationError(s.errors)
