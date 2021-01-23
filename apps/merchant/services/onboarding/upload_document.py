"""
TODO: Check for file validation
1. Dwolla only allows file size upto 10MB
2. File types personal [.jpg, .png, .jpeg]
              business [.jpg, .png, .jpeg, .pdf]
"""
from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.box.dbapi import get_boxfile
from apps.merchant.dbapi.onboarding import (
    create_beneficial_owner_document, create_business_document,
    create_controller_document, get_beneficial_owner,
    get_beneficial_owner_document, get_business_document,
    get_controller_document, get_merchant_beneficial_owner_document,
    get_merchant_business_document, get_merchant_controller_document,
    update_beneficial_owner_document, update_business_document,
    update_controller_document)
from apps.merchant.options import (BeneficialOwnerStatus, BusinessDocumentType,
                                   BusinessTypes, VerificationDocumentStatus)
from apps.merchant.validators import (BeneficialOwnerDocumentValidator,
                                      BusinessDocumentValidator,
                                      ControllerDocumentValidator)

__all__ = (
    "BusinessDocumentUpload",
    "ControllerDocumentUpload",
    "BeneficialOwnerDocumentUpload",
)


class BusinessDocumentUpload(ServiceBase):
    """
    For corporation and llp it should be only ein_paper
    """

    def __init__(self, merchant, data):
        self.merchant = merchant
        self.data = data

    def handle(self):
        data = self._validate_data()
        document_file_id = data["document_file_id"]
        document_type = data["document_type"]
        incorporation_details = data["incorporation_details"]
        document = data.get("document")
        document_id = data.get("document_id")
        if document:
            update_business_document(
                document_id=document_id,
                document_file_id=document_file_id,
                document_type=document_type,
            )
        else:
            create_business_document(
                incorporation_details_id=incorporation_details.id,
                document_file_id=document_file_id,
                document_type=document_type,
            )
        boxfile = get_boxfile(boxfile_id=document_file_id)
        boxfile.enable_use()
        return True

    def _validate_data(self):
        data = run_validator(BusinessDocumentValidator, data=self.data)
        try:
            incorporation_details = self.merchant.incorporation_details
        except AttributeError:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _(
                            "Please add incorporation details first before uploading documents."
                        )
                    )
                }
            )

        data["incorporation_details"] = incorporation_details
        if not incorporation_details.verification_document_required:
            raise ValidationError(
                {"detail": [ErrorDetail(_("Document is not required."))]}
            )

        document_type = data["document_type"]
        if (
            incorporation_details.business_type
            != BusinessTypes.SOLE_PROPRIETORSHIP
            and document_type != BusinessDocumentType.EIN_LETTER.value
        ):
            raise ValidationError(
                {
                    "document_type": [
                        ErrorDetail(
                            _(
                                "If business if of type other than sole proprietor then,"
                                "verification document type can only be EIN letter."
                            )
                        )
                    ]
                }
            )

        document_id = data.get("document_id")
        if not document_id:
            documents = incorporation_details.documents
            if not documents.exists():
                return data
            for document in documents.all():
                if document.status != VerificationDocumentStatus.FAILED:
                    if document.status == VerificationDocumentStatus.VERIFIED:
                        raise ValidationError(
                            {
                                "detail": [
                                    ErrorDetail(
                                        _(
                                            "Incorporation document has already been verified."
                                        )
                                    )
                                ]
                            }
                        )
                    else:
                        raise ValidationError(
                            {
                                "detail": [
                                    ErrorDetail(
                                        _("Please update existing document.")
                                    )
                                ]
                            }
                        )
            return data

        document = get_business_document(
            document_id=document_id,
            incorporation_details_id=incorporation_details.id,
        )
        data["document"] = document
        return data


