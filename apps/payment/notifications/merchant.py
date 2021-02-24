from apps.merchant.dbapi import get_members_by_account
from apps.notification.tasks import NotificationBase

__all__ = (
    "SendNewPaymentNotification",
    "SendRefundNotification",
    "SendRejectRequestNotification",
    "SendApproveRequestNotification",
)


class SendSinglePaymentNotification(NotificationBase):
    def send_single_message(self, device):
        amount = self.data["amount"]
        first_name = self.data["customer"]["first_name"]
        last_name = self.data["customer"]["last_name"]
        device.send_notification_message(
            title="New payment recieved",
            body=f"You received a payment of ${amount} from {first_name} {last_name}",
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


class SendSingleApproveRequestNotification(NotificationBase):
    def send_single_message(self, device):
        device.send_data_message(
            data_message={
                "action": "PAYMENT_REQUEST_APPROVED",
                "payload": self.data,
            },
            content_available=True,
        )


class SendApproveRequestNotification(object):
    def __init__(self, merchant_id, data):
        self.merchant_id = merchant_id
        self.data = data

    def send(self):
        members = get_members_by_account(merchant_id=self.merchant_id)
        for member in members:
            SendSingleApproveRequestNotification(
                user_id=member.user.id, data=self.data
            ).send()


class SendRefundNotification(NotificationBase):
    def send_single_message(self, device):
        merchant_name = self.data["merchant"].get("full_name", "Loqal merchant")
        amount = self.data["amount"]
        device.send_notification_message(
            title="Refund recieved",
            body=f"You received a refund of ${amount} from {merchant_name}",
            data_message={
                "action": "REFUND_RECEIVED",
                "payload": self.data,
            },
        )
