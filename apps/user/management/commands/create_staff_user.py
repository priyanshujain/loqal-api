from django.conf import settings
from django.core.management.base import BaseCommand

from apps.user.dbapi import create_staff_user, get_user_by_email


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("password", nargs="+", type=str)

    def handle(self, *args, **options):
        admin_email = settings.SPOTLIGHT_ADMIN_EMAIL
        password = options["password"][0]
        user = get_user_by_email(email=admin_email)
        if not user:
            user = create_staff_user(
                email=admin_email,
                password=password,
                first_name="Spotlight",
                last_name="Admin",
            )


