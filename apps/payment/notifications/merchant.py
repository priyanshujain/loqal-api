from apps.merchant.dbapi import get_members_by_account
from apps.notification.tasks import NotificationBase

__all__ = (
    "SendNewPaymentNotification",
    "SendRefundNotification",
    "SendRejectRequestNotification",
)


class SendSinglePaymentNotification(NotificationBase):
    def send_single_message(self, device):
        device.send_notification_message(
            title="New payment recieved",
            body="Click to view payment details",
            data_message={
                "action": "NEW_PAYMENT",
                "payload": self.data,
            },
        )


class SendNewPaymentNotification(object):
    def __init__(self, merchant_id, data):
        self.merchant_id = merchant_id
        self.data = data

    def send(self):
        members = get_members_by_account(merchant_id=self.merchant_id)
        for member in members:
            SendSinglePaymentNotification(
                user_id=member.user.id, data=self.data
            ).send()


class SendSingleRejectRequestNotification(NotificationBase):
    def send_single_message(self, device):
        device.send_data_message(
            data_message={
                "action": "PAYMENT_REQUEST_REJECTED",
                "payload": self.data,
            },
            content_available=True,
        )


class SendRejectRequestNotification(object):
    def __init__(self, merchant_id, data):
        self.merchant_id = merchant_id
        self.data = data

    def send(self):
        members = get_members_by_account(merchant_id=self.merchant_id)
        for member in members:
            SendSingleRejectRequestNotification(
                user_id=member.user.id, data=self.data
            ).send()


class SendRefundNotification(NotificationBase):
    def send_single_message(self, device):
        device.send_notification_message(
            title="New refund recieved",
            body="Click to view refund details",
            data_message={
                "action": "REFUND_RECEIVED",
                "payload": self.data,
            },
        )
