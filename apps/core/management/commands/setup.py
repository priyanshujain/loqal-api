from django.conf import settings
from django.core.management.base import BaseCommand

from apps.user.dbapi import create_staff_user, get_user_by_email


class Command(BaseCommand):
    def handle(self, *args, **options):
        admin_email = settings.SPOTLIGHT_ADMIN_EMAIL
        admin_password = settings.INITIAL_ADMIN_PASSWORD
        user = get_user_by_email(email=admin_email)
        if not user:
            user = create_staff_user(
                email=admin_email,
                password=admin_password,
                first_name="Loqal",
                last_name="Admin",
            )
