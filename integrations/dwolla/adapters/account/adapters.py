from lib.adapter import Adapter, Field

__all__ = ("CreateConsumerAccountAdapter",)


class CreateConsumerAccountAdapter(Adapter):
    firstName = Field(source="first_name")
    lastName = Field("last_name")
    email = Field()
    ipAddress = Field(source="ip_address")
