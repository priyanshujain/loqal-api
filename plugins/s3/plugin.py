"""
TODO: File encryption
1. https://github.com/marcobellaccini/pyAesCrypt/blob/master/pyAesCrypt/crypto.py

TODO: *
1. https://github.com/jschneier/django-storages/blob/master/storages/backends/s3boto3.py
"""

import tempfile
from io import BytesIO

import boto3
import six
from django.conf import settings
from django.utils.encoding import smart_bytes


class S3Storage(object):
    _bucket_name = settings.AWS_STORAGE_BUCKET_NAME

    def __init__(self):
        self._client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

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
        self._client.upload_fileobj(file_obj, self._bucket_name, filename)

        if signed_url:
            return self.signed_url(file_path=filename)
        return filename

    def upload_from_string(
        self, file_content, filename, content_type, encryption_key
    ):
        """
        Uploads a file to a given S3 bucket.
        """
        file_content = smart_bytes(file_content, encoding="utf-8")
        string_buffer = BytesIO(file_content)
        self._client.upload_fileobj(string_buffer, self._bucket_name, filename)
        return True

    def get_file(self, file_path, encryption_key):
        """
        returns the public url to the requested object.
        """
        return self.signed_url(file_path=file_path)

    def signed_url(self, file_path):
        url = self._client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": self._bucket_name, "Key": file_path},
            ExpiresIn=5 * 60,
        )

        if isinstance(url, six.binary_type):
            url = url.decode("utf-8")
        return url

    def write_to_file(self, file_path, file_obj, encryption_key):
        """
        returns the public url to the requested object.
        """
        # TODO: add error check for `file_obj`
        self._client.download_fileobj(self._bucket_name, file_path, file_obj)
        file_obj.seek(0)
        return file_obj

    def write_to_string(self, file_path, encryption_key):
        """
        returns the public url to the requested object.
        """
        with tempfile.TemporaryFile() as f:
            self._client.download_fileobj(self._bucket_name, file_path, f)
            f.seek(0)
            return f.read(), file_path
