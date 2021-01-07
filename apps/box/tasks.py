import os

from apps.box.shortcut import generate_encryption_key, safe_filename
from plugins.s3 import S3Storage


def store_file_to_gcs(file_obj, file_name, content_type, signed_url=False):
    gcs_client = S3Storage()
    encryption_key = generate_encryption_key()
    filename = safe_filename(file_name)
    url_ = gcs_client.upload_from_file(
        file_obj=file_obj,
        filename=filename,
        content_type=content_type,
        encryption_key=encryption_key,
        signed_url=signed_url,
    )

    return dict(
        file_obj=file_obj,
        file_name=filename,
        content_type=content_type,
        encryption_key=encryption_key,
        signed_url=url_,
    )


def get_file_from_gcs(file_data):
    gcs_client = S3Storage()
    return gcs_client.get_file(
        file_path=file_data["file_path"],
        encryption_key=file_data["encryption_key"],
    )
