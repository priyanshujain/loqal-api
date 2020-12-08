"""
User Banking related APIs
"""

from apps.provider.lib.api.api import API


class Banking(API):
    def create_bank_account(self, **kwargs):
        request_method = self.psp_client.banking.create_bank_account
        return self.execute_request(
            request_method=request_method, request_kwargs=kwargs
        )
