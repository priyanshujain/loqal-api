from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.services import ServiceBase
from apps.merchant.dbapi import (get_all_beneficial_owners,
                                 get_controller_details,
                                 get_incorporation_details)
from apps.merchant.options import (BeneficialOwnerStatus, BusinessDocumentType,
                                   BusinessTypes, IndividualDocumentType)

__all__ = ("DocumentRequirements",)


class DocumentRequirements(ServiceBase):
    def __init__(self, merchant, internal=False):
        self.merchant = merchant
        self.internal = internal

    def handle(self):
        docs_required = {}
        ba_required_docs = []
        beneficial_owners = get_all_beneficial_owners(
            merchant_id=self.merchant.id
        )
        for beneficial_owner in beneficial_owners:
            if not beneficial_owner.dwolla_id:
                raise ValidationError(
                    {
                        "detail": ErrorDetail(
                            "Please re-submit the data before uploading documents. "
                            "If you need further help please contact our "
                            "support team."
                        )
                    }
                )
            if (
                beneficial_owner.status
                == BeneficialOwnerStatus.DOCUMENT_PENDING
            ):
                ba_details = self._individual_docs_requirement(
                    beneficial_owner
                )
                if self.internal:
                    ba_details["orm_object"] = beneficial_owner
                ba_required_docs.append(ba_details)
        docs_required["beneficial_owners"] = ba_required_docs

        controller = get_controller_details(merchant_id=self.merchant.id)
        if controller.verification_document_required:
            controller_details = self._individual_docs_requirement(controller)
            if self.internal:
                controller_details["orm_object"] = controller
            docs_required["controller"] = controller_details
        else:
            docs_required["controller"] = None

        incorporation_details = get_incorporation_details(
            merchant_id=self.merchant.id
        )
        if incorporation_details.verification_document_required:
            inc_details = {}
            inc_details["documents"] = self._documents_detail(
                incorporation_details.documents
            )
            if self.internal:
                inc_details["orm_object"] = incorporation_details
            inc_details[
                "acceptable_document_types"
            ] = self._acceptable_business_document_types(incorporation_details)
            docs_required["incorporation"] = inc_details
        else:
            docs_required["incorporation"] = None
        return docs_required

    def _acceptable_business_document_types(self, incorporation_details):
        if (
            incorporation_details.business_type
            == BusinessTypes.SOLE_PROPRIETORSHIP
        ):
            return [
                {"document_type_label": v, "document_type_value": k}
                for k, v in BusinessDocumentType.choices
                if BusinessDocumentType.NOT_APPLICABLE.value != k
            ]
        return [
            {
                "document_type_label": BusinessDocumentType.EIN_LETTER.label,
                "document_type_value": BusinessDocumentType.EIN_LETTER.value,
            }
        ]

    def _individual_docs_requirement(self, individual_obj):
        req_details = {
            "first_name": individual_obj.first_name,
            "last_name": individual_obj.last_name,
            "id": individual_obj.id,
            "acceptable_document_types": [
                {"document_type_label": v, "document_type_value": k}
                for k, v in IndividualDocumentType.choices
                if IndividualDocumentType.NOT_APPLICABLE.value != k
            ],
        }
        req_details["documents"] = self._documents_detail(
            individual_obj.documents
        )
        return req_details

    def _documents_detail(self, documents):
        documents_data = []
        for document in documents.all():
            documents_data.append(
                {
                    "document_id": document.u_id,
                    "document_type": {
                        "label": document.document_type.label,
                        "value": document.document_type.value,
                    },
                    "document_file": {
                        "id": document.document_file.id,
                        "file_name": document.document_file.file_name,
                    },
                    "status": {
                        "label": document.status.label,
                        "value": document.status.value,
                    },
                    "failure_reason": document.failure_reason,
                    "all_failure_reasons": document.all_failure_reasons,
                }
            )
        return documents_data
