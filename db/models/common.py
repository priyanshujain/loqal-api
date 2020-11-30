from django.db import models

from db.postgres.fields import JSONField
from utils.shortcuts import upload_to

from .base import Base


class BankAccountBase(models.Model):
    bank_account_country = models.CharField(max_length=50)
    currency = models.CharField(max_length=50)
    account_type = models.CharField(max_length=50, blank=True)
    account_number = models.CharField(max_length=50, blank=True)
    iban = models.CharField(max_length=50, blank=True)
    account_holder_name = models.CharField(max_length=200)
    address = JSONField(default=dict)
    bic_swift = models.CharField(max_length=50, blank=True)
    routing_code_type_1 = models.CharField(max_length=100, blank=True)
    routing_code_value_1 = models.CharField(max_length=100, blank=True)
    routing_code_type_2 = models.CharField(max_length=100, blank=True)
    routing_code_value_2 = models.CharField(max_length=100, blank=True)
    bank_name = models.CharField(max_length=100)
    bank_code = models.CharField(max_length=50, blank=True)
    bank_branch = models.CharField(max_length=50, blank=True)
    branch_code = models.CharField(max_length=100, blank=True)
    bank_address = JSONField(default=dict)

    class Meta:
        abstract = True


class IndividualBase(models.Model):
    first_name = models.CharField(max_length=512, blank=True)
    last_name = models.CharField(max_length=512, blank=True)
    middle_name = models.CharField(max_length=512, blank=True)
    dob = models.DateField(null=True)
    email = models.EmailField(blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True)
    id_type = models.CharField(max_length=128, blank=True)
    id_number = models.CharField(max_length=128, blank=True)
    id_expiration = models.DateField(null=True)
    country_of_id_issue = models.CharField(max_length=128, blank=True)
    address = JSONField(null=True, blank=True)

    class Meta:
        abstract = True
