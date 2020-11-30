# System imports
import uuid

# Django imports
from django.db import models


class Base(models.Model):
    # A unique id as string but not PK as we dont't want to expose PK's
    u_id = models.UUIDField(
        primary_key=False, default=uuid.uuid4, editable=False
    )

    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # A timestamp reprensenting when this object was last updated.
    updated_at = models.DateTimeField(auto_now=True)

    # A timestamp reprensenting when this object was soft deleted.
    deleted_at = models.DateTimeField(null=True, blank=True)

    # deleted parameter for soft delete
    deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

        # By default, any model that inherits from `Base` should be ordered in
        # reverse-chronological order.
        ordering = ["-created_at", "-updated_at"]
