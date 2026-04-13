from .Base import BaseNode, BaseDescriptor

__all__ = [
    "BaseStorageNode",
    "BaseStorageDescriptor",
]

class BaseStorageNode(BaseNode):
    def __init__(self, primary_method, dependencies = None) -> None:
        super().__init__(primary_method = primary_method, dependencies = dependencies)

        self._value = self._create_initial_value()

    def _create_initial_value(self):
        return None

    @property
    def value(self):
        self.ensure_up_to_date()

        return self._value

class BaseStorageDescriptor(BaseDescriptor):
    node_class = BaseStorageNode

    def get(self, instance, owner):
        return self.touch_own_node(instance).value

    def set(self, instance, value):
        raise AttributeError(f"Cannot set read-only {self.__class__.__name__} property {self._name!r}")
