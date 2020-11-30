from django.contrib.auth.models import AnonymousUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.user.models import User
from config.middlewares.user import local
from db.models.base import Base
from db.models.manager import BaseManager

__all__ = ("AbstractBase",)


class AbstractBase(Base):
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s_created_by_user",
        null=True,
        blank=True,
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s_updated_by_user",
        null=True,
        blank=True,
    )
    deleted_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s_deleted_by_user",
        null=True,
        blank=True,
    )

    objects = BaseManager()

    def save(self, *args, **kwargs):
        if (
            self.pk is None
            and hasattr(local, "user")
            and local.user.__class__ != AnonymousUser
        ):
            self.created_by = local.user
        elif (
            self.pk
            and hasattr(local, "user")
            and local.user.__class__ != AnonymousUser
        ):
            self.updated_by = local.user

        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if (
            self.pk
            and hasattr(local, "user")
            and local.user.__class__ != AnonymousUser
        ):
            self.deleted_by = local.user

        return super().delete(*args, **kwargs)

    class Meta:
        abstract = True
