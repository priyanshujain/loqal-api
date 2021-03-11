from celery import shared_task
from django.template.loader import render_to_string

from apps.payment.dbapi.transaction import get_dispute
from utils.email import send_email_async


class SendPaymentInitiatedEmail(object):
    def __init__(self, transaction):
        self.user = transaction.payment.order.consumer.user
        self.transaction = transaction

    def send(self):
        self._send_email()

    def _send_email(self):
        user = self.user
        transaction = self.transaction
        source_bank_account = transaction.sender_bank_account
        source = f"{source_bank_account.bank_name} XXXX{source_bank_account.account_number_suffix}({source_bank_account.name})"
        recipient = transaction.payment.order.merchant.profile.full_name
        amount = f"${transaction.amount}"
        date_initiated = transaction.created_at.strftime(
            "%X %p (%Z) %A, %b %d, %Y"
        )
        render_data = {
            "source": source,
            "recipient": recipient,
            "amount": amount,
            "date_initiated": date_initiated,
        }
        email_html = render_to_string("payment_initiated.html", render_data)
        send_email_async(
            (user.email),
            f"New paytment initiated #{transaction.transaction_tracking_id}",
            email_html,
        )


class RefundReceivedEmail(object):
    def __init__(self, transaction):
        self.user = transaction.payment.order.consumer.user
        self.transaction = transaction

    def send(self):
        self._send_email()

    def _send_email(self):
        user = self.user
        transaction = self.transaction
        bank_account = transaction.recipient_bank_account
        source = f"{bank_account.bank_name} XXXX{bank_account.account_number_suffix}({bank_account.name})"
        merchant = transaction.payment.order.merchant.profile.full_name
        amount = f"${transaction.amount}"
        date_initiated = transaction.created_at.strftime(
            "%X %p (%Z) %A, %b %d, %Y"
        )
        render_data = {
            "source": source,
            "merchant": merchant,
            "amount": amount,
            "date_initiated": date_initiated,
        }
        email_html = render_to_string("refund_initiated.html", render_data)
        send_email_async(
            (user.email),
            f"Refund initiated for payment #{transaction.transaction_tracking_id}",
            email_html,
        )


class CreateDisputeConsumerEmail(object):
    def __init__(self, dispute):
        self.user = dispute.transaction.payment.order.consumer.user
        self.dispute = dispute

    def send(self):
        self._send_email()

    def _send_email(self):
        user = self.user
        dispute = self.dispute
        reason = dispute.reason_type.label
        description = dispute.reason_type
        render_data = {
            "reason": reason,
            "description": description,
        }
        email_html = render_to_string(
            "dispute_alert_consumer.html", render_data
        )
        send_email_async(
            (user.email),
            f"Payment dispute #{dispute.dispute_tracking_id}",
            email_html,
        )


@shared_task
def send_dispute_email(dispute_id):
    dispute = get_dispute(dispute_id=dispute_id)
    CreateDisputeConsumerEmail(dispute=dispute).send()


class SendPaymentCapturedEmail(object):
    def __init__(self, payment, email):
        self.consumer = payment.order.consumer
        self.payment = payment
        self.email = email

    def send(self):
        self._send_email()

    def _send_email(self):
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
        render_data = {
            "sender_name": f"{first_name} {last_name}",
            "loqal_id": consumer.username,
            "amount": amount,
            "date_initiated": date_initiated,
        }
        email_html = render_to_string("payment_captured.html", render_data)
        send_email_async(
            (self.email),
            f"New paytment captured #{payment.payment_tracking_id}",
            email_html,
        )
