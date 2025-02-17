from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.services import ServiceBase
from api.views import merchant
from apps.account.dbapi import (create_merchant_account,
                                get_consumer_account_by_email)
from apps.account.notifications import SendMerchantAccountVerifyEmail
from apps.merchant.constants import DEFAULT_ROLE
from apps.merchant.dbapi import (create_account_member_on_reg,
                                 create_merchant_profile, get_super_admin_role)
from apps.merchant.models.member import FeatureAccessRole
from apps.payment.dbapi import (create_merchant_receive_limit,
                                create_payment_register)
from apps.user.dbapi import create_user, get_merchant_user_by_email
from apps.user.options import CustomerTypes

from .accept_merchant_terms import AcceptTerms

__all__ = ("CreateMerchantAccount",)


class CreateMerchantAccount(ServiceBase):
    def __init__(self, data, request):
        self.request = request
        self._first_name = data["first_name"]
        self._last_name = data["last_name"]
        self._email = data["email"]
        self._company_name = data["company_name"]
        self._contact_number = data["phone_number"]
        self._password = data["password"]
        self._address = data["address"]
        self._category = data["category"]
        self._sub_category = data["sub_category"]
        self._consent_timestamp = data["consent_timestamp"]
        self._payment_terms_url = data["payment_terms_url"]

    def handle(self):
        self._validate_data()
        merchant_account = self._factory_merchant_account()
        user = self._factory_user()
        role = self._factory_admin_role()
        account_member = create_account_member_on_reg(
            user_id=user.id,
            merchant_id=merchant_account.id,
            member_role_id=role.id,
        )
        self._send_verification_email(user=user)
        self._send_accepted_terms(account=merchant_account.account, user=user)
        return account_member

    def _validate_data(self):
        user = get_merchant_user_by_email(email=self._email)
        if user:
            raise ValidationError(
                {
                    "email": [
                        ErrorDetail(
                            _("A user with this email already exists.")
                        )
                    ]
                }
            )

        user = get_consumer_account_by_email(email=self._email)
        if user:
            raise ValidationError(
                {
                    "detail": [
                        ErrorDetail(
                            _(
                                "You already signed for a Loqal app user account "
                                "with this email. Please use a different email."
                            )
                        )
                    ]
                }
            )

    def _factory_merchant_account(self):
        merchant_account = create_merchant_account(company_email=self._email)
        create_merchant_profile(
            merchant_id=merchant_account.id,
            name=self._company_name,
            address=self._address,
            category=self._category,
            sub_category=self._sub_category,
            phone_number=self._contact_number,
        )
        self._factory_payment_register(
            account_id=merchant_account.account.id,
            merchant_id=merchant_account.id,
        )
        return merchant_account

    def _factory_payment_register(self, account_id, merchant_id):
        create_payment_register(account_id=account_id)
        create_merchant_receive_limit(merchant_id=merchant_id)

    def _factory_user(self):
        return create_user(
            first_name=self._first_name,
            last_name=self._last_name,
            email=self._email,
            phone_number=self._contact_number,
            password=self._password,
            customer_type=CustomerTypes.MERCHANT,
        )

    def _factory_admin_role(self):
        return FeatureAccessRole.objects.create(
            is_full_access=True, is_super_admin=True, **DEFAULT_ROLE
        )

    def _send_verification_email(self, user):
        SendMerchantAccountVerifyEmail(user=user).send()

    def _send_accepted_terms(self, account, user):
        AcceptTerms(
            request=self.request,
            account=account,
            user=user,
            data={
                "consent_timestamp": self._consent_timestamp,
                "payment_terms_url": self._payment_terms_url,
            },
        ).handle()
