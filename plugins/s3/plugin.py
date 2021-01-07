"""
TODO: File encryption
1. https://github.com/marcobellaccini/pyAesCrypt/blob/master/pyAesCrypt/crypto.py
"""

import six
from django.conf import settings
import boto3
from io import BytesIO
import tempfile


def to_bytes(value, encoding="ascii"):

    result = value.encode(encoding) if isinstance(value, six.text_type) else value
    if isinstance(result, six.binary_type):
        return result
    else:
        raise TypeError("%r could not be converted to bytes" % (value,))


class S3Storage(object):
    def __init__(self):
        self._client = boto3.resource(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        self._bucket = self._client.Bucket(settings.S3_BUCKET_NAME)


    def upload_from_file(
        self,
        file_obj,
        filename,
        content_type,
        encryption_key,
        signed_url=False,
    ):
        """
        Uploads a file to a given S3 bucket.
        """
        self._bucket.upload_fileobj(file_obj, filename)

        if signed_url:
            return self.signed_url(file_path=filename)
        return filename

    def upload_from_string(
        self, file_content, filename, content_type, encryption_key
    ):
        """
        Uploads a file to a given S3 bucket.
        """
        file_content = to_bytes(file_content, encoding="utf-8")
        string_buffer = BytesIO(file_content)
        self._bucket.upload_fileobj(string_buffer, filename)
        return True

    def get_file(self, file_path, encryption_key):
        """
        returns the public url to the requested object.
        """
        return self.signed_url(file_path=file_path)

    def signed_url(self, file_path):
        url = self._bucket.generate_presigned_url(file_path, ExpiresIn=5*60)

        if isinstance(url, six.binary_type):
            url = url.decode("utf-8")
        return url

    def write_to_file(self, file_path, file_obj, encryption_key):
        """
        returns the public url to the requested object.
        """
        # TODO: add error check for `file_obj`
        self._bucket.download_fileobj(file_path, file_obj)
        file_obj.seek(0)
        return file_obj

    def write_to_string(self, file_path, encryption_key):
        """
        returns the public url to the requested object.
        """
        with tempfile.TemporaryFile() as f:
            self._bucket.download_fileobj(file_path, f)
            f.seek(0)
            return f.read()

