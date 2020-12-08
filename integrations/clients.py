from integrations.dwolla.client import Client as DwollaClient
from integrations.options import IntegratedProviders

CLIENT_CLASSES = {IntegratedProviders.DWOLLA: DwollaClient}
