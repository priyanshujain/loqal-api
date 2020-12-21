from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, InternalDBError, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.merchant.dbapi import (create_beneficial_owner,
                                 create_controller_details,
                                 create_incorporation_details,
                                 delete_beneficial_owner, get_beneficial_owner,
                                 get_controller_details,
                                 get_incorporation_details,
                                 update_beneficial_owner,
                                 update_controller_details,
                                 update_incorporation_details)
from apps.merchant.validators import (BeneficialOwnerValidator,
                                      ControllerValidator,
                                      IncorporationDetailsValidator,
                                      RemoveBeneficialOwnerValidator,
                                      UpdateBeneficialOwnerValidator)

__all__ = (
    "CreateIncorporationDetails",
    "UpdateIncorporationDetails",
    "CreateControllerDetails",
    "UpdateControllerDetails",
    "CreateBeneficialOwner",
    "UpdateBeneficialOwner",
    "RemoveBeneficialOwner",
)


class CreateIncorporationDetails(ServiceBase):
    def __init__(self, merchant_id, data):
        self.data = data
        self.merchant_id = merchant_id

    def handle(self):
        assert self._validate_data()
        incorporation_details = self._factory_incorporation_details()
        return incorporation_details

    def _validate_data(self):
        if get_incorporation_details(merchant_id=self.merchant_id):
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _("Incorporation details already exists.")
                    )
                }
            )

        self.data = run_validator(IncorporationDetailsValidator, self.data)
        return True

    def _factory_incorporation_details(self):
        incorporation_details = create_incorporation_details(
            merchant_id=self.merchant_id, **self.data
        )
        if incorporation_details:
            return incorporation_details

        raise InternalDBError(
            {
                "detail": ErrorDetail(
                    _(
                        "Incorporation details creation failed, please try again."
                    )
                )
            }
        )


class UpdateIncorporationDetails(CreateIncorporationDetails):
    def __init__(self, merchant_id, data):
        super().__init__(merchant_id, data)

    def handle(self):
        assert self._validate_data()
        self._update_incorporation_details()

    def _validate_data(self):
        incorporation_details = get_incorporation_details(
            merchant_id=self.merchant_id
        )
        if not incorporation_details:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _("Incorporation details did not found.")
                    )
                }
            )
        self.incorporation_details = incorporation_details

        self.data = run_validator(IncorporationDetailsValidator, self.data)
        return True

    def _update_incorporation_details(self):
        update_incorporation_details(
            incorporation_details_id=self.incorporation_details.id,
            merchant_id=self.merchant_id,
            **self.data
        )


class CreateControllerDetails(ServiceBase):
    # TODO: Validate for aleast ssn or passport number required
    def __init__(self, merchant_id, data):
        self.data = data
        self.merchant_id = merchant_id

    def handle(self):
        assert self._validate_data()
        return self._factory_controller_details()

    def _validate_data(self):
        if get_controller_details(merchant_id=self.merchant_id):
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _("Controller details already exists.")
                    )
                }
            )

        self.data = run_validator(ControllerValidator, self.data)
        return True

    def _factory_controller_details(self):
        controller_details = create_controller_details(
            merchant_id=self.merchant_id, **self.data
        )
        if controller_details:
            return controller_details

        raise InternalDBError(
            {
                "detail": ErrorDetail(
                    _("Controller details creation failed, please try again.")
                )
            }
        )


class UpdateControllerDetails(CreateControllerDetails):
    def __init__(self, merchant_id, data):
        super().__init__(merchant_id, data)

    def handle(self):
        assert self._validate_data()
        self._update_controller_details()

    def _validate_data(self):
        controller_details = get_controller_details(
            merchant_id=self.merchant_id
        )
        if not controller_details:
            raise ValidationError(
                {"detail": ErrorDetail(_("Controller details did not found."))}
            )

        self.data = run_validator(ControllerValidator, self.data)
        return True

    def _update_controller_details(self):
        update_controller_details(merchant_id=self.merchant_id, **self.data)


class CreateBeneficialOwner(ServiceBase):
    def __init__(self, merchant_id, data):
        self.data = data
        self.merchant_id = merchant_id

    def handle(self):
        assert self._validate_data()
        return self._factory_controller_details()

    def _validate_data(self):
        self.data = run_validator(BeneficialOwnerValidator, self.data)
        return True

    def _factory_controller_details(self):
        beneficial_owner = create_beneficial_owner(
            merchant_id=self.merchant_id, **self.data
        )
        if beneficial_owner:
            return beneficial_owner

        raise InternalDBError(
            {
                "detail": ErrorDetail(
                    _("Beneficial owner creation failed, please try again.")
                )
            }
        )


class UpdateBeneficialOwner(CreateBeneficialOwner):
    def __init__(self, merchant_id, data):
        super().__init__(merchant_id, data)

    def handle(self):
        assert self._validate_data(validator=UpdateBeneficialOwnerValidator)
        self._update_benficial_owner()

    def _validate_data(self, validator):
        data = run_validator(validator=validator, data=self.data)
        beneficial_owner_id = data["id"]
        beneficial_owner = get_beneficial_owner(
            merchant_id=self.merchant_id,
            beneficial_owner_id=beneficial_owner_id,
        )
        if not beneficial_owner:
            raise ValidationError(
                {"detail": ErrorDetail(_("Beneficial owner did not found."))}
            )
        self.benefical_owner = beneficial_owner
        return True

    def _update_benficial_owner(self):
        update_beneficial_owner(
            beneficial_owner_id=self.benefical_owner.id,
            merchant_id=self.merchant_id,
            **self.data
        )


class RemoveBeneficialOwner(UpdateBeneficialOwner):
    def __init__(self, merchant_id, data):
        super().__init__(merchant_id, data)

    def handle(self):
        assert self._validate_data(validator=RemoveBeneficialOwnerValidator)
        self._remove_beneficial_owner()

    def _remove_beneficial_owner(self):
        delete_beneficial_owner(
            beneficial_owner_id=self.benefical_owner.id,
            merchant_id=self.merchant_id,
        )
