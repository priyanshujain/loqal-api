from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.payment.dbapi import get_dispute_by_uid
from apps.payment.validators import (ChangeDisputeStatusValidator,
                                     CloseDisputeValidator)

__all__ = (
    "ChangeDisputeStatus",
    "CloseDispute",
)


class ChangeDisputeStatus(ServiceBase):
    def __init__(self, dispute_id, data):
        self.dispute_id = dispute_id
        self.data = data

    def handle(self):
        data = self._validate_data()
        dispute = data["dispute"]
        dispute.update_status(status=data["status"], notes=data["notes"])

    def _validate_data(self, validator=ChangeDisputeStatusValidator):
        data = run_validator(validator, self.data)
        dispute = get_dispute_by_uid(self.dispute_id)

        if not dispute:
            raise ValidationError(
                {"details": ErrorDetail(_("Given dispute does not exist."))}
            )

        data["dispute"] = dispute
        return data


class CloseDispute(ChangeDisputeStatus):
    def handle(self):
        data = self._validate_data(validator=CloseDisputeValidator)
        dispute = data["dispute"]
        dispute.close_dispute(
            resolution=data["resolution"],
            status=data["status"],
            notes=data["notes"],
        )
