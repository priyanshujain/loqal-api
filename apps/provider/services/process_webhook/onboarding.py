from apps.account.options import (DwollaCustomerStatus,
                                  DwollaCustomerVerificationStatus)
from apps.merchant.dbapi.webhooks import (get_controller_document,
                                          get_incorporation_document)
from apps.merchant.options import VerificationDocumentStatus

from .tasks import get_document_failure_details


class ApplyOnboardingWebhook(object):
    def __init__(self, event, customer_account):
        self.event = event
        self.customer_account = customer_account

    def handle(self):
        topic = self.event.topic

        if topic == "customer_created":
            """
            A Customer was created.
            """
            # NOTE: this can be use to track error during sending
            # onboarding request to dwolla

            pass

        if topic == "customer_kba_verification_needed":
            """
            The retry identity verification attempt failed due insufficient scores
            on the submitted data. The end-user will have a single kba attempt
            to answer a set of “out of wallet” questions about themselves for
            identity verification.
            """
            # NOTE: we are not doing KBA verification
            pass

        if topic == "customer_kba_verification_failed":
            """
            The end-user failed KBA verification and were unable to correctly answer
            at least three KBA questions.
            """
            # NOTE: we are not doing KBA verification
            pass

        if topic == "customer_kba_verification_passed":
            """
            The end-user was able to correctly answer at least three KBA questions.
            """
            # NOTE: we are not doing KBA verification
            pass

        if topic == "customer_verification_document_needed":
            """
            Additional documentation is needed to verify a Customer.
            """
            self.customer_account.update_status(
                status=DwollaCustomerStatus.DOCUMENT,
                verification_status=DwollaCustomerVerificationStatus.DOCUMENT_NEEDED,
            )

        if topic == "customer_verification_document_uploaded":
            """
            A verification document was uploaded for a Customer.
            """
            self.customer_account.update_status(
                status=DwollaCustomerStatus.DOCUMENT,
                verification_status=DwollaCustomerVerificationStatus.DOCUMENT_UPLOADED,
            )

        if topic == "customer_verification_document_failed":
            """
            A verification document has been rejected for a Customer.
            """
            self.customer_account.update_status(
                status=DwollaCustomerStatus.DOCUMENT,
                verification_status=DwollaCustomerVerificationStatus.DOCUMENT_FAILED,
            )
            document_id = self.event.target_resource_dwolla_id
            failure_details = get_document_failure_details(
                document_id=document_id
            )
            document = get_incorporation_document(dwolla_id=document_id)
            if not document:
                document = get_controller_document(dwolla_id=document_id)
            document.add_failure_reason(
                failure_reason=failure_details["failure_reason"],
                all_failure_reasons=failure_details["all_failure_reasons"],
            )

        if topic == "customer_verification_document_approved":
            """
            A verification document was approved for a Customer.
            """
            self.customer_account.update_status(
                status=DwollaCustomerStatus.DOCUMENT,
                verification_status=DwollaCustomerVerificationStatus.DOCUMENT_APPROVED,
            )
            document_id = self.event.target_resource_dwolla_id
            document = get_incorporation_document(dwolla_id=document_id)
            if not document:
                document = get_controller_document(dwolla_id=document_id)
            document.update_status(status=VerificationDocumentStatus.VERIFIED)

        if topic == "customer_reverification_needed":
            """
            Incomplete information was received for a Customer;
            updated information is needed to verify the Customer.
            """
            self.customer_account.update_status(
                status=DwollaCustomerStatus.RETRY,
                verification_status=DwollaCustomerVerificationStatus.REVERIFICATION_NEEDED,
            )

        if topic == "customer_verified":
            """
            A Customer was verified.
            """
            self.customer_account.update_status(
                status=DwollaCustomerStatus.VERIFIED,
                verification_status=DwollaCustomerVerificationStatus.VERIFIED,
            )

        if topic == "customer_suspended":
            """
            A Customer was suspended.
            """
            self.customer_account.update_status(
                status=DwollaCustomerStatus.SUSPENDED,
                verification_status=DwollaCustomerVerificationStatus.SUSPENDED,
            )

        if topic == "customer_activated":
            """
            A Customer moves from deactivated or suspended to an active status.
            """
            self.customer_account.update_status(
                status=DwollaCustomerStatus.VERIFIED,
                verification_status=DwollaCustomerVerificationStatus.ACTIVATED,
            )

        if topic == "customer_deactivated":
            """
            A Customer was deactivated.
            """
            self.customer_account.update_status(
                status=DwollaCustomerStatus.DEACTIVATED,
                verification_status=DwollaCustomerVerificationStatus.DEACTIVATED,
            )

        self.event.mark_processed()
