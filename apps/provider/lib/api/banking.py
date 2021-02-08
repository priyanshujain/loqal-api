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

    def get_bank_accounts(self, **kwargs):
        request_method = self.psp_client.banking.get_bank_accounts
        return self.execute_request(
            request_method=request_method, request_kwargs=kwargs
        )

    def get_bank_account(self, **kwargs):
        request_method = self.psp_client.banking.get_bank_account
        return self.execute_request(
            request_method=request_method, request_kwargs=kwargs
        )

    def remove_bank_account(self, **kwargs):
        request_method = self.psp_client.banking.remove_bank_account
        return self.execute_request(
            request_method=request_method, request_kwargs=kwargs
        )

    def update_bank_account(self, **kwargs):
        request_method = self.psp_client.banking.update_bank_account
        return self.execute_request(
            request_method=request_method, request_kwargs=kwargs
        )
