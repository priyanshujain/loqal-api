import os
import tempfile

from django.db.models import Q
from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ProviderAPIException, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.account.options import DwollaCustomerVerificationStatus
from apps.box.dbapi import get_boxfile
from apps.merchant.dbapi.onboarding import get_beneficial_owner
from apps.merchant.options import VerificationDocumentStatus
from apps.provider.lib.actions import ProviderAPIActionBase
from plugins.s3 import S3Storage

from .document_req import DocumentRequirements

__all__ = ("SubmitDocuments",)


class SubmitDocuments(ServiceBase):
    def __init__(self, merchant):
        self.merchant = merchant

    def handle(self):
        upload_required_docs = self._validate_data()
        return self._upload_docs(required_docs=upload_required_docs)

    def _validate_data(self):
        required_docs = DocumentRequirements(
            merchant=self.merchant, internal=True
        ).handle()
        beneficial_owners = required_docs.get("beneficial_owners", [])
        controller = required_docs.get("controller", {})
        if controller:
            controller = controller.get("orm_object")
        incorporation = required_docs.get("incorporation", {})
        if incorporation:
            incorporation = incorporation.get("orm_object")

        all_docs_uploaded = True

        def check_if_document_upload_required(documents):
            if not documents.exists():
                return True
            elif (
                documents.all()
                .filter(
                    Q(status=VerificationDocumentStatus.FAILED)
                    | Q(status=VerificationDocumentStatus.PENDING)
                )
                .count()
                == documents.all().count()
            ):
                return True
            return False

        inc_docs_uploadable = None
        if incorporation and incorporation.verification_document_required:
            documents = incorporation.documents
            inc_docs_uploadable = self._get_docs_uploadable(documents)
            if not inc_docs_uploadable:
                if check_if_document_upload_required(documents):
                    all_docs_uploaded = False

        controller_docs_uploadable = None
        if controller:
            documents = controller.documents
            controller_docs_uploadable = self._get_docs_uploadable(documents)
            if not controller_docs_uploadable:
                if check_if_document_upload_required(documents):
                    all_docs_uploaded = False

        ba_docs = []
        if beneficial_owners:
            for beneficial_owner in beneficial_owners:
                beneficial_owner = beneficial_owner.get("orm_object")
                if beneficial_owner:
                    documents = beneficial_owner.documents
                    ba_single_docs_uploadable = self._get_docs_uploadable(
                        documents
                    )
                    if ba_single_docs_uploadable:
                        ba_docs.append(
                            {
                                "document": ba_single_docs_uploadable,
                                "orm_object": beneficial_owner,
                            }
                        )
                    elif check_if_document_upload_required(documents):
                        all_docs_uploaded = False
        if not all_docs_uploaded:
            raise ValidationError(
                {
                    "detail": [
                        ErrorDetail(
                            _(
                                "Please upload all required docs before submitting."
                            )
                        )
                    ]
                }
            )

        upload_required_docs = {
            "controller": None,
            "incorporation": None,
            "beneficial_owners": ba_docs,
        }
        if inc_docs_uploadable:
            upload_required_docs["incorporation"] = {
                "document": inc_docs_uploadable,
                "orm_object": incorporation,
            }
        if controller_docs_uploadable:
            upload_required_docs["controller"] = {
                "document": controller_docs_uploadable,
                "orm_object": controller,
            }
        return upload_required_docs

    def _get_docs_uploadable(self, documents):
        uploaded_docs = documents.all().filter(
            status=VerificationDocumentStatus.UPLOADED
        )
        if not uploaded_docs.exists():
            return None
        else:
            return uploaded_docs.first()

    def _upload_docs(self, required_docs):
        beneficial_owners = required_docs.get("beneficial_owners")
        controller = required_docs.get("controller")
        incorporation = required_docs.get("incorporation")

        if not (beneficial_owners or controller or incorporation):
            raise ValidationError(
                {"detail": ErrorDetail(_("No doument submit pending."))}
            )

        account_id = self.merchant.account.id
        if incorporation:
            incorporation_object = incorporation["orm_object"]
            document = incorporation["document"]
            api_response = CustomerDocumentUploadAPIAction(
                account_id=account_id,
            ).upload(
                document_file_id=document.document_file.id,
                document_type=document.document_type,
                entity_type="business",
            )
            document.add_dwolla_id(dwolla_id=api_response["dwolla_id"])

        if controller:
            controller_object = controller["orm_object"]
            document = controller["document"]
            api_response = CustomerDocumentUploadAPIAction(
                account_id=account_id
            ).upload(
                document_file_id=document.document_file.id,
                document_type=document.document_type,
                entity_type="controller",
            )
            document.add_dwolla_id(dwolla_id=api_response["dwolla_id"])

        if beneficial_owners:
            for beneficial_owner in beneficial_owners:
                beneficial_owner_object = beneficial_owner["orm_object"]
                document = beneficial_owner["document"]
                api_response = BeneficialOwnerDocumentUploadAPIAction(
                    account_id=account_id
                ).upload(
                    dwolla_id=beneficial_owner_object.dwolla_id,
                    document_file_id=document.document_file.id,
                    document_type=document.document_type,
                )
                document.add_dwolla_id(dwolla_id=api_response["dwolla_id"])
        self.merchant.account.update_status(
            verification_status=DwollaCustomerVerificationStatus.DOCUMENT_UPLOADED
        )
        return True


class BeneficialOwnerDocumentUploadAPIAction(ProviderAPIActionBase):
    def upload(self, dwolla_id, document_file_id, document_type):
        interface = DocumentInterface(boxfile_id=document_file_id)
        file = interface.get_file()
        response = self.client.account.upload_ba_document(
            beneficial_owner_id=dwolla_id,
            document_file=file,
            document_type=document_type,
        )
        interface.delete_temp_files()
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
            "dwolla_id": response["data"].get("dwolla_id"),
        }


class CustomerDocumentUploadAPIAction(ProviderAPIActionBase):
    def upload(
        self, document_file_id, document_type, entity_type="controller"
    ):
        interface = DocumentInterface(boxfile_id=document_file_id)
        file = interface.get_file()
        response = self.client.account.upload_customer_document(
            document_file=file,
            document_type=document_type,
            entity_type=entity_type,
        )
        interface.delete_temp_files()
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
            "dwolla_id": response["data"].get("dwolla_id"),
        }


class DocumentInterface(object):
    files = []

    def __init__(self, boxfile_id):
        self.boxfile_id = boxfile_id

    def get_file(self):
        s3_client = S3Storage()
        box_file = get_boxfile(boxfile_id=self.boxfile_id)
        file_content, file_name = s3_client.write_to_string(
            file_path=box_file.file_path,
            encryption_key=box_file.encryption_key,
        )
        _, file_extension = os.path.splitext(file_name)
        f = tempfile.NamedTemporaryFile(suffix=file_extension, delete=False)
        f.write(file_content)
        f.seek(0)
        self.files.append(f)
        return {
            "file": f,
            "file_name": box_file.file_name,
            "content_type": box_file.content_type,
        }

    def delete_temp_files(self):
        for file in self.files:
            try:
                os.unlink(file.name)
            except FileNotFoundError:
                continue
