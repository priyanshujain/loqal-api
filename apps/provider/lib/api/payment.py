"""
User Payments related APIs
"""

from apps.provider.lib.api.api import API


class Payment(API):
    def create_new_payment(self, **kwargs):
        request_method = self.psp_client.payment.create_new_payment
        return self.execute_request(
            request_method=request_method, request_kwargs=kwargs
        )
