import threading

local = threading.local()

__all__ = (
    "local",
    "LocalUserMiddleware",
)


class LocalUserMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        local.user = request.user
        response = self.get_response(request)
        return response
