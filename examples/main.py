#!/usr/bin/env python3

import math

from UseState import use_state, use_lazy_generated_state

class Cylinder:
    def __init__(self, radius: float, height: float) -> None:
        self.radius = radius
        self.height = height

    @use_state()
    def radius(self) -> float:
        print("Calculating default radius")
        return 0.0

    @use_state()
    def height(self) -> float:
        print("Calculating default height")
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
