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

    def get_payment_failure(self, **kwargs):
        request_method = self.psp_client.payment.get_payment_failure
        return self.execute_request(
            request_method=request_method, request_kwargs=kwargs
        )
