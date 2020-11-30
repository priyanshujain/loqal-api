import base64
import datetime
import hashlib
import os
import random
import re
import time
import uuid
from base64 import b64encode
from functools import partial
from io import BytesIO

from cryptography.fernet import Fernet
from django.utils.crypto import get_random_string


def rand_str(length=128, type="str"):
    """
    Generate a random string or number of a specified length, which can be used in security scenarios such as keys
    """
    if type == "str":
        return get_random_string(
            length,
            allowed_chars="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
        )
    elif type == "lower_str":
        return get_random_string(
            length, allowed_chars="abcdefghijklmnopqrstuvwxyz0123456789"
        )
    elif type == "lower_hex":
        return random.choice("123456789abcdef") + get_random_string(
            length - 1, allowed_chars="0123456789abcdef"
        )
    else:
        return random.choice("123456789") + get_random_string(
            length - 1, allowed_chars="0123456789"
        )


def build_query_string(kv_data, ignore_none=True):
    # {"a": 1, "b": "test"} -> "?a=1&b=test"
    query_string = ""
    for k, v in kv_data.items():
        if ignore_none is True and kv_data[k] is None:
            continue
        if query_string != "":
            query_string += "&"
        else:
            query_string = "?"
        query_string += k + "=" + str(v)
    return query_string


def img2base64(img):
    with BytesIO() as buf:
        img.save(buf, "gif")
        buf_str = buf.getvalue()
    img_prefix = "data:image/png;base64,"
    b64_str = img_prefix + b64encode(buf_str).decode("utf-8")
    return b64_str


def datetime2str(value, format="iso-8601"):
    if format.lower() == "iso-8601":
        value = value.isoformat()
        if value.endswith("+00:00"):
            value = value[:-6] + "Z"
        return value
    return value.strftime(format)


def timestamp2utcstr(value):
    return datetime.datetime.utcfromtimestamp(value).isoformat()


def natural_sort_key(s, _nsre=re.compile(r"(\d+)")):
    return [
        int(text) if text.isdigit() else text.lower()
        for text in re.split(_nsre, s)
    ]


def get_env(name, default=""):
    return os.environ.get(name, default)


def _update_filename(instance, filename, path, prefix):
    ext = filename.split(".")[-1]
    # set filename as random string
    random_id = "rid_%s_%d" % (uuid.uuid4().hex, int(time.time()))
    filename = "{}.{}.{}".format(prefix, random_id, ext)
    # return the whole path to the file
    return os.path.join(path, filename)


def upload_to(path, prefix):
    return partial(_update_filename, path=path, prefix=prefix)


def generate_encryption_key():
    """Generates a 256 bit (32 byte) AES encryption key and prints the
    base64 representation.

    This is included for demonstration purposes. You should generate your own
    key. Please remember that encryption keys should be handled with a
    comprehensive security policy.
    #TODO: recheck for security policy and algo
    """
    key = Fernet.generate_key()
    return base64.b64encode(key).decode("utf-8")
