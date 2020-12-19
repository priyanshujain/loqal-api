from datetime import timedelta

from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.timezone import now

from apps.account.models import MerchantAccount
from apps.user.models import User
from db.models import AbstractBaseModel
from utils.shortcuts import rand_str


class FeatureAccessRole(AbstractBaseModel):
    merchant = models.ForeignKey(MerchantAccount, on_delete=models.CASCADE)
    role_name = models.CharField(max_length=256)
    description = models.CharField(max_length=1024, blank=True)
    team_and_roles = ArrayField(
        models.CharField(max_length=255, blank=True), default=list, blank=True
    )
    beneficiaries = ArrayField(
        models.CharField(max_length=255, blank=True), default=list, blank=True
    )
    transactions = ArrayField(
        models.CharField(max_length=255, blank=True), default=list, blank=True
    )
    banking = ArrayField(
        models.CharField(max_length=255, blank=True), default=list, blank=True
    )
    settings = ArrayField(
        models.CharField(max_length=255, blank=True), default=list, blank=True
    )
    is_super_admin = models.BooleanField(default=False)
    is_standard_user = models.BooleanField(default=False)
    is_editable = models.BooleanField(default=True)

    class Meta:
        unique_together = (
            "merchant",
            "role_name",
        )
        db_table = "merchant_account_role"

    def __str__(self):
        return self.role_name


class AccountMember(AbstractBaseModel):
    merchant = models.ForeignKey(MerchantAccount, on_delete=models.CASCADE)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    position = models.CharField(max_length=256, blank=True)
    account_active = models.BooleanField(default=False)
    role = models.ForeignKey(
        FeatureAccessRole, on_delete=models.CASCADE, blank=True, null=True
    )
    is_primary_member = models.BooleanField(default=False)

    def set_position(self, position):
        self.position = position
        self.save()

    def disable_member(self):
        user = self.user
        user.is_disbled = True
        user.save()

    def enable_member(self):
        user = self.user
        user.is_disbled = False
        user.save()

    def update_role(self, role_id):
        self.role_id = role_id
        self.save()

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
    role = models.ForeignKey(FeatureAccessRole, on_delete=models.CASCADE)
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

    def expire_invite_code(self):
        self.token_expires_at = now()
        self.save()

    def update_role(self, role_id):
        self.role_id = role_id
        self.save()

    class Meta:
        db_table = "merchant_member_invite"
