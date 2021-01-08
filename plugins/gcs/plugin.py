"""
TODO: File encryption
1. https://github.com/marcobellaccini/pyAesCrypt/blob/master/pyAesCrypt/crypto.py
"""

import base64
from datetime import timedelta

import six
from django.conf import settings
from google.cloud import storage


# TODO: https://github.com/googleapis/python-storage/issues/221
class GoogleCloudStorage(object):
    def __init__(self):
        self._client = storage.Client(
            project=settings.GS_CREDENTIALS.project_id,
            credentials=settings.GS_CREDENTIALS,
        )
        self._bucket = self._client.bucket(settings.GS_BUCKET_NAME)

    def __create_blob(self, filename, encryption_key):
        encryption_key = base64.b64decode(encryption_key)
        blob = self._bucket.blob(filename)  # , encryption_key=encryption_key)
        return blob

    def __get_blob(self, file_path, encryption_key):
        encryption_key = base64.b64decode(encryption_key)
        blob = self._bucket.__get_blob(
            file_path
        )  # , encryption_key=encryption_key)
        return blob

    def upload_from_file(
        self,
        file_obj,
        filename,
        content_type,
        encryption_key,
        signed_url=False,
    ):
        """
        Uploads a file to a given Cloud Storage bucket.
        """
        blob = self.__create_blob(filename, encryption_key=encryption_key)
        blob.upload_from_file(file_obj=file_obj, content_type=content_type)

        if signed_url:
            return self.signed_url(blob)
        return filename

    def upload_from_string(
        self, file_content, filename, content_type, encryption_key
    ):
        """
        Uploads a file to a given Cloud Storage bucket.
        """
        blob = self.__create_blob(filename, encryption_key=encryption_key)
        blob.upload_from_string(file_content, content_type=content_type)
        return True

    def get_file(self, file_path, encryption_key):
        """
        returns the public url to the requested object.
        """
        blob = self.__get_blob(file_path, encryption_key=encryption_key)
        return self.signed_url(blob)

    def signed_url(self, blob):
        expiration = timedelta(minutes=5)
        url = blob.generate_signed_url(method="GET", expiration=expiration)

        if isinstance(url, six.binary_type):
            url = url.decode("utf-8")
        return url

    def write_to_file(self, file_path, file_obj, encryption_key):
        """
        returns the public url to the requested object.
        """
        # TODO: add error check for `file_obj`
        blob = self.__get_blob(file_path, encryption_key=encryption_key)
        blob.download_to_file(file_obj, client=self._client)
        file_obj.seek(0)
        return file_obj

    def write_to_string(self, file_path, encryption_key):
        """
        returns the public url to the requested object.
        """
        # TODO: add error check for `file_obj`
        blob = self.__get_blob(file_path, encryption_key=encryption_key)
        return blob.download_as_string(client=self._client), blob.name
