from utils.choices import Choices


class PlaidEnvTypes(Choices):
    SANDBOX = "sandbox"
    DEVELOPMENT = "development"
    PRODUCTION = "production"


class PlaidProductTypes(Choices):
    AUTH = "auth"


class PlaidSupportedCountries(Choices):
    US = "US"
    CA = "CA"
    GB = "GB"
    IE = "IE"
    NL = "NL"
    FR = "FR"
    ES = "ES"


class PlaidAccountTypeMap:
    US = "ach"
