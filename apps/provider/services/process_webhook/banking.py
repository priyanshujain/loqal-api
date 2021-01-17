class ApplyBankingWebhook(object):
    def __init__(self, event):
        self.event = event

    def handle(self):
        topic = self.event.topic
        # event_payload, dwolla_id, is_processed, target_resource_dwolla_id

        if topic == "customer_funding_source_added":
            # A funding source was added to a Customer.
            pass

        if topic == "customer_funding_source_removed":
            # A funding source was removed from a Customer.
            pass

        if topic == "customer_funding_source_verified":
            # A Customer’s funding source was marked as verified.
            pass

        if topic == "customer_funding_source_unverified":
            # A funding source has been systematically unverified.
            # This is generally a result of a transfer failure. View our developer resource
            # article(https://developers.dwolla.com/resources/bank-transfer-workflow/transfer-failures.html)
            # to learn more.
            pass

        if topic == "customer_funding_source_negative":
            # A Customer’s balance has gone negative. You are responsible for ensuring a zero or
            # positive Dwolla balance for Customer accounts created by your application.
            # If a Customer balance funding source has gone negative, you are responsible
            # for making the Dwolla Customer account whole. Dwolla will notify you via a webhook
            # and separate email of the negative balance. If no action is taken, Dwolla will
            # debit your attached billing source.
            pass

        if topic == "customer_funding_source_updated":
            # A Customer’s funding source has been updated. This can also be fired as a
            # result of a correction after a bank transfer processes. For example, a
            # financial institution can issue a correction to change the bank account
            # type from checking to savings.
            pass
