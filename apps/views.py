from rest_framework.exceptions import NotFound

from api.views import APIView


class WelcomeAPI(APIView):
    def get(
        self,
        request,
    ):
        return self.response("Welcome to Loqal API")


def error404(request, exception):
    raise NotFound()
