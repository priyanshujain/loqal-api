from django.conf import settings
from django.template.loader import render_to_string

from utils.email import send_email_async

__all__ = (
    "MemberSignupInviteEmail",
)

class MemberSignupInviteEmail:
    def __init__(self, invite):
        self.invite = invite

    def send(self):
        invite_key = self.invite.invite_key
        invite_email = self.invite.email
        first_name = self.invite.first_name

        # Sending invited client email.
        key_path = f"/team/signup/{invite_key}"
        path = f"{settings.APP_BASE_URL}{key_path}"
        render_data = dict(path=path, username=first_name)

        email_html = render_to_string("member_signup_invite.html", render_data)
        send_email_async(
            (invite_email), "Signup invite for Spotlight Account", email_html
        )
