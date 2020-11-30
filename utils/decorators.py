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
