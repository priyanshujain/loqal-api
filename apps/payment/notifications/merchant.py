from apps.merchant.dbapi import get_members_by_account
from apps.notification.dbapi import get_device_by_id, get_devices_by_user

__all__ = (
    "SendNewPaymentNotification",
    "SendRefundNotification",
)


class SendNewPaymentNotification(object):
    def __init__(self, merchant_id, data):
        self.merchant_id = merchant_id
        self.data = data

    def send(self):
        members = get_members_by_account(merchant_id=self.merchant_id)
        for member in members:
            devices = get_devices_by_user(user_id=member.user.id)
            for device in devices:
                device.send_notification_message(
                    title="New payment recieved",
                    body="Click to view payment details",
                    data_message={
                        "action": "NEW_PAYMENT",
                        "payload": self.data,
                    },
                )


class SendRefundNotification(object):
    def __init__(self, user_id, data):
        self.user_id = user_id
        self.data = data

    def send(self):
        devices = get_devices_by_user(user_id=self.user_id)
        for device in devices:
            device.send_notification_message(
                title="New refund recieved",
                body="Click to view refund details",
                data_message={
                    "action": "REFUND_RECEIVED",
                    "payload": self.data,
                },
            )
