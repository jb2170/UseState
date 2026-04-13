from .UseLazyGeneratedState import UseLazyGeneratedStateNode, UseLazyGeneratedState, use_lazy_generated_state

__all__ = [
    "UseStateNode",
    "UseState",
    "use_state",
]

class UseStateNode(UseLazyGeneratedStateNode):
    @UseLazyGeneratedStateNode.value.setter
    def value(self, new_value) -> None:
        if self._value == new_value:
            return

        self._value = new_value
        self._is_out_of_date = False
        self._set_dependants_out_of_date()

class UseState(UseLazyGeneratedState):
    """
    UseState allows manual getting and setting of its value.

    Setting the value manually marks the UseState as up to date.

    If one tries to get the value when the UseState is out of date, eg before
    one has manually assigned a value to the UseState, or because a dependency
    has been changed, then the function is called to generate a default value.
    """

    node_class = UseStateNode

    def set(self, instance, value):
        self.touch_node(instance).value = value

class use_state(use_lazy_generated_state):
    """
    Decorator to wrap the function that returns the default value to be
    stored in the UseState node if one does not manually assign a value.
    """

    descriptor_class = UseState
