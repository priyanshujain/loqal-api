from apps.merchant.dbapi.onboarding import (
    get_beneficial_owner,
    update_business_document,
    update_beneficial_owner_document,
    update_controller_document,
)
from api.helpers import run_validator

from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.services import ServiceBase
from apps.box.dbapi import get_boxfile
from apps.merchant.validators import (
    BusinessDocumentValidator,
    ControllerDocumentValidator,
    BeneficialOwnerDocumentValidator,
)
from apps.merchant.options import (
    BusinessTypes,
    BusinessDocumentType,
    BeneficialOwnerStatus,
)
from apps.box.dbapi import get_boxfile


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
        verification_document_file_id = data["verification_document_file_id"]
        verification_document_type = data["verification_document_type"]
        update_business_document(
            merchant_id=self.merchant.id,
            verification_document_id=verification_document_file_id,
            verification_document_type=verification_document_type,
        )
        boxfile = get_boxfile(boxfile_id=verification_document_file_id)
        boxfile.enable_use()
        return True

    def _validate_data(self):
        data = run_validator(BusinessDocumentValidator, data=self.data)
        try:
            incorporation_details = self.merchant.incorporationdetails
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

        if not incorporation_details.verification_document_required:
            raise ValidationError(
                {"detail": [ErrorDetail(_("Document is not required."))]}
            )
        verification_document_type = data["verification_document_type"]
        if (
            incorporation_details.business_type != BusinessTypes.SOLE_PROPRIETORSHIP
            and verification_document_type != BusinessDocumentType.EIN_LETTER
        ):
            raise ValidationError(
                {
                    "verification_document_type": [
                        ErrorDetail(
                            _(
                                "If business if of type other than sole proprietor then,"
                                "verification document type can only be EIN letter."
                            )
                        )
                    ]
                }
            )
        return data


class ControllerDocumentUpload(ServiceBase):
    def __init__(self, merchant, data):
        self.merchant = merchant
        self.data = data

    def handle(self):
        data = self._validate_data()
        verification_document_file_id = data["verification_document_file_id"]
        verification_document_type = data["verification_document_type"]
        update_controller_document(
            merchant_id=self.merchant.id,
            verification_document_id=verification_document_file_id,
            verification_document_type=verification_document_type,
        )
        boxfile = get_boxfile(boxfile_id=verification_document_file_id)
        boxfile.enable_use()
        return True

    def _validate_data(self):
        data = run_validator(ControllerDocumentValidator, data=self.data)
        try:
            controller_details = self.merchant.controllerdetails
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

        if not controller_details.verification_document_required:
            raise ValidationError(
                {"detail": [ErrorDetail(_("Document is not required."))]}
            )
        return data


class BeneficialOwnerDocumentUpload(ServiceBase):
    def __init__(self, merchant, data):
        self.merchant = merchant
        self.data = data

    def handle(self):
        data = self._validate_data()
        verification_document_file_id = data["verification_document_file_id"]
        verification_document_type = data["verification_document_type"]
        beneficial_owner_id = data["beneficial_owner_id"]
        update_beneficial_owner_document(
            beneficial_owner_id=beneficial_owner_id,
            verification_document_id=verification_document_file_id,
            verification_document_type=verification_document_type,
        )
        boxfile = get_boxfile(boxfile_id=verification_document_file_id)
        boxfile.enable_use()

    def _validate_data(self):
        data = run_validator(BeneficialOwnerDocumentValidator, data=self.data)
        beneficial_owner_id = data["beneficial_owner_id"]
        benenficial_owner = get_beneficial_owner(
            merchant_id=self.merchant.id, beneficial_owner_id=beneficial_owner_id
        )
        if not beneficial_owner_id:
            ValidationError(
                {
                    "beneficial_owner_id": [
                        ErrorDetail(_("Benefical owner is not valid"))
                    ]
                }
            )

        if benenficial_owner.status != BeneficialOwnerStatus.DOCUMENT_PENDING:
            ValidationError(
                {"detail": [ErrorDetail(_("Document has not been requested."))]}
            )
        return data
