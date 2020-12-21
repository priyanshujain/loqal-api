"""
User Account related APIs
"""

from apps.provider.lib.api.api import API


class Account(API):
    def create_consumer_account(self, **kwargs):
        request_method = self.psp_client.account.create_consumer_account
        return self.execute_request(
            request_method=request_method, request_kwargs=kwargs
        )

    def create_merchant_account(self, **kwargs):
        request_method = self.psp_client.account.create_merchant_account
        return self.execute_request(
            request_method=request_method, request_kwargs=kwargs
        )
    
    def add_beneficial_owner(self, **kwargs):
        request_method = self.psp_client.account.add_beneficial_owner
        return self.execute_request(
            request_method=request_method, request_kwargs=kwargs
        )
    
    def certify_beneficial_owner(self, **kwargs):
        request_method = self.psp_client.account.certify_beneficial_owner
        return self.execute_request(
            request_method=request_method, request_kwargs=kwargs
        )
