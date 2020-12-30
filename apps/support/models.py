from django.conf import settings
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import gettext as _

from db.models import BaseModel
from db.models.fields import ChoiceEnumField

from .options import IssueTypes


class SupportTicket(BaseModel):
    """
    This represents user device for push notification
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    message = models.TextField()
    issue_tracking_id = models.CharField(
        blank=True, null=True, default=None, unique=True, max_length=32
    )
    issue_type = ChoiceEnumField(
        enum_type=IssueTypes, default=IssueTypes.OTHER
    )

    class Meta:
        db_table = "support_ticket"

    def save(self, *args, **kwargs):
        def id_generator():
            return get_random_string(
                length=10, allowed_chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            )

        if not self.issue_tracking_id:
            self.issue_tracking_id = id_generator()
            while SupportTicket.objects.filter(
                issue_tracking_id=self.issue_tracking_id
            ).exists():
                self.issue_tracking_id = id_generator()
        return super().save(*args, **kwargs)
