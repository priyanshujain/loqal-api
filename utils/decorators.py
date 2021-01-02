from __future__ import absolute_import

import inspect


def user_attributes(klass):
    defaults = dir(type("defaults", (object,), {}))
    return [
        item[0]
        for item in inspect.getmembers(klass)
        if item[0] not in defaults
    ]


def meta_choices(klass):
    """
    Decorator to set `choices` and other attributes
    """
    _choices = []
    for attr in user_attributes(klass.Meta):
        val = getattr(klass.Meta, attr)
        setattr(klass, attr, val)
        _choices.append(val)
    setattr(klass, "choices", tuple(_choices))
    return klass


# Vendored from newer Django:
# https://github.com/django/django/blob/1.9.6/django/utils/decorators.py#L188-L197
class classproperty(object):
    def __init__(self, method=None):
        self.fget = method

    def __get__(self, instance, owner):
        return self.fget(owner)

    def getter(self, method):
        self.fget = method
        return self
