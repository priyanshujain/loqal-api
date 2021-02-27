from apps.merchant.dbapi import get_members_by_account
from apps.notification.tasks import NotificationBase

__all__ = ("SendNewPaymentRequestNotification",)


class SendNewPaymentRequestNotification(NotificationBase):
    def send_single_message(self, device):
        merchant_name = self.data["merchant"].get(
            "full_name", "Loqal merchant"
        )
        amount = self.data["amount"]

        device.send_notification_message(
            title="You received a new payment request",
            body=f"{merchant_name} has requested a payment of ${amount} for your purchase",
            data_message={
                "action": "NEW_PAYMENT_REQUEST",
                "payload": self.data,
            },
        )