class ControllerDocumentUpload(ServiceBase):
    def __init__(self, merchant, data):
        self.merchant = merchant
        self.data = data

    def handle(self):
        data = self._validate_data()
        document_file_id = data["document_file_id"]
        document_type = data["document_type"]
        controller_details = data["controller_details"]
        document = data.get("document")
        document_id = data.get("document_id")
        if document:
            update_controller_document(
                document_id=document_id,
                document_file_id=document_file_id,
                document_type=document_type,
            )
        else:
            create_controller_document(
                controller_id=controller_details.id,
                document_file_id=document_file_id,
                document_type=document_type,
            )
        boxfile = get_boxfile(boxfile_id=document_file_id)
        boxfile.enable_use()
        return True

    def _validate_data(self):
        data = run_validator(ControllerDocumentValidator, data=self.data)
        try:
            controller_details = self.merchant.controller_details
        except AttributeError:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _(
                            "Please add controller details first before uploading documents."
                        )
                    )
                }
            )
        data["controller_details"] = controller_details
        if not controller_details.verification_document_required:
            raise ValidationError(
                {"detail": [ErrorDetail(_("Document is not required."))]}
            )

        document_id = data.get("document_id")
        if not document_id:
            documents = controller_details.documents
            if not documents.exists():
                return data
            for document in documents.all():
                if document.status != VerificationDocumentStatus.FAILED:
                    if document.status == VerificationDocumentStatus.VERIFIED:
                        raise ValidationError(
                            {
                                "detail": [
                                    ErrorDetail(
                                        _(
                                            "Incorporation document has already been verified."
                                        )
                                    )
                                ]
                            }
                        )
                    else:
                        raise ValidationError(
                            {
                                "detail": [
                                    ErrorDetail(
                                        _("Please update existing document.")
                                    )
                                ]
                            }
                        )
            return data

        document = get_controller_document(
            document_id=document_id, controller_id=controller_details.id
        )
        data["document"] = document
        return data


class BeneficialOwnerDocumentUpload(ServiceBase):
    def __init__(self, merchant, data):
        self.merchant = merchant
        self.data = data

    def handle(self):
        data = self._validate_data()
        document_file_id = data["document_file_id"]
        document_type = data["document_type"]
        beneficial_owner_id = data["beneficial_owner_id"]
        document = data.get("document")
        document_id = data.get("document_id")
        if document:
            update_beneficial_owner_document(
                document_id=document_id,
                document_file_id=document_file_id,
                document_type=document_type,
            )
        else:
            create_beneficial_owner_document(
                owner_id=beneficial_owner_id,
                document_file_id=document_file_id,
                document_type=document_type,
            )
        boxfile = get_boxfile(boxfile_id=document_file_id)
        boxfile.enable_use()

    def _validate_data(self):
        data = run_validator(BeneficialOwnerDocumentValidator, data=self.data)
        beneficial_owner_id = data["beneficial_owner_id"]
        benenficial_owner = get_beneficial_owner(
            merchant_id=self.merchant.id,
            beneficial_owner_id=beneficial_owner_id,
        )
        if not benenficial_owner:
            raise ValidationError(
                {
                    "beneficial_owner_id": [
                        ErrorDetail(_("Benefical owner is not valid"))
                    ]
                }
            )

        if benenficial_owner.status != BeneficialOwnerStatus.DOCUMENT_PENDING:
            raise ValidationError(
                {
                    "detail": [
                        ErrorDetail(_("Document has not been requested."))
                    ]
                }
            )

        document_id = data.get("document_id")
        if not document_id:
            documents = benenficial_owner.documents
            if not documents.exists():
                return data
            for document in documents.all():
                if document.status != VerificationDocumentStatus.FAILED:
                    if document.status == VerificationDocumentStatus.VERIFIED:
                        raise ValidationError(
                            {
                                "detail": [
                                    ErrorDetail(
                                        _(
                                            "Incorporation document has already been verified."
                                        )
                                    )
                                ]
                            }
                        )
                    else:
                        raise ValidationError(
                            {
                                "detail": [
                                    ErrorDetail(
                                        _("Please update existing document.")
                                    )
                                ]
                            }
                        )
            return data

        document = get_beneficial_owner_document(
            document_id=document_id, owner_id=benenficial_owner.id
        )
        data["document"] = document
        return data
