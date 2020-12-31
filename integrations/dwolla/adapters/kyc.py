from lib.adapter import Adapter, Field


class SolePersonAdapter(Adapter):
    firstName = Field(source="first_name")
    lastName = Field(source="last_name")
    DateOfBirth = Field(source="dob")
    address1 = Field(source="address.address1")
    address2 = Field(source="address.address2")
    city = Field(source="address.city")
    state = Field(source="address.state")
    postalCode = Field(source="address.zip_code")
    ssn = Field()


class AddressAdapter(Adapter):
    address1 = Field()
    address2 = Field()
    city = Field()
    stateProvinceRegion = Field(source="state")
    country = Field()
    postalCode = Field(source="zip_code")


class PassportAdapter(Adapter):
    number = Field(source="passport_number", required=False)
    country = Field(source="passport_country", required=False)


class IndividualBaseAdapter(Adapter):
    firstName = Field(source="first_name")
    lastName = Field(source="last_name")
    dateOfBirth = Field(source="dob")
    address = AddressAdapter()


class ControllerAdapter(IndividualBaseAdapter):
    ssn = Field(required=False)


class DwollaBusinessTypes:
    sole_proprietorship = "soleProprietorship"
    llc = "llc"
    corporation = "corporation"
    partnership = "partnership"


def format_business_type(business_type):
    return getattr(DwollaBusinessTypes, business_type)


class IncorporationDetailsAdapter(Adapter):
    firstName = Field(source="user.first_name")
    lastName = Field(source="user.last_name")
    email = Field(source="user.email")
    type = Field(default="business")
    ipAddress = Field(source="ip_address")
    address1 = Field(source="registered_address.address1")
    address2 = Field(source="registered_address.address2")
    city = Field(source="registered_address.city")
    state = Field(source="registered_address.state")
    postalCode = Field(source="registered_address.zip_code")
    businessName = Field(source="legal_business_name")
    businessType = Field(
        source="business_type.value", format_callback=format_business_type
    )
    businessClassification = Field(source="industry_classification_id")
    ein = Field(source="ein_number", required=False)


class BeneficialOwnerAdapter(IndividualBaseAdapter):
    ssn = Field(required=False)


def get_individual_data(adapter, data):
    adapted_data = adapter(data).adapt()
    if data.get("title"):
        adapted_data["title"] = data["title"]
    if data.get("passport_number"):
        adapted_data["passport"] = PassportAdapter(data).adapt()
    return adapted_data


def get_adapted_kyc_data(data):
    incorporation_details = data["incorporation_details"]
    controller_details = data["controller_details"]
    business_type = incorporation_details["business_type"]

    adapted_data = {}
    if business_type.value == DwollaBusinessTypes.sole_proprietorship:
        adapted_data = {
            **IncorporationDetailsAdapter(incorporation_details).adapt(),
            **SolePersonAdapter(controller_details).adapt(),
        }
    else:
        controller = get_individual_data(
            adapter=ControllerAdapter, data=controller_details
        )
        adapted_data = {
            **IncorporationDetailsAdapter(incorporation_details).adapt(),
            "controller": controller,
        }
    return adapted_data


def get_adapted_benficial_owner(data):
    return get_individual_data(adapter=BeneficialOwnerAdapter, data=data)
