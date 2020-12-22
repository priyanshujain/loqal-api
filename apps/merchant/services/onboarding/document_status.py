from django.utils.translation import gettext as _

from api.services import ServiceBase
from apps.merchant.dbapi import (
    get_all_beneficial_owners,
    get_controller_details,
    get_incorporation_details
)
from apps.merchant.options import BenficialOwnerStatus


__all__ = (
    "DocumentRequirements",
)

class DocumentRequirements(ServiceBase):
    def __init__(self, merchant):
        self.merchant = merchant

    def handle(self):
        docs_required = {}
        ba_required_docs = []
        beneficial_owners = get_all_beneficial_owners(merchant_id=self.merchant.id)
        for beneficial_owner in beneficial_owners:
            if not beneficial_owner.dwolla_id:
                continue
            if beneficial_owner.status == BenficialOwnerStatus.DOCUMENT_PENDING:
                ba_details = self._individual_docs_requirement(beneficial_owner)
                ba_required_docs.append(ba_details)
        if ba_required_docs:
            docs_required["beneficial_owners"] = ba_required_docs
        
        controller = get_controller_details(merchant_id=self.merchant.id)
        if controller.verification_document_required:
            docs_required["controller"] = self._individual_docs_requirement(controller)
        
        incorporation_details = get_incorporation_details(merchant_id=self.merchant.id)
        if incorporation_details.verification_document_required:
            inc_details = {
                "verification_document_status": incorporation_details.verification_document_status.label 
            }
            if incorporation_details.verification_document_file:
                inc_details["verification_document_file"] = {
                    "id": incorporation_details.verification_document_file.id,
                    "file_name": incorporation_details.verification_document_file.file_name
                }
                inc_details["verification_document_type"] = incorporation_details.verification_document_type
            docs_required["incorporation"] = incorporation_details
        return docs_required
    
    def _individual_docs_requirement(self, individual_obj):
        req_details = {
                "first_name": individual_obj.first_name,
                "last_name": individual_obj.last_name,
                "id": individual_obj.id,
                "verification_document_status": individual_obj.verification_document_status.label 
            }
        if individual_obj.verification_document_file:
            req_details["verification_document_file"] = {
                "id": individual_obj.verification_document_file.id,
                "file_name": individual_obj.verification_document_file.file_name
            }
            req_details["verification_document_type"] = individual_obj.verification_document_type
        return req_details