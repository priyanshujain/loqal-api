from apps.provider.lib.api import Account


class APIClient(object):
    """
    Payment service API client.
    """

    def __init__(self, psp_client):
        self.psp_client = psp_client

        # Mirror the HTTP API hierarchy
        self.account = Account(psp_client=self.psp_client)
