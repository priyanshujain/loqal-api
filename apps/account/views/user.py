from django.utils.translation import gettext as _

from api.exceptions import ValidationError
from api.views import APIView
from apps.account.services import RegisterAccount
from apps.account.validators import RegisterAccountSerializer


class UserSignupAPI(APIView):
    serializer_class = RegisterAccountSerializer

    def post(self, request):
        serializer = self.get_serializer()
        if serializer.is_valid():
            self._run_services(data=serializer.data)
        else:
            raise ValidationError(serializer.errors)
        return self.response(status=201)

    def _run_services(self, data):
        service = RegisterAccount(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            company_name=data["company_name"],
            country=data["country"],
            contact_number=data["contact_number"],
            password=data["password"],
        )
        service.execute()

