from .UseState import UseStateNode, UseState, use_state

__all__ = [
    "UsePropertyNode",
    "UseProperty",
    "use_property",
]

class UsePropertyNode(UseStateNode):
    @UseStateNode.value.setter
    def value(self, new_value) -> None:
        if not self._is_out_of_date:
            raise ValueError("Can only set the value of a UseProperty once")

        UseStateNode.value.fset(self, new_value)

class UseProperty(UseState):
    """
    UseProperty is a special version of UseState that allows manual setting
    of its value only when out of date. For UseProperty attributes with
    no dependencies this means only once.

    Trying to get the value when the UseProperty is out of date behaves the
    same as UseState; the function is called to generate a default value.
    """

    node_class = UsePropertyNode

class use_property(use_state):
    """
    Decorator to wrap the function that returns the default value to be
    stored in the UseProperty node if one does not manually assign a value.
    """

    descriptor_class = UseProperty

    def __call__(self, method) -> UseProperty:
        return super().__call__(method)
