from integrations.dwolla.client import Client as DwollaClient
from integrations.options import IntegratedProviders
from integrations.plaid.client import PlaidClient

CLIENT_CLASSES = {
    IntegratedProviders.DWOLLA: DwollaClient,
    "PLAID": PlaidClient,
}
