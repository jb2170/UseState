from .Base import base_descriptor_decorator
from .BaseStorage import BaseStorageNode, BaseStorageDescriptor

__all__ = [
    "UseLazyGeneratedStateNode",
    "UseLazyGeneratedState",
    "use_lazy_generated_state",
]

class UseLazyGeneratedStateNode(BaseStorageNode):
    def _make_up_to_date(self):
        self._value = self.descriptor.primary_method(self.instance)

class UseLazyGeneratedState(BaseStorageDescriptor):
    """
    UseLazyGeneratedState allows the getting of its stored value,
    which first calls its function if the stored value is out of date
    because a dependency has changed.
    """

    node_class = UseLazyGeneratedStateNode

class use_lazy_generated_state(base_descriptor_decorator):
    """
    Decorator to wrap the function that generates the value to be
    stored in the UseLazyGeneratedState node.
    """

    descriptor_class = UseLazyGeneratedState

    def __call__(self, method) -> UseLazyGeneratedState:
        return super().__call__(method)
