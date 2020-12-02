from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.approval.dbapi import get_payment_approval_settings
from apps.approval.services import CreatePaymentApproval
from apps.beneficiary.dbapi import get_beneficiary_object
from apps.member.dbapi import get_account_member_by_id
from apps.payment.dbapi import create_payment_request
from apps.payment.validators import CreatePaymentRequestSerializer


class CreatePayment(ServiceBase):
    def __init__(self, account_id, data):
        self.data = data
        self.account_id = account_id

    def execute(self):
        self._validate_data()
        payment_request = self._factory_payment_request()
        return payment_request

    def _validate_data(self):
        self.data = run_validator(CreatePaymentRequestSerializer, self.data)
        beneficiary_id = self.data["beneficiary_id"]
        beneficiary_instance = get_beneficiary_object(
            beneficiary_id=beneficiary_id, account_id=self.account_id
        )
        if not beneficiary_instance:
            raise ValidationError(
                {"beneficiary_id": ErrorDetail(_("Invalid beneficiary."))}
            )
        self.payment_approval_setting = get_payment_approval_settings(
            account_id=self.account_id
        )
        self.approvers = self._validate_approver_profiles()

    def _validate_approver_profiles(self):
        approval_count = self.payment_approval_setting.approval_count
        approver_ids = self.data["approver_ids"]
        if len(approver_ids) != approval_count:
            raise ValidationError(
                {"detail": ErrorDetail(_("Incorrect number of approvers."))}
            )

        approvers = []
        for approver_id in approver_ids:
            approver = get_account_member_by_id(
                member_id=approver_id, account_id=self.account_id
            )
            if not approver:
                raise ValidationError(
                    {
                        "detail": ErrorDetail(
                            _("Provided approver is not valid.")
                        )
                    }
                )
            approvers.append(approver)
        return approvers

    def _factory_payment_request(self):
        payment_request = create_payment_request(
            account_id=self.account_id,
            beneficiary_id=self.data["beneficiary_id"],
            target_amount=self.data["target_amount"],
            source_currency=self.data["source_currency"],
            ref_document=self.data["ref_document"],
            payment_reference=self.data["payment_reference"],
            purpose_of_payment=self.data["purpose_of_payment"],
            purpose_of_payment_code=self.data["purpose_of_payment_code"],
        )

        for approver in self.approvers:
            create_approval_request_service = CreatePaymentApproval(
                payment_request_id=payment_request.id,
                beneficiary_id=self.data["beneficiary_id"],
                approval_setting_id=self.payment_approval_setting.id,
                approver_id=approver.id,
            )
            create_approval_request_service.execute()

        if len(self.approvers) > 0:
            payment_request.set_approval_pending()
        return payment_request
