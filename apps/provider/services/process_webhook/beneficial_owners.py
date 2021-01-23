from apps.merchant.dbapi.webhooks import (get_beneficial_owner_by_dwolla_id,
                                          get_owner_document)
from apps.merchant.options import BeneficialOwnerStatus

from .tasks import get_document_failure_details


class ApplyBeneficialOwnerWebhook(object):
    def __init__(self, event, customer_account):
        self.event = event
        self.customer_account = customer_account

    def handle(self):
        topic = self.event.topic

        if topic == "customer_beneficial_owner_created":
            """
            Beneficial owner successfully created.
            """
            pass

        if topic == "customer_beneficial_owner_removed":
            """
            An individual beneficial owner has been successfully
            removed from the Customer.
            """
            pass

        if topic == "customer_beneficial_owner_verification_document_needed":
            """
            Additional documentation is needed to verify an individual
            beneficial owner.
            """
            dwolla_id = self.event.target_resource_dwolla_id
            beneficial_owner = get_beneficial_owner_by_dwolla_id(
                dwolla_id=dwolla_id
            )
            beneficial_owner.update_status(
                status=BeneficialOwnerStatus.DOCUMENT_PENDING
            )

        if topic == "customer_beneficial_owner_verification_document_uploaded":
            """
            A verification document was uploaded for beneficial owner.
            """
            pass

        if topic == "customer_beneficial_owner_verification_document_failed":
            """
            A verification document has been rejected for a beneficial owner.
            """
            document_id = self.event.target_resource_dwolla_id
            failure_details = get_document_failure_details(
                document_id=document_id
            )
            document = get_owner_document(dwolla_id=document_id)
            document.add_failure_reason(
                failure_reason=failure_details["failure_reason"],
                all_failure_reasons=failure_details["all_failure_reasons"],
            )

        if topic == "customer_beneficial_owner_verification_document_approved":
            """
            A verification document was approved for a beneficial owner.
            """
            pass

        if topic == "customer_beneficial_owner_reverification_needed":
            """
            A previously verified beneficial owner status has changed due to
            either a change in the beneficial owner’s information or at request
            for more information from Dwolla. The individual will need to verify
            their identity within 30 days.
            """
            pass

        if topic == "customer_beneficial_owner_verified":
            """
            A beneficial owner has been verified.
            """
            dwolla_id = self.event.target_resource_dwolla_id
            beneficial_owner = get_beneficial_owner_by_dwolla_id(
                dwolla_id=dwolla_id
            )
            beneficial_owner.update_status(
                status=BeneficialOwnerStatus.VERIFIED
            )

        self.event.mark_processed()
