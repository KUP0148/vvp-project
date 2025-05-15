"""
``planetary2d.bodies_system``
=============================

The ``planetary2d.bodies_system`` module provides functionality for handling
systems of bodies.

Please note that the most important class ``SystemOfBodies`` is present
in the main ``planetary2d`` namespace.

Classes, functions, constants and type aliases present in
``planetary2d.bodies_system`` listed below.

Classes for systems of bodies
-----------------------------
- SystemOfBodies
- SystemOfBodiesIterator

Constants for system of bodies
------------------------------
- T_UNITS
- T_UNITS_INV
- S_UNITS
- S_UNITS_INV
- M_UNITS
- M_UNITS_INV
- G

Type aliases fro system of bodies
---------------------------------
- ScalarType
- VectorType
- ArrayOfScalars
- ArrayOfVectors
- MatrixOfScalars
- MatrixOfVectors

"""

# Imports
from typing import Literal, List, Dict
# from numba import jit
import numpy as np
import copy as cpy  # For copying SystemOfBodies
from .data import POSITION, MASS, VELOCITY
from .data import try_structure


# Type alias definitions
ScalarType = float
VectorType = np.complex128
ArrayOfScalars = np.ndarray[tuple[int], np.dtype[ScalarType]]
ArrayOfVectors = np.ndarray[tuple[int], np.dtype[VectorType]]
MatrixOfScalars = np.ndarray[tuple[int, int], np.dtype[ScalarType]]
MatrixOfVectors = np.ndarray[tuple[int, int], np.dtype[VectorType]]


# Global constants for units
T_UNITS: Dict[str, float] = {
    'millisecs': 0.001, 'secs': 1, 'mins': 60, 'hrs': 3600,
    'days': 86_400, 'wks': 604_800, 'months': 2_592_000,
    'yrs': 31_536_000}
"""
Dictionary of units of time.
"""
T_UNITS_INV: Dict[float, str] = {v: k for k, v in T_UNITS.items()}
"""
Dictionary of units of time inverted.
"""
S_UNITS: Dict[str, float] = {
    'mm': 0.001, 'cm': 0.01, 'm': 1, 'km': 1000}
"""
Dictionary of units of space/distance.
"""
S_UNITS_INV: Dict[float, str] = {v: k for k, v in S_UNITS.items()}
"""
Dictionary of units of space/distance inverted.
"""
M_UNITS: Dict[str, float] = {
    'mg': 0.000_1, 'g': 0.001, 'kg': 1, 't': 1}
"""
Dictionary of units of mass.
"""
M_UNITS_INV: Dict[float, str] = {v: k for k, v in M_UNITS.items()}
"""
Dictionary of units of mass inverted.
"""
# Global numerical constants
G: ScalarType = 6.674e-11
"""
Gravitational constant [m^3 kg^-1 s^-2]
"""


