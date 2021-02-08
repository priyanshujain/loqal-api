from django.conf import settings
from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.views import APIView, StaffAPIView
from apps.user.dbapi import (create_staff_user, get_admin_users,
                             get_user_by_email)
from apps.user.permissions import IsAdminStaffPermission, IsStaffPermission
from apps.user.responses import AdminUserProfileResponse
from apps.user.services import LoginRequest
from apps.user.validators import (AdminRoleChangeSerializer,
                                  AdminUserAddSerializer)


class UserLoginAPI(APIView):
    def post(self, request):
        throttle_scope = "login"

        if request.user.is_authenticated:
            raise ValidationError(
                {"detail": ErrorDetail(_("You are already logged in."))}
            )
        session = request.session
        if session:
            session.set_expiry(settings.SESSION_INACTIVITY_EXPIRATION_DURATION)

        service_response = self._run_services(request=request)
        if service_response:
            return self.response(service_response)
        return self.response()

    def _run_services(self, request):
        service = LoginRequest(request=request, data=self.request_data)
        return service.handle()


class AdminUserAddAPI(StaffAPIView):
    permission_classes = (IsAdminStaffPermission,)

    def post(self, request):
        data = self._validate_data()
        user = self._factory_admin_user(data)
        return self.response(AdminUserProfileResponse(user).data, status=201)

    def _validate_data(self):
        return run_validator(AdminUserAddSerializer, self.request_data)

    def _factory_admin_user(self, data):
        email = data["user_email"]
        password = data["password"]
        first_name = data["first_name"]
        last_name = data["last_name"]
        user_type = data["user_type"]

        user = get_user_by_email(email=email)
        if not user:
            user = create_staff_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                user_type=user_type,
            )
        return user


class ChangeAdminRoleAPI(StaffAPIView):
    permission_classes = (IsAdminStaffPermission,)

    def post(self, request):
        request_user = request.user
        data = self._validate_data(request_user=request_user)
        self._change_admin_role(data=data)
        return self.response(status=204)

    def _validate_data(self, request_user):
        data = run_validator(AdminRoleChangeSerializer, self.request_data)
        request_user_email = request_user.email
        if request_user_email == data["user_email"]:
            raise ValidationError(
                {"detail": ErrorDetail(_("Can you change own role type."))}
            )
        return data

    def _change_admin_role(self, data):
        email = data["user_email"]
        user_type = data["user_type"]

        user = get_user_by_email(email=email)
        if not user:
            raise ValidationError(
                {"user_email": [ErrorDetail(_("Invalid user."))]}
            )
        user.set_user_type(user_type=user_type)
        return user


class GetAdminUserAPI(StaffAPIView):
    permission_classes = (IsStaffPermission,)

    def get(self, request):
        admin_users = get_admin_users()
        return self.response(
            AdminUserProfileResponse(admin_users, many=True).data
        )
