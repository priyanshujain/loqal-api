from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ProviderAPIException, ValidationError
from apps.account.dbapi.webhooks import get_account_by_dwolla_id
from apps.banking.notifications import SendVerifyMicroDepositEmail
from apps.payment.options import (TransactionFailureReasonType,
                                  TransactionStatus)
from apps.provider.lib.actions import ProviderAPIActionBase


class GetPaymentFailureDetailsAPIAction(ProviderAPIActionBase):
    def get(self, transfer_id):
        response = self.client.payment.get_payment_failure(
            transfer_id=transfer_id
        )
        if self.get_errors(response):
            raise ProviderAPIException(
                {
                    "detail": ErrorDetail(
                        _(
                            "Banking service failed, Please try "
                            "again. If the problem persists please "
                            "contact our support team."
                        )
                    )
                }
            )
        return response["data"]


def get_payment_failure(transfer_id):
    return GetPaymentFailureDetailsAPIAction().get(transfer_id=transfer_id)


class GetFundingSourceDetailsAPIAction(ProviderAPIActionBase):
    def get(self, funding_source_id):
        response = self.client.banking.get_bank_account(
            funding_source_id=funding_source_id
        )
        if self.get_errors(response):
            raise ProviderAPIException(
                {
                    "detail": ErrorDetail(
                        _(
                            "Banking service failed, Please try "
                            "again. If the problem persists please "
                            "contact our support team."
                        )
                    )
                }
            )
        return response["data"]


class GetFailedDocumentDetailsAPIAction(ProviderAPIActionBase):
    def get(self, document_id):
        response = self.client.account.get_customer_document(
            document_id=document_id
        )
        if self.get_errors(response):
            raise ProviderAPIException(
                {
                    "detail": ErrorDetail(
                        _(
                            "Banking service failed, Please try "
                            "again. If the problem persists please "
                            "contact our support team."
                        )
                    )
                }
            )
        return response["data"]


def get_document_failure_details(document_id):
    return GetFailedDocumentDetailsAPIAction().get(document_id=document_id)


def get_bank_account(funding_source_id):
    return GetFundingSourceDetailsAPIAction().get(
        funding_source_id=funding_source_id
    )


def get_account(customer_id):
    return get_account_by_dwolla_id(dwolla_id=customer_id)


def record_payment_failure(transaction, at_source):
    transaction.status = TransactionStatus.FAILED
    failure_details = get_payment_failure(transfer_id=transaction.dwolla_id)
    if not failure_details:
        return None

    transaction.is_sender_failure = at_source
    if at_source:
        transaction.failure_reason_type = (
            TransactionFailureReasonType.PRE_SOURCE_ACH_FAILED
        )
    else:
        transaction.failure_reason_type = (
            TransactionFailureReasonType.PRE_DESTINATION_ACH_FAILED
        )
    ach_return_account = None
    ach_return_bank_account = None
    funding_source_id = (
        failure_details.get("_links", {})
        .get("failed-funding-source", {})
        .get("href", "")
        .split("/")
        .pop()
    )
    if funding_source_id:
        ach_return_bank_account = get_bank_account
    customer_id = (
        failure_details.get("_links", {})
        .get("customer", {})
        .get("href", "")
        .split("/")
        .pop()
    )
    if customer_id:
        ach_return_account = get_account(customer_id=customer_id)
    transaction.log_ach_return(
        ach_return_code=failure_details.get("code", ""),
        ach_return_description=failure_details.get("description", ""),
        ach_return_explaination=failure_details.get("explaination", ""),
        ach_return_bank_account=ach_return_bank_account,
        ach_return_account=ach_return_account,
    )
    return failure_details


def send_micro_deposit_verify_email(bank_account):
    account = bank_account.account
    email = ""
    try:
        consumer = account.consumer
        email = consumer.user.email
    except Exception:
        pass

    try:
        merchant = account.merchant
        email = merchant.company_email
    except Exception:
        pass
    SendVerifyMicroDepositEmail(email=email).send()
