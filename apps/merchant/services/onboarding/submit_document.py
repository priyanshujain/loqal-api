import os
import tempfile
from re import T

from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ProviderAPIException, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.account.options import MerchantAccountStatus
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
        beneficial_owners = required_docs.get("beneficial_owners")
        controller = required_docs.get("controller")
        incorporation = required_docs.get("incorporation")
        all_docs_uploaded = True
        if (
            incorporation
            and incorporation["verification_document_status"]
            == VerificationDocumentStatus.PENDING
        ):
            all_docs_uploaded = False
        if (
            controller
            and controller["verification_document_status"]
            == VerificationDocumentStatus.PENDING
        ):
            all_docs_uploaded = False
        if beneficial_owners:
            for beneficial_owner in beneficial_owners:
                if (
                    beneficial_owner["verification_document_status"]
                    == VerificationDocumentStatus.PENDING
                ):
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
            "beneficial_owners": None,
        }
        upload_required_docs["beneficial_owners"] = [
            beneficial_owner
            for beneficial_owner in beneficial_owners
            if beneficial_owner["verification_document_status"]
            == VerificationDocumentStatus.UPLOADED
        ]
        if (
            incorporation
            and incorporation["verification_document_status"]
            == VerificationDocumentStatus.UPLOADED
        ):
            upload_required_docs["incorporation"] = incorporation
        if (
            controller
            and controller["verification_document_status"]
            == VerificationDocumentStatus.UPLOADED
        ):
            upload_required_docs["controller"] = controller
        return upload_required_docs

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
            api_response = CustomerDocumentUploadAPIAction(
                account_id=account_id,
            ).upload(
                document_file_id=incorporation["verification_document_file"][
                    "id"
                ],
                document_type=incorporation["verification_document_type"],
                entity_type="business",
            )
            incorporation_object.add_dwolla_document_id(
                dwolla_id=api_response["dwolla_id"]
            )

        if controller:
            controller_object = controller["orm_object"]
            api_response = CustomerDocumentUploadAPIAction(
                account_id=account_id
            ).upload(
                document_file_id=controller["verification_document_file"][
                    "id"
                ],
                document_type=controller["verification_document_type"],
                entity_type="controller",
            )
            controller_object.add_dwolla_document_id(
                dwolla_id=api_response["dwolla_id"]
            )

        if beneficial_owners:
            for beneficial_owner in beneficial_owners:
                beneficial_owner_object = beneficial_owner["orm_object"]
                api_response = BeneficialOwnerDocumentUploadAPIAction(
                    account_id=account_id
                ).upload(
                    dwolla_id=beneficial_owner_object.dwolla_id,
                    document_file_id=beneficial_owner[
                        "verification_document_file"
                    ]["id"],
                    document_type=beneficial_owner[
                        "verification_document_type"
                    ],
                )
                beneficial_owner_object.add_dwolla_document_id(
                    dwolla_id=api_response["dwolla_id"]
                )
        self.merchant.update_status(
            status=MerchantAccountStatus.DOCUMENT_REVIEW_PENDING
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
        self.files.append(f)
        return f

    def delete_temp_files(self):
        for file in self.files:
            try:
                os.unlink(file.name)
            except FileNotFoundError:
                continue
