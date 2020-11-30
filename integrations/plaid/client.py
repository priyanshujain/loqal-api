from django.conf import settings
from plaid import Client
from plaid.errors import InvalidInputError

from integrations.exceptions import IntegrationAPIError

from .fields import CountryAdapterMap
from .options import PlaidAccountTypeMap


class PlaidClient:
    """
    Client implementation for the Plaid API.
    """

    _client = None
    _access_token = None

    def __init__(self):
        """
        Initializes an instance of the plaid client
        """

        self._client = Client(
            client_id=settings.PLAID_CLIENT_ID,
            secret=settings.PLAID_SECRET,
            public_key=settings.PLAID_PUBLIC_KEY,
            environment=settings.PLAID_ENV,
        )

    @property
    def client(self):
        return self._client

    def _get_fields_adater(self, country_code):
        return getattr(CountryAdapterMap, country_code)

    def exchange_public_token(self, public_token):
        """
        Exchange access_token with short lived public_token

        Args:
            - public_token: token returned by plaidLink after auth

        Returns:
            - access_token: access_token will be stored into DB and will
                            use for further auth purpose
        """

        self._access_token = self._client.Item.public_token.exchange(
            public_token
        ).get("access_token")
        return self._access_token

    def get_account_details(self, access_token, country_code, account_id):
        response = self._client.Auth.get(
            access_token, account_ids=[account_id]
        )["numbers"]
        account_type = getattr(PlaidAccountTypeMap, country_code)
        accounts = response.get(account_type, [])
        for account in accounts:
            if account["account_id"] == account_id:
                account_adapter = getattr(CountryAdapterMap, country_code)
                return account_adapter().adapt(account)
        return {}

    def get_institution(self, bank_id):
        try:
            return self._client.Institutions.get_by_id(
                institution_id=bank_id
            ).get("institution")
        except InvalidInputError:
            raise IntegrationAPIError({"bank_id": "Invalid bank_id"})
