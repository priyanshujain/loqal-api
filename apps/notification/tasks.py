from apps.notification.dbapi import get_device_by_id

__all__ = (
    "SendEmailVerifiedNotification",
    "SendNewPaymentNotification",
    "SendRefundNotification",
)


class SendEmailVerifiedNotification(object):
    def __init__(self, user_id, device_id):
        self.user_id = user_id
        self.device_id = device_id

    def send(self):
        if not self.device_id:
            return
        device = get_device_by_id(user_id=self.user_id, device_id=self.device_id)
        if not device:
            return
        device.send_data_message(
            data_message={
                "action": "EMAIL_VERIFIED",
                "payload": {"email_verified": True},
            },
            content_available=True,
        )


class SendNewPaymentNotification(object):
    def __init__(self, user_id, device_id, data):
        self.user_id = user_id
        self.device_id = device_id
        self.data = data

    def send(self):
        if not self.device_id:
            return
        device = get_device_by_id(user_id=self.user_id, device_id=self.device_id)
        if not device:
            return
        device.send_notification_message(
            title="New payment recieved",
            body="Click to view payment details",
            data_message={"data": self.data},
        )


class SendRefundNotification(object):
    def __init__(self, user_id, device_id, data):
        self.user_id = user_id
        self.device_id = device_id
        self.data = data

    def send(self):
        if not self.device_id:
            return
        device = get_device_by_id(user_id=self.user_id, device_id=self.device_id)
        if not device:
            return
        device.send_notification_message(
            title="Refund recieved",
            body="Click to view refund details",
            data_message={"data": self.data},
        )
