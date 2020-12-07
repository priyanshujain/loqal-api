from datetime import timedelta

from django.db import models
from django.utils.timezone import now

from apps.account.models import Account
from db.models.abstract import AbstractBaseModel
from utils.shortcuts import upload_to


class BoxFile(AbstractBaseModel):
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, blank=True, null=True
    )
    file_name = models.CharField(max_length=512)
    file_path = models.CharField(max_length=512)
    content_type = models.CharField(max_length=256)
    document_type = models.CharField(max_length=512)
    encryption_key = models.CharField(max_length=64)

    def __str__(self):
        return self.file_name or "-"
