from django.utils.deprecation import MiddlewareMixin

__all__ = (
    "AddXCsrfMiddleware",
    "PreventAuthenticatePromptMiddleware",
)


class AddXCsrfMiddleware(MiddlewareMixin):
    def process_request(self, request):
        cookies = request.COOKIES
        if "csrftoken" in cookies.keys():
            request.META["HTTP_X_CSRFTOKEN"] = cookies["csrftoken"]


# NOTE: Remove WWW-Authenticate header, in case browser popup login window when 401
class PreventAuthenticatePromptMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response and response.status_code == 401:
            del response["WWW-Authenticate"]
        return response
