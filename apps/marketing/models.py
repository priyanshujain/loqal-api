from django.conf import settings
from django.db import models

from db.models import AbstractBaseModel


class Campaign(AbstractBaseModel):
    title = models.CharField(max_length=256, unique=True)
    short_description = models.CharField(blank=True, max_length=1024)
    content = models.TextField(null=True, blank=True)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    target_amount = models.DecimalField(
        max_digits=10,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0,
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "campaign"

    def deactivate_campaign(self, save=True):
        self.is_active = False
        if save:
            self.save()

    def activate_campaign(self, save=True):
        self.is_active = True
        if save:
            self.save()
