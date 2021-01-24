def to_float(num):
    if num is None:
        return 0.0
    else:
        return float(num)


def to_int(num):
    if num is None:
        return 0
    else:
        return int(num)


def to_str(s):
    if s is None:
        return ""
    return str(s)
