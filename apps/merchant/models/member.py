from datetime import timedelta
from re import I

from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.timezone import now

from apps.account.models import MerchantAccount
from apps.merchant.options import FeatureAcessTypes
from db.models import AbstractBaseModel
from db.models.fields import ChoiceCharEnumField, EncryptedCharField
from utils.shortcuts import rand_str


class FeatureAccessRole(AbstractBaseModel):
    payment_requests = ArrayField(
        ChoiceCharEnumField(max_length=255, enum_type=FeatureAcessTypes),
        default=list,
        blank=True,
    )
    payment_history = ArrayField(
        ChoiceCharEnumField(max_length=255, enum_type=FeatureAcessTypes),
        default=list,
        blank=True,
    )
    settlements = ArrayField(
        ChoiceCharEnumField(max_length=255, enum_type=FeatureAcessTypes),
        default=list,
        blank=True,
    )
    disputes = ArrayField(
        ChoiceCharEnumField(max_length=255, enum_type=FeatureAcessTypes),
        default=list,
        blank=True,
    )
    refunds = ArrayField(
        ChoiceCharEnumField(max_length=255, enum_type=FeatureAcessTypes),
        default=list,
        blank=True,
    )
    customers = ArrayField(
        ChoiceCharEnumField(max_length=255, enum_type=FeatureAcessTypes),
        default=list,
        blank=True,
    )
    bank_accounts = ArrayField(
        ChoiceCharEnumField(max_length=255, enum_type=FeatureAcessTypes),
        default=list,
        blank=True,
    )
    qr_codes = ArrayField(
        ChoiceCharEnumField(max_length=255, enum_type=FeatureAcessTypes),
        default=list,
        blank=True,
    )
    store_profile = ArrayField(
        ChoiceCharEnumField(max_length=255, enum_type=FeatureAcessTypes),
        default=list,
        blank=True,
    )
    team_management = ArrayField(
        ChoiceCharEnumField(max_length=255, enum_type=FeatureAcessTypes),
        default=list,
        blank=True,
    )
    top_customers = ArrayField(
        ChoiceCharEnumField(max_length=255, enum_type=FeatureAcessTypes),
        default=list,
        blank=True,
    )
    loyalty_program = ArrayField(
        ChoiceCharEnumField(max_length=255, enum_type=FeatureAcessTypes),
        default=list,
        blank=True,
    )
    merchant_settings = ArrayField(
        ChoiceCharEnumField(max_length=255, enum_type=FeatureAcessTypes),
        default=list,
        blank=True,
    )
    is_full_access = models.BooleanField(default=False)
    is_super_admin = models.BooleanField(default=False)
    is_standard_user = models.BooleanField(default=False)
    is_editable = models.BooleanField(default=True)

    class Meta:
        db_table = "merchant_account_role"


class AccountMember(AbstractBaseModel):
    merchant = models.ForeignKey(MerchantAccount, on_delete=models.CASCADE)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="merchant_account_member",
    )
    position = models.CharField(max_length=256, blank=True)
    account_active = models.BooleanField(default=False)
    role = models.OneToOneField(
        FeatureAccessRole,
        related_name="account_member",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    is_primary_member = models.BooleanField(default=False)

    def set_position(self, position):
        self.position = position
        self.save()

    def disable_member(self):
        user = self.user
        user.is_disabled = True
        user.save()

    def enable_member(self):
        user = self.user
        user.is_disabled = False
        user.save()

    def __str__(self):
        return self.user.first_name or "-"

    class Meta:
        db_table = "merchant_account_member"


class MemberInvite(AbstractBaseModel):
    merchant = models.ForeignKey(MerchantAccount, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, unique=True)
    position = models.CharField(max_length=256, blank=True)
    role = models.OneToOneField(
        FeatureAccessRole,
        related_name="member_invite",
        on_delete=models.CASCADE,
    )
    token = models.CharField(max_length=512, blank=True)
    token_expires_at = models.DateTimeField(default=None, null=True)

    @property
    def is_expired(self):
        """
        Check if invite is expired
        """
        return self.token_expires_at < now()

    @classmethod
    def account_invites(cls, merchant_id):
        """
        List of active invites for an account
        """
        invites = cls.objects.filter(merchant_id=merchant_id)
        if not invites.exists():
            return []
        return [invite for invite in invites if invite.is_expired == False]

    def generate_invite_token(self):
        self.token = rand_str()
        self.token_expires_at = now() + timedelta(days=7)
        self.save()

    def expire_token(self):
        self.token_expires_at = now()
        self.save()

    class Meta:
        db_table = "merchant_member_invite"
