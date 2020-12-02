from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ProviderAPIException
from api.services import ServiceBase
from apps.payment.dbapi import get_pending_transaction
from apps.payment.options import TransactionStatus
from apps.provider.lib.actions import ProviderAPIActionBase
from apps.provider.options import IntegratedProviders


class GetTransactionStatusAPIAction(ProviderAPIActionBase):
    def statuses(self):
        response = self.client.payment.get_status_all()
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


class TransactionStatusUpdate(ServiceBase):
    def __init__(self, account_id):
        self.account_id = account_id

    def execute(self):
        for provider_slug in IntegratedProviders.choices():
            pending_transactions = get_pending_transaction(
                account_id=self.account_id, provider_slug=provider_slug
            )
            provider_api_action = GetTransactionStatusAPIAction(
                account_id=self.account_id, provider_slug=provider_slug
            )
            transaction_statuses = provider_api_action.statuses()
            for transaction in pending_transactions:
                status = self.check_status(
                    provider_transaction_id=transaction.provider_transaction_id,
                    transaction_statuses=transaction_statuses,
                )
                if status == TransactionStatus.PROCESSED:
                    transaction.processed()

    def check_status(self, provider_transaction_id, transaction_statuses):
        statuses = [
            transaction_status["status"]
            for transaction_status in transaction_statuses
            if transaction_status["provider_transaction_id"]
            == provider_transaction_id
        ]
        if statuses:
            return statuses[0]
        return None
