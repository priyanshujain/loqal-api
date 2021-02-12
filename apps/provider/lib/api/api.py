"""
API request execution handling service.  
"""

import traceback

from integrations.utils.options import RequestStatusTypes


class API(object):
    """Base class for classes containing groups of API action."""

    def __init__(self, psp_client):
        self.psp_client = psp_client
        self.request_tracker = psp_client.config.request_tracker

    def execute_request(self, request_method, request_kwargs=None):
        response = {}
        errors = []
        try:
            response = request_method(**request_kwargs)
        except Exception as err:
            tb = traceback.format_exc()
            self.request_tracker.add_traceback(tb)
            try:
                errors = err.errors
                self.request_tracker.add_errors(errors)
            except AttributeError:
                pass
            return {
                "status": RequestStatusTypes.ERROR,
                "data": {},
                "errors": errors,
            }

        # TODO: Catch API error through an API error exception rather than this comparision
        if response.get("status") == RequestStatusTypes.ERROR:
            return response
        return {"status": RequestStatusTypes.SUCCESS, "data": response}
