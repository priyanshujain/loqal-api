"""
User Payments related APIs
"""

from apps.provider.lib.api.api import API


class Reference(API):
    def business_classifcations(self, **kwargs):
        request_method = self.psp_client.reference.business_classifcations
        return self.execute_request(
            request_method=request_method, request_kwargs=kwargs
        )
