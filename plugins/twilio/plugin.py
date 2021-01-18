import phonenumbers
from django.conf import settings
from twilio.rest import Client

from .errors import InValidPhoneNumber

MAX_SMS_LENGTH = 160


def validate_phone(phone):
    try:
        p = phonenumbers.parse(phone, settings.DEFAULT_PHONE_REGION)
    except phonenumbers.NumberParseException:
        return False
    if not phonenumbers.is_possible_number(p):
        return False
    if not phonenumbers.is_valid_number(p):
        return False
    return True


def clean_phone(phone):
    if not validate_phone(phone):
        raise InValidPhoneNumber
    return phonenumbers.format_number(
        phonenumbers.parse(phone, settings.DEFAULT_PHONE_REGION),
        phonenumbers.PhoneNumberFormat.E164,
    )


class TwilioPlugin(object):
    """
    Client implementation for the twilio API.
    """

    _client = None

    def __init__(self):
        """
        Initializes an instance of the twilio client
        """

        self._client = Client(
            username=settings.TWILIO_ACCOUNT_SID,
            password=settings.TWILIO_AUTH_TOKEN,
        )

    @property
    def client(self):
        return self._client

    def send_text_message(self, phone_to, phone_from, body):
        """
        Send a text message

        Args:
            - phone_to: Phone number of receiver

        Returns:
            - phone_from: Phone number of sender
        """
        phone_to = clean_phone(phone_to)
        phone_from = clean_phone(phone_from)
        message = self._client.messages.create(
            to=phone_to, from_=phone_from, body=body
        )
        import pdb

        pdb.set_trace()
        return message
