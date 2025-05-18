"""
===========
planetary2d
===========

Contains following modules:
- animator.py - contains utilities for animating a system of bodies,
- bodies_system.py - contains classes for handling systems of bodies,
- data.py - contains utilities for handling data and loading JSON files,
- random.py - contains utilities for generating random scenarios.

API classes and functions:
- SystemOfBodies - represents a system of bodies,
- Animator - represents an object that enables handling animations of
the system of bodies,
- Randomizer - represents a generator of random scenarios,
- load_json_data() - serves to load data from a JSON file,
- animate() - serves to animate data simply.

More information to be found in docstrings of respective modules,
classes and functions.
"""

# Import API functions and classes from the modules
from .animator import Animator, animate
from .bodies_system import SystemOfBodies
from .data import load_json_data
from .random import Randomizer


# Set API
__all__: list[str] = ["Animator", "animate",
                      "SystemOfBodies",
                      "load_json_data",
                      "Randomizer"]
