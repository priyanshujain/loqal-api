from rest_framework.exceptions import ErrorDetail
from rest_framework.serializers import *


class BaseSerializer(Serializer):
    def get_fields(self):
        """
        Override get_fields() method to pass context to other serializers of this base class.

        """
        fields = super().get_fields()

        # Cause fields with this same base class to inherit self._context
        for field_name in fields:
            if isinstance(fields[field_name], ListSerializer):
                if isinstance(fields[field_name].child, BaseSerializer):
                    fields[field_name].child._context = self._context

            elif isinstance(fields[field_name], BaseSerializer):
                fields[field_name]._context = self._context

        return fields


class ValidationSerializer(BaseSerializer):
    def add_error(self, field, errors=["This field is required."]):
        if field in self._errors.keys():
            return

        def add_to_error_list(error):
            if not isinstance(error, ErrorDetail):
                error_list.append(ErrorDetail(error))
            else:
                error_list.append(error)

        error_list = []
        if not isinstance(errors, list):
            add_to_error_list(errors)
        else:
            for error in errors:
                add_to_error_list(error)

        self._errors[field] = error_list


class ModelSerializer(BaseSerializer, ModelSerializer):
    pass


class AddressSerializer(BaseSerializer):
    address1 = CharField(max_length=1024)
    address2 = CharField(
        max_length=1024,
        default="",
        allow_blank=True,
        allow_null=True,
        required=False,
    )
    country = CharField(max_length=2)
    state = CharField(max_length=3)
    city = CharField(max_length=255, required=False)
    zip_code = CharField(max_length=10)
    latitude = FloatField(required=False)
    longitude = FloatField(required=False)


class ChoiceCharEnumSerializer(BaseSerializer):
    label = CharField()
    value = CharField()


class ChoiceEnumSerializer(BaseSerializer):
    label = CharField()
    value = IntegerField()
