import functools

__all__ = [
    "BaseNode",
    "BaseDescriptor",
    "base_descriptor_decorator",
]

class BaseNode:
    def __init__(
        self,
        primary_method,
        dependencies: set[BaseNode] | None = None
    ) -> None:
        if dependencies is None:
            dependencies = set()

        # The main method that the decorators wrap.
        # In the future we may have descriptors / nodes that use multiple functions
        # like how there's `@property def my_prop` and `@my_prop.setter def my_prop`
        self.primary_method = primary_method

        # Nodes that this one depends on.
        # Aka 'parents'
        self.dependencies: set[BaseNode] = dependencies.copy()

        # Nodes that depend on this one.
        # Aka 'children'
        self.dependants: set[BaseNode] = set()

        # Aka the dirty bit.
        self._is_out_of_date: bool = self._is_initially_out_of_date()

    @property
    def is_out_of_date(self) -> bool:
        return self._is_out_of_date

    def add_dependency(self, dependency: BaseNode) -> None:
        self._add_dependency(dependency)
        dependency._add_dependant(self)

    def remove_dependency(self, dependency: BaseNode) -> None:
        self._remove_dependency(dependency)
        dependency._remove_dependant(self)

    def has_dependency(self, dependency: BaseNode) -> bool:
        return dependency in self.dependencies

    def _add_dependency(self, dependency: BaseNode) -> None:
        # Shouldn't really be called on its own; see add_dependency
        self.dependencies.add(dependency)

    def _remove_dependency(self, dependency: BaseNode) -> None:
        # Shouldn't really be called on its own; see remove_dependency
        self.dependencies.discard(dependency)

    def _add_dependant(self, dependant: BaseNode) -> None:
        # Shouldn't really be called on its own; see add_dependency
        self.dependants.add(dependant)

    def _remove_dependant(self, dependant: BaseNode) -> None:
        # Shouldn't really be called on its own; see remove_dependency
        self.dependants.discard(dependant)

    def _is_initially_out_of_date(self) -> bool:
        return True

    def set_out_of_date(self, *, and_dependants: bool = True) -> None:
        if self._is_out_of_date:
            return

        self._is_out_of_date = True

        if and_dependants:
            self._set_dependants_out_of_date()

    def _set_dependants_out_of_date(self) -> None:
        for dependant in self.dependants:
            dependant.set_out_of_date()

    def ensure_up_to_date(self) -> None:
        if not self._is_out_of_date:
            return

        self._ensure_dependencies_up_to_date()
        self._make_up_to_date()
        self._is_out_of_date = False

    def _ensure_dependencies_up_to_date(self) -> None:
        for dependency in self.dependencies:
            dependency.ensure_up_to_date()

    def _make_up_to_date(self) -> None:
        pass

class BaseDescriptor:
    node_class: type[BaseNode] = BaseNode

    def __init__(
        self,
        primary_method,
        default_dependencies: set[str] | None = None
    ) -> None:
        if default_dependencies is None:
            default_dependencies = set()

        self.primary_method                 = primary_method
        self.default_dependencies: set[str] = default_dependencies.copy()

    def __set_name__(self, owner, name) -> None:
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self

        return self.get(instance, owner)

    def get(self, instance, owner):
        raise NotImplementedError

    def __set__(self, instance, value) -> None:
        if instance is None:
            raise NotImplementedError

        self.set(instance, value)

    def set(self, instance, value) -> None:
        raise NotImplementedError

    def _name_to_node_name(self, name: str) -> str:
        return f"_{name}"

    def _get_node_by_name(self, instance, name: str, default = None) -> BaseNode:
        return instance.__dict__.get(self._name_to_node_name(name), default)

    def _set_node_by_name(self, instance, name: str, node) -> None:
        instance.__dict__[self._name_to_node_name(name)] = node

    def _create_new_node_only(self, instance) -> BaseNode:
        return self.node_class(
            functools.partial(self.primary_method, self = instance),
        )

    def _create_new_node(self, instance) -> BaseNode:
        # Creation of node + wiring up of dependency nodes is done lazily here
        # instead of in __init__, as otherwise the descriptors would need to be
        # __init__-ed in a very strict order

        ret = self._create_new_node_only(instance)

        for dependency_name in self.default_dependencies:
            # Ensure the dependency node is initialized on the instance
            descriptor = getattr(instance.__class__, dependency_name)
            dependency_node = descriptor.touch_own_node(instance)

            ret.add_dependency(dependency_node)

        return ret

    def touch_own_node(self, instance) -> BaseNode:
        node = self._get_node_by_name(instance, self.name)
        if node is None:
            node = self._create_new_node(instance)
            self._set_node_by_name(instance, self.name, node)

        return node

class base_descriptor_decorator:
    descriptor_class: type[BaseDescriptor] = BaseDescriptor

    def __init__(self, default_dependencies_names: set[str] | None = None):
        self.default_dependencies_names = default_dependencies_names

    def __call__(self, method):
        return self.descriptor_class(method, self.default_dependencies_names)
