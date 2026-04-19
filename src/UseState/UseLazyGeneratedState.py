from .BaseStorage import BaseStorageNode, base_storage_descriptor

__all__ = [
    "UseLazyGeneratedStateNode",
    "use_lazy_generated_state",
]

class UseLazyGeneratedStateNode(BaseStorageNode):
    def _make_up_to_date(self):
        if self.descriptor.generate_state_method is None:
            raise AttributeError(f"{self.descriptor.__class__.__name__} property {self.descriptor.name!r} has no 'generate_state_method'", name = None)

        self._value = self.descriptor.generate_state_method(self.instance)

class use_lazy_generated_state(base_storage_descriptor):
    """
    `use_lazy_generated_state` allows the getting of its stored value,
    which first calls its function if the stored value is out of date
    because a dependency has changed.
    """

    node_class = UseLazyGeneratedStateNode

    def __init__(
        self,
        default_dependencies: set[str] | None = None,
        *,
        generate_state_method = None,
    ) -> None:
        super().__init__(default_dependencies)

        self.generate_state_method = generate_state_method

    def __call__(self, generate_state_method) -> use_lazy_generated_state:
        """
        Decorator to wrap the function that generates the value to be
        stored in the UseLazyGeneratedState node.
        """

        return self.generate_state()(generate_state_method = generate_state_method)

    def generate_state(self, *args, **kwargs) -> use_lazy_generated_state:
        def wrapper(generate_state_method):
            ret = use_lazy_generated_state(
                self.default_dependencies,
                generate_state_method = generate_state_method,
            )
            return ret
        return wrapper
