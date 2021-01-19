from apps.payment.dbapi.webhoooks import get_transaction 
from apps.account.dbapi.webhooks import get_account
from api.exceptions import ValidationError, ErrorDetail


class ApplyPaymentWebhook(object):
    def __init__(self, event, customer_account):
        self.event = event
        self.customer_account = customer_account

    def handle(self):
        topic = self.event.topic
        transaction_dwolla_id = self.event.target_resource_dwolla_id
        transaction = get_transaction(dwolla_id=transaction_dwolla_id)
        if not transaction:
            raise ValidationError({"detail": ErrorDetail("Invalid resource id for transfer.")})
        

        if topic == "customer_bank_transfer_created":
            # A bank transfer was created for a Customer. Represents funds moving either
            # from a verified Customer’s bank to the Dwolla network or from the
            # Dwolla network to a verified Customer’s bank.
            #
            # Note: As in our case only recevier is the verified customer we will assume it for receiver 
            transaction.mark_receiver_bank_trasfer_created()

        if topic == "customer_bank_transfer_creation_failed":
            # An attempt to initiate a transfer to a verified Customer’s bank was made,
            # but failed. Transfers initiated to a verified Customer’s bank must pass
            # through the verified Customer’s balance before being sent to a receiving bank.
            # Dwolla will fail to create a transaction intended for a verified
            # Customer’s bank if the funds available in the balance are less than
            # the transfer amount.
            transaction.mark_receiver_bank_trasfer_failed()

        if topic == "customer_bank_transfer_cancelled":
            # A pending Customer bank transfer has been cancelled, and will not process further.
            # Represents a cancellation of funds either transferring from a verified
            # Customer’s bank to the Dwolla network or from the Dwolla network to a
            # verified Customer’s bank.
            pass

        if topic == "customer_bank_transfer_failed":
            # A Customer bank transfer failed to clear successfully. Usually,
            # this is a result of an ACH failure (insufficient funds, etc.).
            # Represents funds failing to clear either from a verified
            # Customer’s bank to the Dwolla network or from the Dwolla
            # network to a verified Customer’s bank.
            pass

        if topic == "customer_bank_transfer_completed":
            # A bank transfer that was created for a Customer has cleared successfully.
            # Represents funds clearing either from a verified Customer’s bank to the
            # Dwolla network or from the Dwolla network to a verified Customer’s bank.
            pass

        if topic == "customer_transfer_created":
            # A transfer was created for a Customer. Represents funds transferring from a
            # verified Customer’s balance or unverified Customer’s bank
            pass

        if topic == "customer_transfer_cancelled":
            # A pending transfer has been cancelled, and will not process further.
            # Represents a cancellation of funds transferring either to an unverified
            # Customer’s bank or to a verified Customer’s balance.
            pass

        if topic == "customer_transfer_failed":
            # A Customer transfer failed to clear successfully. Represents funds
            # failing to clear either to an unverified Customer’s bank or to a
            # verified Customer’s balance.
            pass

        if topic == "customer_transfer_completed":
            # A Customer transfer has cleared successfully. Represents funds clearing
            # either to an unverified Customer’s bank or to a verified Customer’s balance.
            pass
