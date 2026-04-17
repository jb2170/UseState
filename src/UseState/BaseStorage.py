from .Base import BaseNode, BaseDescriptor

__all__ = [
    "BaseStorageNode",
    "BaseStorageDescriptor",
]

class BaseStorageNode(BaseNode):
    def __init__(
        self, *,
        descriptor: BaseStorageDescriptor,
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

class BaseStorageDescriptor(BaseDescriptor):
    node_class = BaseStorageNode

    def get(self, instance, owner):
        return self.touch_node(instance).value

    def set(self, instance, value):
        raise AttributeError(f"Cannot set read-only {self.__class__.__name__} property {self._name!r}")
