# UseState

Wrap your class's instance methods with `@use_state` and `@use_lazy_generated_state` to create a dependency graph of cached properties that only regenerate when their dependencies change.

Uses Python's [data descriptors](https://docs.python.org/3/howto/descriptor.html) to proxy (to the graph) access of properties. Graph nodes are stored on the instances of classes that use the decorators, for sane garbage collection sake.

## Installing

Available on PyPI as [UseState](https://pypi.org/project/UseState/)

```
$ pip install UseState
```

## Examples

See [examples](./examples/) folder

```py
#!/usr/bin/env python3

import math

from UseState import use_state, use_lazy_generated_state

class Cylinder:
    def __init__(self, radius: float, height: float) -> None:
        self.radius = radius
        self.height = height

    @use_state()
    def radius(self) -> float:
        # Default radius
        return 0.0

    @use_state()
    def height(self) -> float:
        # Default height
        return 0.0

    @use_lazy_generated_state({"radius"})
    def area(self) -> float:
        print("Calculating area")
        return self.radius * self.radius * math.pi

    @use_lazy_generated_state({"area", "height"})
    def volume(self) -> float:
        print("Calculating volume")
        return self.area * self.height

def main() -> None:
    c = Cylinder(4.0, 8.0)

    print(c.area)
    # Calculating area
    # 50.26548245743669

    print(c.volume)
    # Calculating volume
    # 402.1238596594935

    c.radius = 4.0 # doesn't cause invalidation because value is same

    print(c.volume)
    # 402.1238596594935

    c.radius = 1.0 # invalidates area, which invalidates volume

    print(c.volume)
    # Calculating area
    # Calculating volume
    # 25.132741228718345

    print(c.area) # cached by previous call to volume
    # 3.141592653589793

    print(c.volume)
    # 25.132741228718345

if __name__ == "__main__":
    main()
```
