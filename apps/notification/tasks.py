from apps.notification.dbapi import get_device_by_id, get_devices_by_user

__all__ = (
    "NotificationBase",
    "SendEmailVerifiedNotification",
    "SendRefundNotification",
)


class NotificationBase(object):
    def __init__(self, user_id, device_id=None, data=None):
        self.user_id = user_id
        self.device_id = device_id
        self.data = data

    def send(self):
        if not self.device_id:
            devices = get_devices_by_user(user_id=self.user_id)
            if not devices.count() > 0:
                return False
            for device in devices:
                user_sessions = device.user_session
                for user_session in user_sessions.all():
                    if user_session.is_active:
                        self.send_single_message(device)
            return True

        device = get_device_by_id(
            user_id=self.user_id, device_id=self.device_id
        )
        if not device:
            return False
        self.send_single_message(device)
        return True


class SendEmailVerifiedNotification(NotificationBase):
    def send_single_message(self, device):
        device.send_data_message(
            data_message={
                "action": "EMAIL_VERIFIED",
                "payload": {"email_verified": True},
            },
            content_available=True,
        )


class SendRefundNotification(NotificationBase):
    def send_single_message(self, device):
        device.send_notification_message(
            title="Refund recieved",
            body="Click to view refund details",
            data_message={"data": self.data},
        )
