from .UseState import UseStateNode, use_state

__all__ = [
    "UsePropertyNode",
    "use_property",
]

class UsePropertyNode(UseStateNode):
    @UseStateNode.value.setter
    def value(self, new_value) -> None:
        if not self._is_out_of_date:
            raise ValueError(f"Can only set the value of {self.descriptor.__class__.__name__} property {self.descriptor.name!r} once")

        UseStateNode.value.fset(self, new_value)

class use_property(use_state):
    """
    `use_property` is a special version of UseState that allows manual setting
    of its value only when out of date. For `use_property` attributes with
    no dependencies this means only once.

    Trying to get the value when the `use_property` is out of date behaves the
    same as UseState; the function is called to generate a default value.
    """

    node_class = UsePropertyNode

    def __call__(self, create_default_state_method) -> use_property:
        """
        Decorator to wrap the function that returns the default value to be
        stored in the UseProperty node if one does not manually assign a value.
        """

        return super().__call__(create_default_state_method)
