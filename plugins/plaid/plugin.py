import re

from django.conf import settings
from plaid import Client
from plaid.api import accounts, institutions
from plaid.errors import InvalidInputError
from rest_framework.exceptions import ErrorDetail

from integrations.exceptions import IntegrationAPIError


class PlaidPlugin(object):
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
            environment=settings.PLAID_ENV,
        )

    @property
    def client(self):
        return self._client

    def create_link_token(self, user_account_id):
        """
        Exchange access_token with short lived public_token

        Args:
            - public_token: token returned by plaidLink after auth

        Returns:
            - access_token: access_token will be stored into DB and will
                            use for further auth purpose
        """
        try:
            self._link_token = self._client.LinkToken.create(
                {
                    "user": {
                        "client_user_id": user_account_id,
                    },
                    "products": ["auth"],
                    "client_name": getattr(
                        settings, "PLAID_APP_NAME", "Loqal"
                    ),
                    "country_codes": ["US"],
                    "language": "en",
                }
            ).get("link_token")
        except InvalidInputError:
            return None
        return self._link_token

    def exchange_public_token(self, public_token):
        """
        Exchange access_token with short lived public_token

        Args:
            - public_token: token returned by plaidLink after auth

        Returns:
            - access_token: access_token will be stored into DB and will
                            use for further auth purpose
        """
        try:
            self._access_token = self._client.Item.public_token.exchange(
                public_token
            ).get("access_token")
        except InvalidInputError:
            return None
        return self._access_token

    def get_dwolla_processor_token(self, access_token, account_id):
        """
        Create a processor token for a specific account id.
        """
        create_response = self._client.Processor.tokenCreate(
            access_token, account_id, "dwolla"
        )
        processor_token = create_response["processor_token"]
        return processor_token

    def get_bank_account(self, access_token, account_id):
        """
        Get account details for given account
        """
        # response = self._client.Auth.get(access_token, account_ids=[account_id])[
        #     "numbers"
        # ]
        try:
            auth_data = self._client.Auth.get(
                access_token, account_ids=[account_id]
            )
        except InvalidInputError:
            return None
        accounts = auth_data["accounts"]
        if not accounts:
            return {}

        bank_account = {"name": accounts[0]["name"]}
        institution_id = auth_data["item"]["institution_id"]
        bank_account["institution"] = self.get_institution(
            institution_id=institution_id
        )

        account_numbers = auth_data["numbers"].get("ach", [])
        for account in account_numbers:
            if account["account_id"] == account_id:
                bank_account["account_number"] = account.get("account")
                bank_account["aba_routing_number"] = account.get("routing")
                bank_account["wire_routing_number"] = account.get(
                    "wire_routing"
                )
        return bank_account

    def get_institution(self, institution_id):
        """
        Get institution name and logo for given institution_id
        """
        institution = self._client.Institutions.get_by_id(
            institution_id=institution_id,
            country_codes=["US"],
            _options={"include_optional_metadata": True},
        ).get(
            "institution",
        )

        return {
            "id": institution_id,
            "name": institution["name"],
            "logo_base64": institution["logo"],
        }

    def get_balance(self, access_token, account_id):
        """
        Get institution name and logo for given institution_id
        """
        accounts = self._client.Accounts.balance.get(
            access_token=access_token,
            account_ids=[account_id],
        ).get(
            "accounts",
        )
        if accounts and len(accounts) > 0:
            return float(accounts[0]["balances"]["available"])
        return None
