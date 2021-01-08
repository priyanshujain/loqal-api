"""
User Management related APIs
"""

from apps.provider.lib.api.api import API


class Management(API):
    def create_webhook(self, **kwargs):
        request_method = self.psp_client.management.create_webhook
        return self.execute_request(
            request_method=request_method, request_kwargs=kwargs
        )
