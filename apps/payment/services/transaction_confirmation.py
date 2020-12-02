from tempfile import NamedTemporaryFile

import magic
from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ProviderAPIException
from api.services import ServiceBase
from apps.box.dbapi import create_boxfile
from apps.box.tasks import store_file_to_gcs
from apps.payment.dbapi import get_transaction
from apps.provider.lib.actions import ProviderAPIActionBase


class TransactionConfirmationAPIAction(ProviderAPIActionBase):
    def get(self, provider_transaction_id):
        response = self.client.payment.payment_confirmation(
            provider_transaction_id=provider_transaction_id
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


class TransactionConfirmation(ServiceBase):
    def __init__(self, account_id, transaction_id):
        self.transaction_id = transaction_id
        self.account_id = account_id

    def execute(self):
        transaction = get_transaction(
            account_id=self.account_id, transaction_id=self.transaction_id
        )
        provider_slug = (
            transaction.quote.payment_account.provider.provider_slug
        )
        provider_api_action = TransactionConfirmationAPIAction(
            account_id=self.account_id, provider_slug=provider_slug
        )
        provider_reponse = provider_api_action.get(
            provider_transaction_id=transaction.provider_transaction_id
        )

        file_content = provider_reponse["content"]
        file_url = self._create_file(
            transaction=transaction, file_content=file_content
        )
        return file_url

    def _create_file(self, transaction, file_content):
        file_name = f"payment-confirmation-{transaction.id}.pdf"
        with NamedTemporaryFile(suffix=".pdf") as temp_file_:
            temp_file_.write(file_content)
            temp_file_.seek(0)
            content_type = magic.from_buffer(
                temp_file_.read(256), mime=True
            ).format()
            temp_file_.seek(0)
            gcs_file = store_file_to_gcs(
                temp_file_, file_name, content_type, signed_url=True
            )
            boxfile = create_boxfile(
                account_id=self.account_id,
                file_name=file_name,
                file_path=gcs_file["file_name"],
                content_type=gcs_file["content_type"],
                encryption_key=gcs_file["encryption_key"],
                document_type="transaction.transaction_confirmation",
            )
            transaction.add_transaction_confirmation(
                {
                    "id": boxfile.id,
                    "file_name": boxfile.file_name,
                    "document_type": boxfile.document_type,
                }
            )
        return gcs_file["signed_url"]
