"""
Email tasks for user APIs
"""
from django.conf import settings
from django.template.loader import render_to_string

from utils.email import send_email_async


def send_forgot_password_email(user):
    render_data = {
        "username": user.username,
        "website_name": settings.APP_BASE_URL,
        "path": f"{settings.APP_BASE_URL}/user/forgot/key/{user.reset_password_token}",
    }
    email_html = render_to_string("reset_password_email.html", render_data)
    send_email_async((user.email), "Reset your password", email_html)
