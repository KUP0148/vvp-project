"""
This is planetary2d.

Contains following modules:
- animator.py - contains utilities for animating a system of bodies
- bodies_system.py - contains ........
- data - contains utilities for loading JSON files
- random - contains utilities for generating random scenarios

API classes:
- SystemOfBodies - represents...
- Animator - represents...
...

More information to be found in docstrings of respective modules,
classes and functions.
"""

# Import API functions and classes from the modules
from .animator import Animator, animate
from .bodies_system import SystemOfBodies
from .data import load_json_data
from .random import Randomizer


# Set API.......
__all__: list[str] = ["Animator", "animate",
                      "SystemOfBodies",
                      "load_json_data",
                      "Randomizer"]
