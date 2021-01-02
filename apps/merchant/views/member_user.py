from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.decorators.csrf import ensure_csrf_cookie

from api.helpers import run_validator
from api.views import APIView, MerchantAPIView
from apps.user.dbapi import update_user_profile
from apps.user.responses.merchant import UserProfileResponse
from apps.user.validators import EditProfileValidator
from apps.merchant.dbapi import get_account_member_by_user_id


class GetUserProfileAPI(APIView):
    """
    Get user profile API
    - View user profile.
    - Also used for checking if user is logged In.
    """

    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        # TODO: Revisit status of this API, discuss with @adi
        user = request.user
        if not user.is_authenticated:
            return self.response()
        
        account_member = get_account_member_by_user_id(user_id=user.id)
        if not account_member:
            return self.response()

        return self.response(UserProfileResponse(user).data)


class UpdateUserProfileAPI(MerchantAPIView):
    """
    Update user profile API
    """

    def put(self, request):
        data = run_validator(EditProfileValidator, self.request_data)
        user = request.user
        update_user_profile(
            user=user,
            first_name=data["first_name"],
            last_name=data["last_name"],
        )
        return self.response(status=204)
