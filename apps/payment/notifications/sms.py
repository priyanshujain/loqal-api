from utils.sms import send_sms


class SendPaymentCapturedSMS(object):
    def __init__(self, payment, phone_number, phone_number_country):
        self.consumer = payment.order.consumer
        self.payment = payment
        self.phone_number = phone_number
        self.phone_number_country = phone_number_country

    def send(self):
        self._send_email()

    def _send_sms(self):
        consumer = self.consumer
        payment = self.payment
        first_name = consumer.user.first_name
        last_name = consumer.user.last_name
        if len(last_name) > 0:
            last_name - last_name[0]
        amount = f"${payment.captured_amount}"
        date_initiated = payment.created_at.strftime(
            "%X %p (%Z) %A, %b %d, %Y"
        )
        sms_body = (
            f"A new Loqal payment captured from {first_name} "
            f"{last_name}({consumer.username}).\n\n",
            f"Amount: {amount}\n",
            f"Time: {date_initiated}",
        )
        send_sms(
            body=sms_body,
            phone_number=self.phone_number,
            phone_number_country=self.phone_number_country,
        )