class SystemOfBodies:
    """
    A class which stores the state of the system of bodies
    (i.e. positions, velocities, masses, accelerations).

    Implementation note
    -------------------
    The 2D vectors (of position, velocity...) are represented as
    a complex numbers. Not as a tuple or something similar.
    Hence the complex types of numpy arrays which store these data.


    :ivar b_num: Number of bodies in the system.
    :vartype b_num: int

    :ivar labels: List of labels for the bodies.
    :vartype labels: List[str]

    :ivar self.pos: Array of vectors of positions of the bodies
        in ``space_units``.
    :vartype self.pos: ArrayOfVectors

    :ivar self.vel: Array of vectors of velocities of the bodies.
        in ``space_units`` over ``time_units``.
    :vartype self.vel: ArrayOfVectors

    :ivar self.mass: Array of scalars of masses of the bodies.
        in ``mass_units``.
    :vartype self.mass: ScalarType

    :ivar self.acc: Array of vectors of accelerations of the bodies.
        in ``space_units`` over ``time_units`` squared.
    :vartype self.acc: ArrayOfVectors

    :ivar Δt: Length of the base interval in ``time_units``.
    :vartype Δt: ScalarType

    :ivar t_units: Numerical equivalent to ``time_units``
        (a coefficient of fundamental SI units).
    :vartype t_units: ScalarType

    :ivar s_units: Numerical equivalent to ``space_units``
        (a coefficient of fundamental SI units).
    :vartype s_units: ScalarType

    :ivar m_units: Numerical equivalent to ``mass_units``
        (a coefficient of fundamental SI units).
    :vartype m_units: ScalarType

    :ivar lim: Maximum number of changes of the system of bodies which
        can be performed (i.e. only this number of steps can be done).
    :vartype lim: int

    :ivar no_hist: The history of positions of bodies in the system
        not to be tracked.
    :vartype no_hist: bool

    :ivar hist: The history of positions of bodies in the system.
        (only if ``no_hist`` is True)
    :vartype hist: List[ArrayOfVectors]
    """

    def __init__(self,
                 dict_data: dict,
                 base_interval: ScalarType = 1,
                 time_units: Literal['millisecs', 'secs', 'mins', 'hrs',
                                     'days', 'wks', 'months', 'yrs'] = 'secs',
                 space_units: Literal['mm', 'cm', 'm', 'km'] = 'm',
                 mass_units: Literal['mg', 'g', 'kg', 't'] = 'kg',
                 limit: int = 100,
                 no_hist: bool = False) -> None:
        """
        A constructor of SystemOfBodies objects.

        :param dict_data: Initial-conditions data structured as *dict*. \n
            The structure of the dictionary should follow this pattern:: \n
                {'name_of_the_body': {'position': [ScalarType, ScalarType],
                                      'velocity': [ScalarType, ScalarType],
                                      'mass': ScalarType},
                ...} \n
            (note that if ``dict_data`` is invalid, raises RuntimeError!)
        :type dict_data: dict

        :param base_interval: The base interval of time discretization, i.e.
            the time of each elemenary change of the system of bodies. \n
            Beware that the units used for ``base_interval`` are given by
            the parameter ``time_units``.
        :type base_interval: ScalarType

        :param time_units: Units of time used in the ``dict_data``.
            *Beware that this does not set the duration of each step*;
            however, ``time_units`` sets how to treat 'velocity'
            (i.e. per what time unit are the velocities given). \n
            Note that given literals has the following meaning:: \n
                'secs' = 1000 * 'millisecs',
                'mins' = 60 * 'secs',
                'hrs' = 60 * 'mins',
                'days' = 24 * 'hrs',
                'wks' = 7 * 'days',
                'months' = 30 * 'days',
                'yrs' = 365 * 'days'.
        :type time_units: Literal['millisecs', 'secs', 'mins', 'hrs',
                                  'days', 'wks', 'months', 'yrs']

        :param space_units: Units of space/distance used in the ``dict_data``.
            This sets how to treat 'position' & 'velocity'
            (i.e. what space unit per a time unit the velocities are given). \n
            Note that given literals has the following meaning:: \n
                'mm' - millimeters,
                'cm' - centimeters,
                'm' - meters,
                'km' - kilometers.
        :type space_units: Literal['mm', 'cm', 'm', 'km']

        :param mass_units: Units of mass used in the ``dict_data``.
            This sets how to treat 'mass'. \n
            Note that given literals has the following meaning:: \n
                'mg' - milligrams,
                'g' - grams,
                'kg' - kilograms,
                't' - metric tons.
        :type mass_units: Literal['mg', 'g', 'kg', 't']

        :param limit: Maximum number of changes of the system of bodies which
            can be performed (i.e. only this number of steps can be done). \n
            Note that this value can be re-set by the eponymous property
            (and in combination with animation, this value is kept default
            in the constructor).
        :type limit: int

        :param no_hist: Boolean switch for setting if the history of
            positions of bodies in the system should be tracked.
        :type no_hist: bool
        """
        # == Create data members ==
        self.b_num: int = len(dict_data)
        self.labels: List[str] = []
        self.pos: ArrayOfVectors = np.zeros((self.b_num), dtype=VectorType)
        self.vel: ArrayOfVectors = np.zeros((self.b_num), dtype=VectorType)
        self.mass: ScalarType = np.zeros((self.b_num), dtype=float)
        self.acc: ArrayOfVectors = np.zeros((self.b_num), dtype=VectorType)
        self.Δt: ScalarType = base_interval
        self.t_units: ScalarType = 0
        self.s_units: ScalarType = 0
        self.m_units: ScalarType = 0
        self.limit: int = limit
        self.no_hist: bool = no_hist
        # == Try dict_data structure ==
        if not try_structure(dict_data):
            raise RuntimeError(
                "The dict_data does not meet the prescribed structure!")
        # == Parse dict_data ==
        for i, (body, data) in enumerate(dict_data.items()):
            self.labels.append(body)  # Body's label
            self.pos[i] = data[POSITION][0] + 1j * data[POSITION][1]
            self.vel[i] = data[VELOCITY][0] + 1j * data[VELOCITY][1]
            self.mass[i] = data[MASS]
            # Check if masses are non-zero
            if self.mass[i] == 0:
                raise RuntimeError("Invalid dict_data! Masses cannot be zero.")
        # == Setting units ==
        if (time_units not in T_UNITS
                or space_units not in S_UNITS
                or mass_units not in M_UNITS):
            raise ValueError("Invalid time_units! (see the docstring)")
        else:
            self.t_units = T_UNITS[time_units]
            self.s_units = S_UNITS[space_units]
            self.m_units = M_UNITS[mass_units]
        # == Save first record in history ==
        if self.no_hist is False:
            self.hist: List[ArrayOfVectors] = []
            self.hist.append(self.pos.copy())

    def __iter__(self) -> "SystemOfBodiesIterator":
        """
        Creates an iterator over the object.
        """
        return SystemOfBodiesIterator(self)

    def __assemble_matrix_R(self) -> MatrixOfVectors:
        """
        Assembles matrix ``R`` of vectors of distances
        between each pair of bodies. (It is antisymmetric)
        """
        R = np.zeros((self.b_num, self.b_num), dtype=VectorType)
        # Go through columns of R and fill elements below the main diagonal;
        # thus creating lower triangular matrix L_R
        for i in range(self.b_num):
            R[i+1:, i] = self.pos[i+1:] - self.pos[i]
        # Subtracting transpose creates antisymmetric matrix
        # from the lower triangular one
        R -= R.T
        # Check that bodies have different positions
        if ((R + np.eye(self.b_num)) == 0).any():
            raise RuntimeError(
                "Invalid positions: Two bodies at one position!")
        return R

    def __assemble_matrix_K(self, R: MatrixOfVectors) -> MatrixOfScalars:
        """
        Assembles matrix ``K`` of coefficients for forces
        between each pair of bodies. (It is symmetric!) \n
        Note that this method does not affect R.

        K_xy = _G * m_1 * m_2 / (‖r_xy‖^3)
        """
        K = np.outer(self.mass, self.mass)  # Create the product of masses
        # Gravitational constant in given units
        __G = G * (self.m_units * (self.t_units ** 2) / (self.s_units ** 3))
        K *= __G  # Multiply each coefficient by the gravitational constant
        # To avoid division by zero on the main diagonal of R,
        # identity matrix is added (it does not affect R in neither context)
        R_ = R + np.eye(self.b_num)
        R_ = np.abs(R_)  # Find norms (moduli) of vectors of distances
        K /= R_ * R_ * R_  # Divide by the 3. power of norms of distances
        return K

    def __assemble_array_F(self, FF: MatrixOfVectors) -> ArrayOfVectors:
        """
        Assembles array ``F`` of forces respective to each body.
        In fact, it is a sum of each vectors in a row respective
        to a body. \n
        Note that this method does not affect the matrix FF of forces.
        """
        F = np.zeros((self.b_num), dtype=VectorType)
        for col in range(self.b_num):
            F += FF[col, :]  # Add whole col to the previous sum
        return F

    def update_accelerations(self) -> None:
        """
        Calculates accelerations of all bodies with respect to
        the current state of the system (positions)
        and updates the array of accelerations.
        """
        # A matrix of vectors of distances between each pair of bodies.
        # (It is antisymmetric!)
        RR: MatrixOfVectors = self.__assemble_matrix_R()
        # A matrix of vectors of coefficients between each pair of bodies.
        # (It is symmetric!)
        KK: MatrixOfVectors = self.__assemble_matrix_K(RR)
        # A matrix of vectors of forces between each pair of bodies.
        # (It is antisymmetric!)
        FF: MatrixOfVectors = RR * KK  # Hadamard product
        # An array of vectors of forces respective to each body
        F: ArrayOfVectors = self.__assemble_array_F(FF)
        # An array of vectors of accelerations respective to each body
        self.acc = F / self.mass  # Hadamard-like division

    def update_positions(self) -> None:
        """
        Calculates positions with respect to the current state
        of the system (positions, velocities and accelerations) and
        updates the array of velocities.

        P = P_0 + V_0 * Δt + 0.5 * A * Δt^2
        """
        # Update positions (s = s_0 + v_0*Δt + 0.5a*Δt^2)
        self.pos += self.vel * self.Δt + (0.5 * (self.Δt ** 2)) * self.acc
        # Append a copy of array of vectors of positions
        if self.no_hist is False:
            self.hist.append(self.pos.copy())

    def update_velocities(self) -> None:
        """
        Calculates velocities with respect to the current state
        of the system (positions, velocities and accelerations) and
        updates the array of velocities.

        V = V_0 + A * Δt
        """
        # Update velocities (v = v_0 + a*Δt)
        self.vel += self.acc * self.Δt


class SystemOfBodiesIterator:
    """
    An iterator over the SystemOfBodies objects.
    Provides a way of simple calculating the next state of a system of bodies.
    """

    def __init__(self, system_of_bodies: SystemOfBodies) -> None:
        """
        Iterator's constructor.
        """
        # Copy of the system of bodies to iterate
        # Copy ensures that the former system is not affected
        self.system_of_bodies = cpy.deepcopy(system_of_bodies)
        # Starting index (iterations stops if index >= system_of_bodies.limit)
        self.index = 0

    def __iter__(self) -> "SystemOfBodiesIterator":
        return self

    def __next__(self) -> SystemOfBodies:
        """
        Internal method for iterating through the iterable SystemOfBodies.
        Returns the SystemOfBodies' next state.
        """
        if self.index >= self.system_of_bodies.limit:
            raise StopIteration
        else:
            self.system_of_bodies.update_accelerations()
            self.system_of_bodies.update_positions()
            self.system_of_bodies.update_velocities()
            self.index += 1
        return self.system_of_bodies

    def __len__(self):
        """
        Returns length, i.e. number of iterations. \n
        It is used even by matplotlib for caching.
        """
        return self.system_of_bodies.limit
