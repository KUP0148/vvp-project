"""
``planetary2d.random``
======================

The ``planetary2d.random`` module provides utilities for generation of random
scenarios, i.e. random initial conditions for systems of bodies.

Please note that the class ``Randomizer`` are present
in the main ``planetary2d`` namespace.

Classes present in ``planetary2d.random`` listed below.

Randomization classes
---------------------
- Randomizer

Randomization type aliases
--------------------------
- IntRange
- Range
- VectorRange

"""

# Imports
from typing import Tuple
from random import randint, uniform
from .bodies_system import SystemOfBodies


# Type alias definitions
IntRange = Tuple[int, int]
Range = Tuple[float, float]
VectorRange = Tuple[Range, Range]


class Randomizer:
    """
    A class which handles randomization of initial conditions.


    :ivar bodies_count_range: A tuple of lower and upper limits of the
        randomization of the number of bodies in the data output.
    :vartype bodies_count_range: IntRange

    :ivar positions_range: A tuple of tuples of lower and upper limits of
        respective coordinates of positions.
    :vartype positions_range: VectorRange

    :ivar velocities_range: A tuple of tuples of lower and upper limits of
        respective coordinates of velocities.
    :vartype velocities_range: VectorRange

    :ivar masses_range: A tuple of lower and upper limits of the
        randomization of the masses.
    :vartype masses_range: Range
    """

    def __init__(self,
                 bodies_count_range: IntRange = (1, 10),
                 positions_range: VectorRange = ((-200, 200), (-200, 200)),
                 velocities_range: VectorRange = ((-100, 100), (-100, 100)),
                 masses_range: Range = (1e10, 1e17)) -> None:
        """
        A constructor of Randomizer objects.

        :param bodies_count_range: A tuple of lower and upper limits of the
            randomization of the number of bodies in the data output.
        :type bodies_count_range: IntRange

        :param positions_range: A tuple of tuples of lower and upper limits of
            respective coordinates of positions.
        :type positions_range: VectorRange

        :param velocities_range: A tuple of tuples of lower and upper limits of
            respective coordinates of velocities.
        :type velocities_range: VectorRange

        :param masses_range: A tuple of lower and upper limits of the
            randomization of the masses.
        :type masses_range: Range
        """
        # == Create data members ==
        self.bodies_count_range = bodies_count_range
        self.positions_range = positions_range
        self.velocities_range = velocities_range
        self.masses_range = masses_range

    def generate_data(self):
        """
        Generates a random initial conditions in the form of the dictionary
        data which the ``SystemOfBodies`` can be passed in the constructor.
        The random generation is given by the member data from the constructor.

        :returns: Dictionary of initial conditions
        :rtype: dict_data (dict)
        """
        # Data dictionary
        dict_data: dict = {}
        # Randomly choose the number of bodies
        bodies_count = randint(*self.bodies_count_range)
        # Generate random data
        for i in range(bodies_count):
            # Extract ranges
            x_pos_range, y_pos_range = self.positions_range
            x_vel_range, y_vel_range = self.velocities_range
            # Randomly choose vectors and scalars in proper ranges
            position = [uniform(*x_pos_range), uniform(*y_pos_range)]
            velocity = [uniform(*x_vel_range), uniform(*y_vel_range)]
            mass = uniform(*self.masses_range)
            # Add a body initialization to the dictionary
            dict_data.update({f"body{i}": {"position": position,
                                           "velocity": velocity,
                                           "mass": mass}})
        return dict_data

    def generate_bodies_system(self, **kwargs):
        """
        A shorthand method for a direct generation of a system of bodies.

        :param kwargs: A dictionary of optional keyword arguments to be
            passed to the SystemOfBodies' constructor.

        :returns: A randomly generated system of bodies.
        :rtype: SystemOfBodies
        """
        # Generates data and passes unpacked dictionary of keyword arguments
        return SystemOfBodies(self.generate_data(), **kwargs)
