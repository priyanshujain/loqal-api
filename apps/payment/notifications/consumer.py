from apps.merchant.dbapi import get_members_by_account
from apps.notification.tasks import NotificationBase

__all__ = ("SendNewPaymentRequestNotification",)


class SendNewPaymentRequestNotification(NotificationBase):
    def send_single_message(self, device):
        device.send_notification_message(
            title="New payment request",
            body="Click to view details",
            data_message={
                "action": "NEW_PAYMENT_REQUEST",
                "payload": self.data,
            },
        )
