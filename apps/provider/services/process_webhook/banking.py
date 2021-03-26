from apps.banking.dbapi import get_bank_account_by_dwolla_id
from apps.banking.options import DwollaFundingSourceStatus, MicroDepositStatus

from .helpers import send_micro_deposit_verify_email


class ApplyBankingWebhook(object):
    def __init__(self, event, customer_account):
        self.event = event
        self.customer_account = customer_account

    def handle(self):
        topic = self.event.topic
        dwolla_id = self.event.target_resource_dwolla_id
        bank_account = get_bank_account_by_dwolla_id(dwolla_id=dwolla_id)
        if not bank_account:
            return

        # event_payload, dwolla_id, is_processed, target_resource_dwolla_id

        if topic == "customer_funding_source_added":
            """
            A funding source was added to a Customer.
            """
            # bank_account.dwolla_funding_source_status = (
            #     DwollaFundingSourceStatus.ADDED
            # )
            # bank_account.save()
            pass

        if topic == "customer_funding_source_removed":
            """
            A funding source was removed from a Customer.
            """
            bank_account.set_dwolla_removed()

        if topic == "customer_funding_source_verified":
            """
            A Customer’s funding source was marked as verified.
            """
            bank_account.dwolla_funding_source_status = (
                DwollaFundingSourceStatus.VERIFIED
            )
            bank_account.save()

        if topic == "customer_funding_source_unverified":
            """
            A funding source has been systematically unverified.
            This is generally a result of a transfer failure. View our developer resource
            article(https://developers.dwolla.com/resources/bank-transfer-workflow/transfer-failures.html)
            to learn more.
            """
            bank_account.dwolla_funding_source_status = (
                DwollaFundingSourceStatus.UNVERIFIED
            )
            bank_account.save()

        if topic == "customer_funding_source_negative":
            """
            A Customer’s balance has gone negative. You are responsible for ensuring a zero or
            positive Dwolla balance for Customer accounts created by your application.
            If a Customer balance funding source has gone negative, you are responsible
            for making the Dwolla Customer account whole. Dwolla will notify you via a webhook
            and separate email of the negative balance. If no action is taken, Dwolla will
            debit your attached billing source.
            """
            # TODO: send an email to admin
            bank_account.dwolla_funding_source_status = (
                DwollaFundingSourceStatus.NEGATIVE_BALANCE
            )
            bank_account.save()

        if topic == "customer_funding_source_updated":
            """
            A Customer’s funding source has been updated. This can also be fired as a
            result of a correction after a bank transfer processes. For example, a
            financial institution can issue a correction to change the bank account
            type from checking to savings.
            """
            # FIX: look into this @pj
            # bank_account.dwolla_funding_source_status = (
            #     DwollaFundingSourceStatus.UPDATED
            # )
            # bank_account.save()
            pass

        if topic == "customer_microdeposits_added":
            """
            A funding source was added to a Customer.
            """

            bank_account.micro_deposit_status = MicroDepositStatus.PENDING
            bank_account.save()

        if topic == "customer_microdeposits_failed":
            """
            A funding source was added to a Customer.
            """

            bank_account.micro_deposit_status = MicroDepositStatus.FAILED
            bank_account.save()

        if topic == "customer_microdeposits_completed":
            """
            A funding source was added to a Customer.
            """

            bank_account.micro_deposit_status = (
                MicroDepositStatus.AWAITING_VERIFICATION
            )
            bank_account.save()
            send_micro_deposit_verify_email(bank_account)

        if topic == "customer_microdeposits_maxattempts":
            """
            A funding source was added to a Customer.
            """

            bank_account.max_attempts_exceeded = True
            bank_account.save()

        self.event.mark_processed()
