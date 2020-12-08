from datetime import timedelta

from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.db.models.query_utils import select_related_descend
from django.utils.timezone import now

from apps.user.options import UserType
from db.models.base import Base
from utils.shortcuts import rand_str


class UserManager(models.Manager):
    use_in_migrations = True

    def get_by_natural_key(self, username):
        return self.get(**{f"{self.model.USERNAME_FIELD}__iexact": username})

    def find_by_username(self, username):
        queryset = self.get_queryset()
        return queryset.filter(username=username)

    def create_user(self, *arg, **kwargs):
        """Create and return a `User` with an email, username and password."""

        email = kwargs.get("email", None)
        password = kwargs.get("password", None)

        user = self.model(username=email, email=email)
        user.set_password(password)
        user.save()

        return user


class User(Base, AbstractBaseUser):
    username = models.CharField(max_length=254, unique=True)
    email = models.EmailField()
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(
        max_length=254, default=rand_str
    )
    email_verification_token_expire_time = models.DateTimeField(null=True)

    first_name = models.CharField(max_length=155, blank=True)
    last_name = models.CharField(max_length=155, blank=True)
    secondary_email = models.EmailField(max_length=255, blank=True)
    contact_number = models.CharField(max_length=255, blank=True)
    contact_number_verified = models.BooleanField(default=False)

    # One of UserType
    user_type = models.CharField(max_length=254, default=UserType.REGULAR_USER)
    # SSO auth token
    auth_token = models.CharField(max_length=254, null=True)
    # Two facotor auth
    two_factor_auth = models.BooleanField(default=False)
    tfa_token = models.CharField(max_length=254, blank=True)
    is_disabled = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def is_regular_staff(self):
        return self.user_type == UserType.REGULAR_STAFF

    def is_regular_user(self):
        return self.user_type == UserType.REGULAR_USER

    def is_admin_staff(self):
        return self.user_type == UserType.ADMIN_STAFF

    def is_staff(self):
        return self.user_type in [
            UserType.REGULAR_STAFF,
            UserType.ADMIN_STAFF,
        ]

    def set_user_type(self, user_type):
        self.user_type = user_type
        self.save()

    def verify_email(self):
        self.email_verified = True
        self.email_verification_token_expire_time = now()
        self.save()

    def gen_email_verification_token(self):
        self.email_verification_token = rand_str()
        self.email_verification_token_expire_time = now() + timedelta(days=7)
        self.save()

    def add_contact_number(self, contact_number):
        self.contact_number = contact_number
        self.save()

    def verify_contact_number(self):
        self.contact_number_verified = True
        self.save()

    def set_tfa_token(self, token):
        self.tfa_token = token
        self.save()

    def enable_tfa(self):
        self.two_factor_auth = True
        self.save()

    def disable_tfa(self):
        self.two_factor_auth = False
        self.save()

    class Meta:
        db_table = "user"


class UserSession(Base):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=512)
    user_agent = models.CharField(max_length=512)
    ip_address = models.GenericIPAddressField()
    is_ip_routable = models.BooleanField(default=True)
    # Storing it temporarily from cf_ip_country
    ip_country_iso = models.CharField(max_length=2, blank=True)
    last_activity = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True)
    country_iso = models.CharField(max_length=255, blank=True)
    region = models.CharField(max_length=255, blank=True)
    region_code = models.CharField(max_length=255, blank=True)
    latitude = models.CharField(max_length=255, blank=True)
    longitude = models.CharField(max_length=255, blank=True)
    timezone = models.CharField(max_length=255, blank=True)
    asn = models.CharField(max_length=255, blank=True)
    asn_code = models.CharField(max_length=255, blank=True)
    is_expired = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user) or "-"

    def update_latest(self, last_activity):
        self.last_activity = last_activity
        self.save()

    def expire_session(self):
        self.last_activity = now()
        self.is_expired = True
        self.save()

    class Meta:
        db_table = "user_session"


class UserPasswordReset(Base):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=254)
    token_expire_time = models.DateTimeField()

    def __str__(self):
        return str(self.user) or "-"

    @property
    def is_expired(self):
        return self.token_expire_time < now()

    def expire_token(self):
        self.token_expire_time = now()
        self.save()

    class Meta:
        db_table = "user_password_reset"
