from api.exceptions import ErrorDetail, ValidationError
from apps.payment.dbapi import create_transaction_event
from apps.payment.dbapi.webhoooks import get_transaction_by_dwolla_id
from apps.payment.options import (TransactionEventType,
                                  TransactionFailureReasonType,
                                  TransactionReceiverStatus,
                                  TransactionSenderStatus, TransactionStatus)

from .helpers import record_payment_failure


class ApplyPaymentWebhook(object):
    def __init__(self, event, customer_account, transaction=None):
        self.event = event
        self.customer_account = customer_account
        self.transaction = transaction

    def handle(self):
        topic = self.event.topic
        transaction = self.transaction
        if not transaction:
            transaction_dwolla_id = self.event.target_resource_dwolla_id
            transaction = get_transaction_by_dwolla_id(
                dwolla_id=transaction_dwolla_id
            )
            self.transaction = transaction
        if not transaction:
            return
        sender_account = transaction.sender_bank_account.account

        if topic == "customer_bank_transfer_created":
            """
            A bank transfer was created for a Customer. Represents funds moving either
            from a verified Customer’s bank to the Dwolla network or from the
            Dwolla network to a verified Customer’s bank.
            """
            if self.customer_account.is_verified_dwolla_customer:
                if sender_account.id == self.customer_account.id:
                    transaction.sender_status = (
                        TransactionSenderStatus.VC_BANK_TRANSFER_CREATED
                    )
                    transaction.save()
                    self._create_event(
                        event_type=TransactionEventType.SENDER_VC_BANK_TRANSFER_CREATED
                    )
                else:
                    transaction.receiver_status = (
                        TransactionReceiverStatus.VC_BANK_TRANSFER_CREATED
                    )
                    transaction.save()
                    self._create_event(
                        event_type=TransactionEventType.RECEIVER_VC_BANK_TRANSFER_CREATED
                    )

        if topic == "customer_bank_transfer_creation_failed":
            """
            An attempt to initiate a transfer to a verified Customer’s bank was made,
            but failed. Transfers initiated to a verified Customer’s bank must pass
            through the verified Customer’s balance before being sent to a receiving bank.
            Dwolla will fail to create a transaction intended for a verified
            Customer’s bank if the funds available in the balance are less than
            the transfer amount.
            """
            transaction.status = TransactionStatus.FAILED
            transaction.is_sender_failure = False
            transaction.failure_reason_type = (
                TransactionFailureReasonType.PRE_SETTLEMENT_INSUFFICIENT_BALANCE_AT_DESTINATION
            )
            transaction.failure_reason_message = (
                "An attempt to initiate a transfer to the"
                " Receiver’s bank was made, but failed. "
                "Transfers initiated to a verified Customer’s "
                "bank must pass through the verified Customer’s "
                "balance before being sent to a receiving bank. "
                "It will fail to create a transaction intended "
                "for a verified Customer’s bank if the funds available"
                " in the balance are less than the transfer amount."
            )
            transaction.receiver_status = (
                TransactionReceiverStatus.VC_BANK_TRANSFER_CREATION_FAILED
            )
            transaction.save()
            self._create_event(
                event_type=TransactionEventType.RECEIVER_VC_BANK_TRANSFER_CREATION_FAILED
            )

        if topic == "customer_bank_transfer_cancelled":
            """
            A pending Customer bank transfer has been cancelled, and will not process further.
            Represents a cancellation of funds either transferring from a verified
            Customer’s bank to the Dwolla network or from the Dwolla network to a
            verified Customer’s bank.
            """
            transaction.status = TransactionStatus.CANCELLED
            if self.customer_account.is_verified_dwolla_customer:
                if sender_account.id == self.customer_account.id:
                    transaction.sender_status = (
                        TransactionSenderStatus.VC_BANK_TRANSFER_CANCELLED
                    )
                    transaction.save()
                    self._create_event(
                        event_type=TransactionEventType.SENDER_VC_BANK_TRANSFER_CANCELLED
                    )
                else:
                    transaction.receiver_status = (
                        TransactionReceiverStatus.VC_BANK_TRANSFER_CANCELLED
                    )
                    transaction.save()
                    self._create_event(
                        event_type=TransactionEventType.RECEIVER_VC_BANK_TRANSFER_CANCELLED
                    )
            # TODO: Trigger an email to admin if any transaction is cancelled

        if topic == "customer_bank_transfer_failed":
            """
            A Customer bank transfer failed to clear successfully. Usually,
            this is a result of an ACH failure (insufficient funds, etc.).
            Represents funds failing to clear either from a verified
            Customer’s bank to the Dwolla network or from the Dwolla
            network to a verified Customer’s bank.
            """
            at_source = False
            if self.customer_account.is_verified_dwolla_customer:
                if sender_account.id == self.customer_account.id:
                    at_source = True
                    transaction.sender_status = (
                        TransactionSenderStatus.VC_BANK_TRANSFER_FAILED
                    )
                    self._create_event(
                        event_type=TransactionEventType.SENDER_VC_BANK_TRANSFER_FAILED
                    )
                else:
                    transaction.receiver_status = (
                        TransactionReceiverStatus.VC_BANK_TRANSFER_FAILED
                    )
                    self._create_event(
                        event_type=TransactionEventType.RECEIVER_VC_BANK_TRANSFER_FAILED
                    )

            failure_details = record_payment_failure(transaction, at_source)
            if not failure_details:
                transaction.save()

        if topic == "customer_bank_transfer_completed":
            """
            A bank transfer that was created for a Customer has cleared successfully.
            Represents funds clearing either from a verified Customer’s bank to the
            Dwolla network or from the Dwolla network to a verified Customer’s bank.
            """
            if self.customer_account.is_verified_dwolla_customer:
                if sender_account.id == self.customer_account.id:
                    transaction.sender_status = (
                        TransactionSenderStatus.VC_BANK_TRANSFER_COMPLETED
                    )
                    transaction.save()
                    self._create_event(
                        event_type=TransactionEventType.SENDER_VC_BANK_TRANSFER_COMPLETED
                    )
                else:
                    transaction.status = TransactionStatus.PROCESSED
                    transaction.receiver_status = (
                        TransactionReceiverStatus.VC_BANK_TRANSFER_COMPLETED
                    )
                    transaction.complete_receiver_transfer(save=False)
                    transaction.save()
                    self._create_event(
                        event_type=TransactionEventType.RECEIVER_VC_BANK_TRANSFER_COMPLETED
                    )

        if topic == "customer_transfer_created":
            """
            A transfer was created for a Customer. Represents funds transferring from a
            verified Customer’s balance or unverified Customer’s bank
            """
            if sender_account.id == self.customer_account.id:
                if self.customer_account.is_verified_dwolla_customer:
                    # FIX: check with dwolla on this event
                    transaction.sender_status = (
                        TransactionSenderStatus.VC_FROM_BALANCE_TRANSFER_CREATED
                    )
                    self._create_event(
                        event_type=TransactionEventType.SENDER_VC_FROM_BALANCE_TRANSFER_CREATED
                    )
                else:
                    transaction.sender_status = (
                        TransactionSenderStatus.UVC_BANK_TRANSFER_CREATED
                    )
                    self._create_event(
                        event_type=TransactionEventType.SENDER_UVC_BANK_TRANSFER_CREATED
                    )
            elif self.customer_account.is_verified_dwolla_customer:
                transaction.receiver_status = (
                    TransactionReceiverStatus.VC_TO_BALANCE_TRANSFER_CREATED
                )
                self._create_event(
                    event_type=TransactionEventType.RECEIVER_VC_TO_BALANCE_TRANSFER_CREATED
                )
            else:
                transaction.receiver_status = (
                    TransactionReceiverStatus.UVC_BANK_TRANSFER_CREATED
                )
                self._create_event(
                    event_type=TransactionEventType.RECEIVER_UVC_BANK_TRANSFER_CREATED
                )
            transaction.save()

        if topic == "customer_transfer_cancelled":
            """
            A pending transfer has been cancelled, and will not process further.
            Represents a cancellation of funds transferring either to an unverified
            Customer’s bank or to a verified Customer’s balance.
            """
            transaction.status = TransactionStatus.CANCELLED
            if sender_account.id == self.customer_account.id:
                if self.customer_account.is_verified_dwolla_customer:
                    # FIX: check with dwolla on this event
                    transaction.sender_status = (
                        TransactionSenderStatus.VC_FROM_BALANCE_TRANSFER_CANCELLED
                    )
                    self._create_event(
                        event_type=TransactionEventType.SENDER_VC_FROM_BALANCE_TRANSFER_CANCELLED
                    )
                else:
                    transaction.sender_status = (
                        TransactionSenderStatus.UVC_BANK_TRANSFER_CANCELLED
                    )
                    self._create_event(
                        event_type=TransactionEventType.SENDER_UVC_BANK_TRANSFER_CANCELLED
                    )
            elif self.customer_account.is_verified_dwolla_customer:
                transaction.receiver_status = (
                    TransactionReceiverStatus.VC_TO_BALANCE_TRANSFER_CANCELLED
                )
                self._create_event(
                    event_type=TransactionEventType.RECEIVER_VC_TO_BALANCE_TRANSFER_CANCELLED
                )
            else:
                transaction.receiver_status = (
                    TransactionReceiverStatus.UVC_BANK_TRANSFER_CANCELLED
                )
                self._create_event(
                    event_type=TransactionEventType.RECEIVER_UVC_BANK_TRANSFER_CANCELLED
                )
            transaction.save()

        if topic == "customer_transfer_failed":
            """
            A Customer transfer failed to clear successfully. Represents funds
            failing to clear either to an unverified Customer’s bank or to a
            verified Customer’s balance.
            """
            at_source = False
            if sender_account.id == self.customer_account.id:
                at_source = True
                if self.customer_account.is_verified_dwolla_customer:
                    # FIX: check with dwolla on this event
                    transaction.sender_status = (
                        TransactionSenderStatus.VC_FROM_BALANCE_TRANSFER_FAILED
                    )
                    self._create_event(
                        event_type=TransactionEventType.SENDER_VC_FROM_BALANCE_TRANSFER_FAILED
                    )
                else:
                    transaction.sender_status = (
                        TransactionSenderStatus.UVC_BANK_TRANSFER_FAILED
                    )
                    self._create_event(
                        event_type=TransactionEventType.SENDER_UVC_BANK_TRANSFER_FAILED
                    )
            elif self.customer_account.is_verified_dwolla_customer:
                transaction.receiver_status = (
                    TransactionReceiverStatus.VC_TO_BALANCE_TRANSFER_FAILED
                )
                self._create_event(
                    event_type=TransactionEventType.RECEIVER_VC_TO_BALANCE_TRANSFER_FAILED
                )
            else:
                transaction.receiver_status = (
                    TransactionReceiverStatus.UVC_BANK_TRANSFER_FAILED
                )
                self._create_event(
                    event_type=TransactionEventType.RECEIVER_UVC_BANK_TRANSFER_FAILED
                )
            failure_details = record_payment_failure(transaction, at_source)
            if not failure_details:
                transaction.save()

        if topic == "customer_transfer_completed":
            """
            A Customer transfer has cleared successfully. Represents funds clearing
            either to an unverified Customer’s bank or to a verified Customer’s balance.
            """
            if sender_account.id == self.customer_account.id:
                if self.customer_account.is_verified_dwolla_customer:
                    # FIX: check with dwolla on this event
                    transaction.sender_status = (
                        TransactionSenderStatus.VC_FROM_BALANCE_TRANSFER_COMPLETED
                    )
                    self._create_event(
                        event_type=TransactionEventType.SENDER_VC_FROM_BALANCE_TRANSFER_COMPLETED
                    )
                else:
                    transaction.sender_status = (
                        TransactionSenderStatus.UVC_BANK_TRANSFER_COMPLETED
                    )
                    self._create_event(
                        event_type=TransactionEventType.SENDER_UVC_BANK_TRANSFER_COMPLETED
                    )
                transaction.status = TransactionStatus.SENDER_COMPLETED
                transaction.complete_sender_transfer(save=False)
            elif self.customer_account.is_verified_dwolla_customer:
                transaction.receiver_status = (
                    TransactionReceiverStatus.VC_TO_BALANCE_TRANSFER_COMPLETED
                )
                self._create_event(
                    event_type=TransactionEventType.RECEIVER_VC_TO_BALANCE_TRANSFER_COMPLETED
                )
            else:
                transaction.status = TransactionStatus.PROCESSED
                transaction.receiver_status = (
                    TransactionReceiverStatus.UVC_BANK_TRANSFER_COMPLETED
                )
                transaction.complete_receiver_transfer(save=False)
                self._create_event(
                    event_type=TransactionEventType.RECEIVER_UVC_BANK_TRANSFER_COMPLETED
                )
            transaction.save()
        self.event.mark_processed()

    def _create_event(self, event_type, parameters={}):
        create_transaction_event(
            transaction_id=self.transaction.id,
            event_timestamp=self.event.event_timestamp,
            event_type=event_type,
            parameters=parameters,
        )
