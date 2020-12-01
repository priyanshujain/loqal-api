from api.helpers import run_validator
from api.services import ServiceBase
from apps.account.validators import ConsumerZipCodeValidator

__all__ = ("AddZipCode",)


class AddZipCode(ServiceBase):
    def __init__(self, account, data):
        self.data = data
        self.account = account

    def execute(self):
        data = self._validate_data()
        zip_code = data["zip_code"]
        self.account.add_zip_code(zip_code=zip_code)

    def _validate_data(self):
        return run_validator(
            validator=ConsumerZipCodeValidator, data=self.data
        )

    def _check_zip_code_support(self):
        """
        Check if we support provided zip_code
        """
        pass
