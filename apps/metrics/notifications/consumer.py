from apps.notification.tasks import NotificationBase

__all__ = ("SendConsumerRatingNotification",)


class SendConsumerRatingNotification(NotificationBase):
    def send_single_message(self, device):
        device.send_data_message(
            data_message={
                "action": "NEW_THANKS_RECEIVED",
                "payload": self.data,
            },
            content_available=True,
        )
