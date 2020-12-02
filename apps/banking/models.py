from os import name

from django.db import models

from apps.account.models import Account
from db.models.abstract import AbstractBase


class BankAccount(AbstractBase):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    plaid_access_token = models.CharField(max_length=255)
    plaid_account_id = models.CharField(max_length=255)
    account_number_suffix = models.CharField(max_length=4)
    name = models.CharField(max_length=64)
    bank_name = models.CharField(max_length=1024)
    bank_logo_base64 = models.TextField()
    currency = models.CharField(max_length=3, default="USD")
    is_disabled = models.BooleanField(default=False)
    dwolla_id = models.CharField(max_length=255, blank=True)

    def add_dwolla_id(self, dwolla_id):
        self.dwolla_id = dwolla_id
        self.save()

    class Meta:
        db_table = "bank_account"
