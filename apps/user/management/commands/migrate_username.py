from django.core.management.base import BaseCommand

from apps.user.models import User
from apps.user.options import CustomerTypes, UserType


class Command(BaseCommand):
    def handle(self, *args, **options):
        for user in User.objects.all():
            try:
                consumer_account = user.consumer_account
                if consumer_account:
                    if "::" not in user.username:
                        user.customer_type = CustomerTypes.CONSUMER
                        user.username = (
                            f"{user}::{CustomerTypes.CONSUMER.value}"
                        )
                        user.save()
                        continue
            except Exception:
                pass
            try:
                merchant_account_member = user.merchant_account_member
                if merchant_account_member:
                    if "::" not in user.username:
                        user.customer_type = CustomerTypes.MERCHANT
                        user.username = (
                            f"{user}::{CustomerTypes.MERCHANT.value}"
                        )
                        user.save()
                        continue
            except Exception:
                pass
            try:
                if user.user_type != UserType.REGULAR_USER:
                    if "::" not in user.username:
                        user.customer_type = CustomerTypes.INTERNAL
                        user.username = (
                            f"{user}::{CustomerTypes.INTERNAL.value}"
                        )
                        user.save()
            except Exception:
                pass
