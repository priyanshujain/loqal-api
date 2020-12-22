from apps.merchant.dbapi.onboarding import get_beneficial_owner
from apps.provider.lib.actions import ProviderAPIActionBase
from api.helpers import run_validator
import os
import tempfile

from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ProviderAPIException, ValidationError
from api.services import ServiceBase
from apps.box.dbapi import get_boxfile
from plugins.gcs import GoogleCloudStorage


class BeneficialOwnerDocumentUploadAPIAction(ProviderAPIActionBase):
    def upload(self, document_file, document_type):
        response = self.client.account.upload_customer_document(
            document_file=document_file, document_type=document_type
        )
        if self.get_errors(response):
            raise ProviderAPIException(
                {
                    "detail": ErrorDetail(
                        _(
                            "KYC service failed, Please try "
                            "again. If the problem persists please "
                            "contact our support team."
                        )
                    )
                }
            )
        return {
            "status": response["data"].get("status"),
        }


class DocumentInterface(object):
    def __init__(self, boxfile_id):
        self.boxfile_id = boxfile_id

    def get_file(self):
        gcs_client = GoogleCloudStorage()
        box_file = get_boxfile(boxfile_id=self.boxfile_id)
        file_content, file_name = gcs_client.write_to_string(
            file_path=box_file.file_path,
            encryption_key=box_file.encryption_key,
        )
        _, file_extension = os.path.splitext(file_name)
        f = tempfile.NamedTemporaryFile(suffix=file_extension, delete=False)
        f.write(file_content)
        return {"file_name": box_file.file_name, "file_object": f}

    def delete_temp_files(self, files):
        for file in files:
            try:
                file_object = file["file_object"]
                os.unlink(file_object.name)
            except FileNotFoundError:
                continue

