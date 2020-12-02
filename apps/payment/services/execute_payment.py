from django.utils.translation import gettext as _
from rest_framework.exceptions import ErrorDetail

from api.exceptions import ErrorDetail, ProviderAPIException, ValidationError
from api.services import ServiceBase
from apps.direct_debit.dbapi import get_active_direct_debit_account
from apps.payment.dbapi import create_rate_quote, create_transaction
from apps.payment.shortcut import calculate_rate
from apps.provider.lib.actions import ProviderAPIActionBase
from apps.provider.options import IntegratedProviders
from integrations.exceptions import IntegrationAPIError
from integrations.utils.options import CommonStatusTypes


class CreatePaymentAPIAction(ProviderAPIActionBase):
    def create(self, data):
        response = self.client.payment.create(data=data)
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


class GetQuoteAPIAction(ProviderAPIActionBase):
    def create(self, data):
        response = self.client.payment.fetch_quotes(data=data)
        if self.get_errors(response):
            raise ProviderAPIException(
                {
                    "detail": ErrorDetail(
                        _(
                            "Payment service failed, please contact our support team."
                        )
                    )
                }
            )
        quote = response["data"]
        quote["payment_account_id"] = self.payment_account_id
        return quote


class ExecutePayment(ServiceBase):
    def __init__(self, payment_request):
        self.payment_request = payment_request
        self.account_id = payment_request.account.id

    def execute(self):
        quote_request_data = {
            "source_currency": self.payment_request.source_currency,
            "target_currency": self.payment_request.beneficiary.currency,
            "beneficiary_id": self.payment_request.beneficiary.id,
            "amount": self.payment_request.target_amount,
        }
        quotes = self._get_quotes(quote_request_data)
        best_quote = quotes[0]
        for quote in quotes:
            if quote.rate < best_quote.rate:
                best_quote = quote

        transaction = self._create_trasaction(best_quote)
        return transaction

    def _get_quotes(self, data):
        provider_quotes = []
        for provider_slug in IntegratedProviders.choices():
            provider_api_action = GetQuoteAPIAction(
                account_id=self.account_id, provider_slug=provider_slug
            )
            try:
                provider_respose = provider_api_action.create(data=data)
                provider_quotes.append(provider_respose)
            except IntegrationAPIError as err:
                # TODO: handle API errors
                raise ValidationError(err.errors)

        return [
            create_rate_quote(
                payment_account_id=quote_data["payment_account_id"],
                beneficiary_id=data["beneficiary_id"],
                provider_quote_id=quote_data["quote_id"],
                source_currency=quote_data["source_currency"],
                target_currency=quote_data["target_currency"],
                rate=calculate_rate(
                    quote_data["source_amount"], quote_data["target_amount"]
                ),
                target_amount=quote_data["target_amount"],
                expires_at=quote_data["expires_at"],
                quote_request_time=quote_data["quote_request_time"],
                quote_response_time=quote_data["quote_response_time"],
                expected_transaction_date=quote_data[
                    "expected_transaction_date"
                ],
            )
            for quote_data in provider_quotes
        ]

    def _create_trasaction(self, quote):
        direct_debit_account = get_active_direct_debit_account(
            account_id=self.account_id
        )
        trade_request_data = {
            "direct_debit_account_number": direct_debit_account.account_number,
            "target_amount": quote.target_amount,
            "purpose_of_payment": self.payment_request.purpose_of_payment,
            "purpose_of_payment_code": self.payment_request.purpose_of_payment_code,
            "provider_quote_id": quote.provider_quote_id,
            "source_currency": quote.source_currency,
            "target_currency": quote.target_currency,
            "expected_transaction_date": quote.expected_transaction_date,
            "beneficiary_id": quote.beneficiary.correlation_id,
        }
        provider_slug = quote.payment_account.provider.provider_slug
        provider_api_action = CreatePaymentAPIAction(
            account_id=self.account_id, provider_slug=provider_slug
        )
        provider_response = provider_api_action.create(data=trade_request_data)
        transaction = create_transaction(
            account_id=self.account_id,
            payment_request_id=self.payment_request.id,
            quote_id=quote.id,
            provider_transaction_id=provider_response[
                "provider_transaction_id"
            ],
            fee_value=provider_response["fee_value"],
            fee_currency=provider_response["fee_currency"],
        )
        if transaction:
            self.payment_request.set_executed()
        return transaction
