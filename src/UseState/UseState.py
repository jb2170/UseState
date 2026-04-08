from .Base import base_descriptor_decorator
from .BaseStorage import BaseStorageNode, BaseStorageDescriptor

__all__ = [
    "UseStateNode",
    "UseState",
    "use_state",
]

class UseStateNode(BaseStorageNode):
    def _is_initially_out_of_date(self):
        # UseState is never intended to be out of date.
        # Even if somehow set_out_of_date() gets called
        # the default _make_up_to_date() does nothing.
        return False

    def _create_initial_value(self):
        return self.primary_method()

    @BaseStorageNode.value.setter
    def value(self, new_value) -> None:
        if self._value == new_value:
            return

        self._value = new_value
        self._set_dependants_out_of_date()

class UseState(BaseStorageDescriptor):
    """
    UseState allows manual getting and setting of its value.
    """

    node_class = UseStateNode

    def set(self, instance, value):
        self.touch_own_node(instance).value = value

class use_state(base_descriptor_decorator):
    """
    Decorator to wrap the function that returns the initial value to be
    stored in the UseState node.
    """

    descriptor_class = UseState
