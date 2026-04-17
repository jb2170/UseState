from .Base import base_descriptor_decorator
from .BaseStorage import BaseStorageNode, BaseStorageDescriptor

__all__ = [
    "UseStateNode",
    "UseState",
    "use_state",
]

class UseStateNode(BaseStorageNode):
    @BaseStorageNode.value.setter
    def value(self, new_value) -> None:
        old_value = self._value

        if not self._is_out_of_date and old_value == new_value:
            return

        if self.descriptor.setter_method is not None:
            new_value = self.descriptor.setter_method(self.instance, old_value, new_value)

        self._value = new_value
        self._is_out_of_date = False
        self._set_dependants_out_of_date()

    def _make_up_to_date(self):
        if self.descriptor.create_default_state_method is not None:
            initial_value = self.descriptor.create_default_state_method(self.instance)
        else:
            initial_value = None

        self._value = initial_value

class UseState(BaseStorageDescriptor):
    """
    UseState allows manual getting and setting of its value.

    Setting the value manually marks the UseState as up to date.

    If one tries to get the value when the UseState is out of date, eg before
    one has manually assigned a value to the UseState, or because a dependency
    has been changed, then the function is called to generate a default value.
    """

    node_class = UseStateNode

    def __init__(
        self,
        default_dependencies: set[str] | None = None,
        *,
        create_default_state_method = None,
        setter_method = None,
    ) -> None:
        super().__init__(default_dependencies)

        self.create_default_state_method = create_default_state_method
        self.setter_method = setter_method

    def set(self, instance, value):
        self.touch_node(instance).value = value

    def setter(self, *args, **kwargs) -> UseState:
        def wrapper(setter_method):
            ret = self.__class__(
                self.default_dependencies,
                create_default_state_method = self.create_default_state_method,
                setter_method = setter_method,
            )
            return ret
        return wrapper

class use_state(base_descriptor_decorator):
    """
    Decorator to wrap the function that returns the default value to be
    stored in the UseState node if one does not manually assign a value.
    """

    descriptor_class = UseState

    def __call__(self, create_default_state_method) -> UseState:
        return super().__call__(create_default_state_method = create_default_state_method)
