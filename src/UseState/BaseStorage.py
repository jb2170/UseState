from .Base import BaseNode, base_descriptor

__all__ = [
    "BaseStorageNode",
    "base_storage_descriptor",
]

class BaseStorageNode(BaseNode):
    def __init__(
        self, *,
        descriptor: base_storage_descriptor,
        instance,
        dependencies: set[BaseNode] | None = None,
    ) -> None:
        super().__init__(
            descriptor = descriptor,
            instance = instance,
            dependencies = dependencies,
        )

        self._value = self._create_initial_value()

    def _create_initial_value(self):
        return None

    @property
    def value(self):
        self.ensure_up_to_date()

        return self._value

class base_storage_descriptor(base_descriptor):
    node_class = BaseStorageNode

    def get(self, instance, owner):
        return self.touch_node(instance).value

    def set(self, instance, value):
        raise AttributeError(f"Cannot set read-only {self.__class__.__name__} property {self._name!r}")
