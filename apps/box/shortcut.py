import base64
import mimetypes
import os
from datetime import datetime
from uuid import uuid4

from cryptography.fernet import Fernet
from werkzeug.utils import secure_filename


def validate_file_format(file_obj):
    _, suffix = os.path.splitext(file_obj.name)
    suffix = suffix.lower()
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
    basename, extension = os.path.splitext(filename)
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


def fix_mimetype_file(file_object):
    if not file_object.content_type:
        return file_object

    if not file_object.name:
        file_object.name = uuid4().hex

    filename, file_extension = os.path.splitext(file_object.name)
    guessed_extension = mimetypes.guess_extension(file_object.content_type)
    if guessed_extension:
        file_extension = guessed_extension

    file_object.name = filename + file_extension
    return file_object
