from django.utils.translation import gettext as _

from api.services import ServiceBase
from apps.merchant.dbapi import (get_all_beneficial_owners,
                                 get_controller_details,
                                 get_incorporation_details)
from apps.merchant.options import BeneficialOwnerStatus

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
                continue
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
            inc_details = {
                "verification_document_status": incorporation_details.verification_document_status.label
            }
            if incorporation_details.verification_document_file:
                inc_details["verification_document_file"] = {
                    "id": incorporation_details.verification_document_file.id,
                    "file_name": incorporation_details.verification_document_file.file_name,
                }
                inc_details[
                    "verification_document_type"
                ] = incorporation_details.verification_document_type.label
            if self.internal:
                inc_details[
                    "verification_document_type"
                ] = incorporation_details.verification_document_type
                inc_details[
                    "verification_document_status"
                ] = incorporation_details.verification_document_status
                inc_details["orm_object"] = incorporation_details
            docs_required["incorporation"] = inc_details
        else:
            docs_required["incorporation"] = None
        return docs_required

    def _individual_docs_requirement(self, individual_obj):
        req_details = {
            "first_name": individual_obj.first_name,
            "last_name": individual_obj.last_name,
            "id": individual_obj.id,
            "verification_document_status": individual_obj.verification_document_status.label,
        }
        if individual_obj.verification_document_file:
            req_details["verification_document_file"] = {
                "id": individual_obj.verification_document_file.id,
                "file_name": individual_obj.verification_document_file.file_name,
            }
            req_details[
                "verification_document_type"
            ] = individual_obj.verification_document_type.label
            if self.internal:
                req_details[
                    "verification_document_type"
                ] = individual_obj.verification_document_type
                req_details[
                    "verification_document_status"
                ] = individual_obj.verification_document_status
        return req_details
