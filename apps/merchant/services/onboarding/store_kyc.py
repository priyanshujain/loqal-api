from re import T

from django.utils.translation import gettext as _

from api.exceptions import (ErrorDetail, InternalDBError, ProviderAPIException,
                            ValidationError)
from api.helpers import run_validator
from api.services import ServiceBase
from apps.merchant.dbapi import (create_beneficial_owner,
                                 create_controller_details,
                                 create_incorporation_details,
                                 delete_beneficial_owner, get_beneficial_owner,
                                 get_controller_details,
                                 get_incorporation_details,
                                 get_incorporation_details_by_ein,
                                 update_beneficial_owner,
                                 update_controller_details,
                                 update_incorporation_details)
from apps.merchant.options import BusinessTypes
from apps.merchant.validators import (BeneficialOwnerValidator,
                                      ControllerValidator,
                                      IncorporationDetailsValidator,
                                      RemoveBeneficialOwnerValidator,
                                      UpdateBeneficialOwnerValidator)
from apps.provider.lib.actions import ProviderAPIActionBase

__all__ = (
    "CreateIncorporationDetails",
    "UpdateIncorporationDetails",
    "CreateControllerDetails",
    "UpdateControllerDetails",
    "CreateBeneficialOwner",
    "UpdateBeneficialOwner",
    "RemoveBeneficialOwner",
)


def validate_business_classifcation(account_id, data):
    business_classification_id = data.get("business_classification_id")
    business_classification = data.get("business_classification")
    industry_classification_id = data.get("industry_classification_id")
    industry_classification = data.get("industry_classification")
    classfications = BusinessClassificationAPIAction(
        account_id=account_id
    ).get(id=business_classification_id)
    if not classfications:
        raise ValidationError(
            {
                "business_classification_id": [
                    ErrorDetail(_("Invalid business classification id"))
                ]
            }
        )
    if classfications["name"] != business_classification:
        raise ValidationError(
            {
                "business_classification": [
                    ErrorDetail(_("Invalid business classification"))
                ]
            }
        )

    industry_classification_filter_list = [
        {"id": classfication["id"], "name": classfication["name"]}
        for classfication in classfications["industry-classifications"]
        if classfication["id"] == industry_classification_id
    ]

    if len(industry_classification_filter_list) == 0:
        raise ValidationError(
            {
                "industry_classification_id": [
                    ErrorDetail(_("Invalid industry classification id"))
                ]
            }
        )

    if (
        industry_classification_filter_list[0]["name"]
        != industry_classification
    ):
        raise ValidationError(
            {
                "industry_classification": [
                    ErrorDetail(_("Invalid industry classification"))
                ]
            }
        )
    return True


class CreateIncorporationDetails(ServiceBase):
    def __init__(self, merchant, data):
        self.data = data
        self.merchant = merchant

    def handle(self):
        assert self._validate_data()
        incorporation_details = self._factory_incorporation_details()
        return incorporation_details

    def _validate_data(self):
        if get_incorporation_details(merchant_id=self.merchant.id):
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _("Incorporation details already exists.")
                    )
                }
            )
        self.data = run_validator(IncorporationDetailsValidator, self.data)
        assert validate_business_classifcation(
            account_id=self.merchant.account.id, data=self.data
        )
        assert self._validate_ein_number(
            self,
            incorporation_details=None,
            ein_number=self.data.get("ein_number"),
        )
        return True

    def _factory_incorporation_details(self):
        incorporation_details = create_incorporation_details(
            merchant_id=self.merchant.id, **self.data
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

    def _validate_ein_number(self, incorporation_details, ein_number):
        if not ein_number:
            return True

        ein_inc_details = get_incorporation_details_by_ein(
            ein_number=ein_number
        )
        if not ein_inc_details:
            return True
        if ein_inc_details and not incorporation_details:
            return True

        if (ein_inc_details and not incorporation_details) or (
            ein_inc_details
            and (ein_inc_details.id != incorporation_details.id)
        ):
            raise ValidationError(
                {
                    "ein_number": ErrorDetail(
                        _(
                            "Please check Provided EIN number again, as it is already being used with another merchant."
                        )
                    )
                }
            )
        return True


class UpdateIncorporationDetails(CreateIncorporationDetails):
    def __init__(self, merchant, data):
        super().__init__(merchant, data)

    def handle(self):
        assert self._validate_data()
        self._update_incorporation_details()

    def _validate_data(self):
        incorporation_details = get_incorporation_details(
            merchant_id=self.merchant.id
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
        assert validate_business_classifcation(
            account_id=self.merchant.account.id, data=self.data
        )
        assert self._validate_ein_number(
            self,
            incorporation_details=incorporation_details,
            ein_number=self.data.get("ein_number"),
        )
        return True

    def _update_incorporation_details(self):
        update_incorporation_details(
            incorporation_details_id=self.incorporation_details.id,
            merchant_id=self.merchant.id,
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
        incorporation_details = get_incorporation_details(
            merchant_id=self.merchant_id
        )
        if not incorporation_details:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _(
                            "Incorporation details are required before adding controller details."
                        )
                    )
                }
            )

        data = run_validator(ControllerValidator, self.data)
        title = data.get("title")
        if (
            incorporation_details.business_type
            != BusinessTypes.SOLE_PROPRIETORSHIP
            and not title
        ):
            raise ValidationError(
                {
                    "title": "Title is required for businesses other than sole proprietors"
                }
            )
        if (
            incorporation_details.business_type
            == BusinessTypes.SOLE_PROPRIETORSHIP
        ):
            data["title"] = ""
            data["passport_number"] = ""
            data["passport_country"] = ""
            if not data.get("ssn"):
                raise ValidationError(
                    {"title": "SSN is required for sole proprietors"}
                )

        self.data = data
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

        incorporation_details = (
            controller_details.merchant.incorporationdetails
        )
        data = run_validator(ControllerValidator, self.data)
        title = data.get("title")
        if (
            incorporation_details.business_type
            != BusinessTypes.SOLE_PROPRIETORSHIP
            and not title
        ):
            raise ValidationError(
                {
                    "title": "Title is required for businesses other than sole proprietors"
                }
            )
        if (
            incorporation_details.business_type
            == BusinessTypes.SOLE_PROPRIETORSHIP
        ):
            data["title"] = ""
            data["passport_number"] = ""
            data["passport_country"] = ""
            if not data.get("ssn"):
                raise ValidationError(
                    {"title": "SSN is required for sole proprietors"}
                )
        self.data = data
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
        incorporation_details = get_incorporation_details(
            merchant_id=self.merchant_id
        )
        if not incorporation_details:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _(
                            "Incorporation details are required before adding controller details."
                        )
                    )
                }
            )
        if (
            incorporation_details.business_type
            == BusinessTypes.SOLE_PROPRIETORSHIP
        ):
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _(
                            "Beneficial owners are not required for sole proprietors."
                        )
                    )
                }
            )
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


class BusinessClassificationAPIAction(ProviderAPIActionBase):
    def get(self, id):
        response = self.client.reference.get_business_classifcation(id=id)
        if self.get_errors(response):
            raise ProviderAPIException(
                {
                    "detail": ErrorDetail(
                        _(
                            "Banking service failed, Please try "
                            "again. If the problem persists please "
                            "contact our support team."
                        )
                    )
                }
            )
        return response.get("data")
