import collections
import copy

from .base import Field
from .meta import AdapterMetaClass
from .utils import BindingDict, undefined

__all__ = ["Adapter"]


class Adapter(Field, metaclass=AdapterMetaClass):
    def __init__(self, data=None, instance=None, *args, **kwargs):
        self.data = data
        self.instance = instance

        super(Adapter, self).__init__(*args, **kwargs)

    @property
    def fields(self):
        if not hasattr(self, "_fields"):
            self._fields = BindingDict(self)
            for key, value in self.get_fields().items():
                self._fields[key] = value
        return self._fields

    def get_fields(self):
        return copy.deepcopy(self.declared_fields)

    def adapt(self, data=None):
        instance = dict()
        for field_name, field in self.fields.items():
            value = field.get_attribute(data or self.data)
            adapted_value = field.adapt(value)
            if adapted_value is undefined:
                continue
            if isinstance(instance, collections.Mapping):
                instance[field_name] = adapted_value
            else:
                setattr(instance, field_name, adapted_value)
        return instance
