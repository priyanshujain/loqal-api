from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.timezone import now

from apps.account.models import MerchantAccount
from apps.payment.models import PaymentQrCode
from db.models import AbstractBaseModel
from db.models.fields import EncryptedCharField
from utils.shortcuts import rand_str


class PosStaff(AbstractBaseModel):
    merchant = models.ForeignKey(MerchantAccount, on_delete=models.CASCADE)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="merchant_pos_staff",
    )
    account_active = models.BooleanField(default=False)
    login_token = EncryptedCharField(max_length=2048, default=rand_str)
    login_pin = EncryptedCharField(
        max_length=1024,
        null=True,
        blank=True,
        default=None,
    )
    pin_last_updated = models.DateTimeField(default=now)
    shift_start = models.TimeField(null=True)
    shift_end = models.TimeField(null=True)
    login_token_expire_time = models.DateTimeField(default=now)
    register = models.ForeignKey(
        PaymentQrCode,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
    )
    staff_tracking_id = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        default=None,
        unique=True,
        editable=False,
    )

    def generate_pin(self, merchant_id, login_pin=None, save=False):
        def pin_generator():
            return get_random_string(length=6, allowed_chars="123456789")

        if not login_pin:
            login_pin = pin_generator()
            while PosStaff.objects.filter(
                login_pin=login_pin, merchant_id=merchant_id
            ).exists():
                login_pin = pin_generator()
        self.login_pin = login_pin
        self.pin_last_updated = now()
        if save:
            self.save()
        return login_pin

    def save(self, *args, **kwargs):
        def id_generator():
            return get_random_string(
                length=10, allowed_chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            )

        if not self.staff_tracking_id:
            self.staff_tracking_id = id_generator()
            while PosStaff.objects.filter(
                staff_tracking_id=self.staff_tracking_id
            ).exists():
                self.staff_tracking_id = id_generator()

        if not self.login_pin:
            self.generate_pin(merchant_id=self.merchant.id)
        return super().save(*args, **kwargs)

    def generate_login_token(self, save=True):
        self.login_token = rand_str()
        self.login_token_expire_time = now() + timedelta(days=30)
        if save:
            self.save()
        return self.login_token

    def get_login_token(self):
        if self.login_token_expire_time > now():
            return self.login_token
        return self.generate_login_token()

    def disable(self):
        user = self.user
        user.is_disabled = True
        user.save()

    def enable(self):
        user = self.user
        user.is_disabled = False
        user.save()

    def __str__(self):
        return self.user.first_name or "-"

    class Meta:
        db_table = "pos_staff"


class PosSession(AbstractBaseModel):
    staff = models.ForeignKey(
        PosStaff,
        on_delete=models.CASCADE,
        related_name="pos_session",
    )
    expires_at = models.DateTimeField(null=True)
    login_session = models.ForeignKey(
        "user.UserSession",
        on_delete=models.CASCADE,
        related_name="pos_session",
    )

    class Meta:
        db_table = "pos_session"

    def expire(self, save=True):
        self.expires_at = now()
        self.login_session.expire_session()
        if save:
            self.save()
