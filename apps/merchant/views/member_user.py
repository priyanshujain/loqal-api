import re

from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.decorators.csrf import ensure_csrf_cookie

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.views import APIView, MerchantAPIView
from apps.merchant.dbapi import (get_account_member_by_user_id,
                                 update_account_member)
from apps.merchant.responses import MemberProfileResponse
from apps.merchant.validators import EditMemberProfileValidator
from apps.user.dbapi import get_user_by_phone


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

        if user.is_disabled:
            return self.response(
                {
                    "detail": ErrorDetail(
                        _(
                            "You member account has been disabled please contact our support team."
                        )
                    )
                },
                status=403,
            )

        return self.response(MemberProfileResponse(account_member).data)


class UpdateUserProfileAPI(MerchantAPIView):
    """
    Update user profile API
    """

    def put(self, request):
        data = run_validator(EditMemberProfileValidator, self.request_data)
        account_member = request.merchant_account_member
        user = request.user
        phone_number = data["phone_number"]
        assert self._validate_phone_number(
            user=user, phone_number=phone_number
        )
        update_account_member(
            user_id=user.id,
            member_id=account_member.id,
            first_name=data["first_name"],
            last_name=data["last_name"],
            position=data["position"],
            phone_number=data["phone_number"],
        )
        return self.response(status=204)

    def _validate_phone_number(self, user, phone_number):
        if user.phone_number and user.phone_number == phone_number:
            return True

        if get_user_by_phone(phone_number=phone_number):
            raise ValidationError(
                {
                    "phone_number": [
                        ErrorDetail(
                            _("A user already exists with this phone number.")
                        )
                    ]
                }
            )
        return True
