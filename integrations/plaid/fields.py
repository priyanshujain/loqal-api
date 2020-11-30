from lib.adapter import Adapter, Field


class USFieldsAdapter(Adapter):
    account_number = Field(source="account", default="", required=False)
    routing_code_type_1 = Field(default="aba_routing_number")
    routing_code_value_1 = Field(source="routing", default="", required=False)


class CountryAdapterMap:
    US = USFieldsAdapter
