from apps.provider.lib.api.banking import Banking
from apps.provider.lib.api import Account, Banking


class APIClient(object):
    """
    Payment service API client.
    """

    def __init__(self, psp_client):
        self.psp_client = psp_client

        # Mirror the HTTP API hierarchy
        self.account = Account(psp_client=self.psp_client)
        self.banking = Banking(psp_client=self.psp_client)
