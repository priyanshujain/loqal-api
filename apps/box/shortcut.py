import base64
import os
from datetime import datetime
from uuid import uuid4

from cryptography.fernet import Fernet
from werkzeug.utils import secure_filename


def validate_file_format(file_obj):
    suffix = os.path.splitext(file_obj.name)[-1].lower()
    if suffix not in [".gif", ".jpg", ".jpeg", ".pdf", ".png"]:
        return False

    return True


def safe_filename(filename):
    """
    Generates a safe filename that is unlikely to collide with existing objects.
    `filename.ext`` is transformed into ``filename-YYYY-MM-DD-HHMMSS.ext``
    """
    filename = secure_filename(filename)
    date = datetime.utcnow().strftime("%Y-%m-%d-%H%M%S")
    basename, extension = filename.rsplit(".", 1)
    return "{0}-{1}-{2}.{3}".format(basename, date, uuid4().hex, extension)


def generate_encryption_key():
    """Generates a 256 bit (32 byte) AES encryption key and prints the
    base64 representation.

    This is included for demonstration purposes. You should generate your own
    key. Please remember that encryption keys should be handled with a
    comprehensive security policy.
    #TODO: recheck for security policy and algo
    """
    # key = Fernet.generate_key()
    key = os.urandom(32)
    return base64.b64encode(key).decode("utf-8")
