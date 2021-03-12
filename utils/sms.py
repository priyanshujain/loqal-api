import phonenumbers
from django.conf import settings

from plugins.twilio import TwilioPlugin


# TODO: implement sms feature
def sms_available():
    return True


def format_phone(phone_number, phone_number_country):
    return phonenumbers.format_number(
        phonenumbers.parse(phone_number, phone_number_country),
        phonenumbers.PhoneNumberFormat.E164,
    )


def send_sms(
    body, phone_number, phone_number_country=settings.DEFAULT_PHONE_REGION
):
    phone_from = format_phone(
        settings.LOQAL_SMS_PHONE_NUMBER,
        settings.LOQAL_SMS_PHONE_NUMBER_COUNTRY,
    )
    phone_to = format_phone(phone_number, phone_number_country)

    if (
        settings.APP_ENV == "local"
        or settings.APP_ENV == "development"
        # or settings.APP_ENV == "staging"
    ):
        print("###################### SMS START ########################")
        print("TO: ", phone_to)
        print("FROM: ", phone_from)
        print("CONTENT: ", body)
        print("###################### SMS END ##########################")
        return True

    try:
        twilio = TwilioPlugin()
        return twilio.send_text_message(phone_to, phone_from, body)
    except Exception:
        return False
