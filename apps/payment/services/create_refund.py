from decimal import Decimal

from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.order.services import CheckReturnRewardCreditAmount
from apps.payment.dbapi import (create_refund_payment, create_transaction,
                                create_zero_transaction, get_merchant_payment)
from apps.payment.dbapi.events import (full_refund_payment_event,
                                       partial_refund_payment_event)
from apps.payment.options import (RefundType, TransactionSourceTypes,
                                  TransactionStatus, TransactionTransferTypes,
                                  TransactionType)
from apps.payment.validators import CreateRefundValidator
from apps.reward.options import RewardValueType
from apps.reward.services import ReturnRewards

from .create_payment import CreatePayment
from .validate_bank_account import ValidateBankAccount

__all__ = ("CreateRefund",)


class CreateRefund(ServiceBase):
    def __init__(self, merchant_account, data, ip_address):
        self.merchant_account = merchant_account
        self.data = data
        self.ip_address = ip_address

    def handle(self):
        payment_data = self._validate_data()
        order = payment_data["order"]
        amount = payment_data["amount"]
        return_reward_credit = CheckReturnRewardCreditAmount(
            order=order, amount=amount
        ).handle()
        reward_usage = None
        return_reward_value = Decimal(0.0)
        reclaim_reward_value = Decimal(0.0)
        if return_reward_credit:
            return_reward_value = return_reward_credit["return_reward_value"]
            reclaim_reward_value = return_reward_credit["reclaim_reward_value"]
            reward_usage = return_reward_credit["reward_usage"]
        refund_payment = self._factory_refund_payment(
            order=order,
            amount=amount,
            refund_reason=payment_data["refund_reason"],
            refund_note=payment_data["refund_note"],
            return_reward_value=return_reward_value,
            reclaim_reward_value=reclaim_reward_value,
        )

        bank_transaction = None
        if refund_payment.amount > Decimal(0.0):
            try:
                transaction = CreatePayment(
                    account_id=self.merchant_account.id,
                    ip_address=self.ip_address,
                    sender_bank_account=payment_data["sender_bank_account"],
                    receiver_bank_account=payment_data[
                        "receiver_bank_account"
                    ],
                    order=order,
                    total_amount=refund_payment.amount,
                    amount_towards_order=(
                        refund_payment.amount + reclaim_reward_value
                    ),
                    fee_bearer_account=self.merchant_account.account,
                    transaction_type=TransactionType.REFUND_PAYMENT,
                    refund_payment_id=refund_payment.id,
                ).handle()
                bank_transaction = transaction
                if refund_payment.refund_type == RefundType.PARTIAL:
                    partial_refund_payment_event(
                        payment_id=refund_payment.payment.id,
                        refund_tracking_id=refund_payment.refund_tracking_id,
                        transaction_tracking_id=bank_transaction.transaction_tracking_id,
                        amount=refund_payment.amount,
                        transfer_type=TransactionTransferTypes.ACH_BANK_TRANSFER,
                    )

            except ValidationError as error:
                try:
                    transaction = error.transaction
                    refund_payment.set_refund_failed(transaction=transaction)
                except AttributeError:
                    refund_payment.set_refund_failed()
                raise error

        if (return_reward_value + reclaim_reward_value) > Decimal(0.0):
            reward_credit = ReturnRewards(
                return_reward_value=return_reward_credit[
                    "return_reward_value"
                ],
                updated_reward_value=return_reward_credit[
                    "updated_reward_value"
                ],
                reclaim_reward_value=return_reward_credit[
                    "reclaim_reward_value"
                ],
                reward_usage=return_reward_credit["reward_usage"],
            ).handle()
            if reward_credit:
                refund_payment.add_reward_credit(reward_credit=reward_credit)
            if reward_credit.reward_value_type == RewardValueType.FIXED_AMOUNT:
                transaction = create_transaction(
                    transaction_type=TransactionType.REFUND_PAYMENT,
                    payment_id=refund_payment.payment.id,
                    amount=return_reward_value,
                    fee_bearer_account_id=None,
                    customer_ip_address=self.ip_address,
                    recipient_source_type=TransactionSourceTypes.REWARD_CASHBACK,
                    sender_source_type=TransactionSourceTypes.NA,
                    refund_payment_id=refund_payment.id,
                    reward_usage_id=reward_credit.id,
                    is_success=True,
                    status=TransactionStatus.PROCESSED,
                )
                transaction.payment.update_charge_status_by_refund(
                    amount=transaction.amount
                )
                partial_refund_payment_event(
                    payment_id=refund_payment.payment.id,
                    refund_tracking_id=refund_payment.refund_tracking_id,
                    transaction_tracking_id=transaction.transaction_tracking_id,
                    amount=return_reward_value,
                    transfer_type=TransactionTransferTypes.CASHBACK,
                )

        if (
            refund_payment.refund_type == RefundType.FULL
            and bank_transaction != None
        ):
            full_refund_payment_event(
                payment_id=refund_payment.payment.id,
                refund_tracking_id=refund_payment.refund_tracking_id,
                transaction_tracking_id=bank_transaction.transaction_tracking_id,
                amount=refund_payment.amount,
                transfer_type=TransactionTransferTypes.ACH_BANK_TRANSFER,
            )

        return refund_payment

    def _validate_data(self):
        data = run_validator(CreateRefundValidator, self.data)
        payment_id = data["payment_id"]
        amount = data["amount"]

        payment = get_merchant_payment(
            merchant_account=self.merchant_account,
            payment_id=payment_id,
        )
        if not payment:
            raise ValidationError(
                {"payment_id": ErrorDetail(_("Given payment does not exist."))}
            )

        order = payment.order
        current_total_order_amount = (
            order.total_amount - order.total_return_amount
        )
        if amount > current_total_order_amount:
            raise ValidationError(
                {
                    "amount": ErrorDetail(
                        _(
                            "The amount should be less than or equal to"
                            " available payment amount."
                        )
                    )
                }
            )

        banking_data = ValidateBankAccount(
            sender_account_id=self.merchant_account.account.id,
            receiver_account_id=payment.order.consumer.account.id,
        ).validate()

        return {
            "refund_note": data.get("refund_note", ""),
            "refund_reason": data.get("refund_reason"),
            "order": order,
            "amount": data["amount"],
            "sender_bank_account": banking_data["sender_bank_account"],
            "receiver_bank_account": banking_data["receiver_bank_account"],
        }

    def _factory_refund_payment(
        self,
        refund_note,
        refund_reason,
        order,
        amount,
        return_reward_value,
        reclaim_reward_value,
    ):
        refund_type = RefundType.FULL
        requested_items_value = amount
        if order.total_net_amount > amount:
            refund_type = RefundType.PARTIAL
        if return_reward_value > Decimal(0.0):
            amount -= return_reward_value
        if reclaim_reward_value > Decimal(0.0):
            amount -= reclaim_reward_value
        return create_refund_payment(
            requested_items_value=requested_items_value,
            payment_id=order.payment.id,
            amount=amount,
            refund_type=refund_type,
            return_reward_value=return_reward_value,
            reclaim_reward_value=reclaim_reward_value,
            refund_reason=refund_reason,
            refund_note=refund_note,
        )
