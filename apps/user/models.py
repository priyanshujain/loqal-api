from datetime import timedelta

import six
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.db.models.query_utils import select_related_descend
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from apps.user.options import UserType
from db.models.base import Base
from db.models.fields import (BoundedPositiveIntegerField,
                              EncryptedPickledObjectField)
from lib.auth.authenticators import (AUTHENTICATOR_CHOICES,
                                     AUTHENTICATOR_INTERFACES,
                                     AUTHENTICATOR_INTERFACES_BY_TYPE,
                                     available_authenticators)
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






class AuthenticatorManager(models.Manager):
    def all_interfaces_for_user(
        self, user, return_missing=False, ignore_backup=False
    ):
        """Returns a correctly sorted list of all interfaces the user
        has enabled.  If `return_missing` is set to `True` then all
        interfaces are returned even if not enabled.
        """

        def _sort(x):
            return sorted(x, key=lambda x: (x.type == 0, x.type))

        # Collect interfaces user is enrolled in
        ifaces = [
            x.interface
            for x in Authenticator.objects.filter(
                user=user,
                type__in=[
                    a.type
                    for a in available_authenticators(
                        ignore_backup=ignore_backup
                    )
                ],
            )
        ]

        if return_missing:
            # Collect additional interfaces that the user
            # is not enrolled in
            rvm = dict(AUTHENTICATOR_INTERFACES)
            for iface in ifaces:
                rvm.pop(iface.interface_id, None)
            for iface_cls in six.itervalues(rvm):
                if iface_cls.is_available:
                    ifaces.append(iface_cls())

        return _sort(ifaces)

    def get_interface(self, user, interface_id):
        """Looks up an interface by interface ID for a user.  If the
        interface is not available but configured a
        `Authenticator.DoesNotExist` will be raised just as if the
        authenticator was not configured at all.
        """
        interface = AUTHENTICATOR_INTERFACES.get(interface_id)
        if interface is None or not interface.is_available:
            raise LookupError("No such interface %r" % interface_id)
        try:
            return Authenticator.objects.get(
                user=user, type=interface.type
            ).interface
        except Authenticator.DoesNotExist:
            return interface()

    def user_has_2fa(self, user):
        """Checks if the user has any 2FA configured.
        """
        return Authenticator.objects.filter(
            user=user,
            type__in=[
                a.type for a in available_authenticators(ignore_backup=True)
            ],
        ).exists()

    def bulk_users_have_2fa(self, user_ids):
        """Checks if a list of user ids have 2FA configured.
        Returns a dict of {<id>: <has_2fa>}
        """
        authenticators = set(
            Authenticator.objects.filter(
                user__in=user_ids,
                type__in=[
                    a.type
                    for a in available_authenticators(ignore_backup=True)
                ],
            )
            .distinct()
            .values_list("user_id", flat=True)
        )
        return {id: id in authenticators for id in user_ids}


class Authenticator(Base):

    user = models.OneToOneField(User, on_delete=models.CASCADE, db_index=True)
    type = BoundedPositiveIntegerField(choices=AUTHENTICATOR_CHOICES)
    config = EncryptedPickledObjectField()

    objects = AuthenticatorManager()

    class AlreadyEnrolled(Exception):
        pass

    class Meta:
        db_table = "auth_authenticator"
        verbose_name = _("authenticator")
        verbose_name_plural = _("authenticators")
        unique_together = (("user", "type"),)

    @cached_property
    def interface(self):
        return AUTHENTICATOR_INTERFACES_BY_TYPE[self.type](self)

    def mark_used(self, save=True):
        self.last_used_at = timezone.now()
        if save:
            self.save()

    def reset_fields(self, save=True):
        self.created_at = timezone.now()
        self.last_used_at = None
        if save:
            self.save()


