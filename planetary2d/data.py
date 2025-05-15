"""
``planetary2d.data``
=============================

The ``planetary2d.data`` module provides functinos for data handling
and utilities for deserializing initial-conditions data from a data file.

It supports only *JSON file format* yet.

Please note that the most important function ``load_json_data`` is present
in the main ``planetary2d`` namespace.

Constants and functions present in ``planetary2d.data`` listed below.

Data handling constants
-----------------------
- POSITION
- VELOCITY
- MASS

Data handling functions
-----------------------
- try_structure()

JSON utilities functions
------------------------
- load_json_data()

"""

# Imports
import json


# Constant string keywords for parameters of a body
POSITION = 'position'
VELOCITY = 'velocity'
MASS = 'mass'
# Constant for the dimension of vectors to load from data file (by default 2D)
__VEC_DIM = 2


def try_structure(dict_data: dict) -> bool:
    """
    Tries if the structure of ``dict_data`` complies with required pattern.

    :param dict_data: Dictionary of initial conditions
    :type dict_data: dict

    :returns: True if ``dict_data`` complies with required pattern and False
    if it does not
    :rtype: has_proper_struct (bool)
    """
    # Browses each body in the data dictionary
    for body in dict_data.values():
        # Returns False if
        # - any keyword is missing,
        # - types of values for the keywords does not fit (list, float...),
        # - dimension of vectorial variables does not fit,
        # - type of components of vectors is not a kind of a real number.
        try:
            if not (
                (POSITION in body
                 and isinstance(body[POSITION], list)
                 and len(body[POSITION]) == __VEC_DIM
                 and all(isinstance(val, (float, int)) for val in body[POSITION]))
                and
                (VELOCITY in body
                 and isinstance(body[VELOCITY], list)
                 and len(body[VELOCITY]) == __VEC_DIM
                 and all(isinstance(val, (float, int)) for val in body[VELOCITY]))
                and
                (MASS in body
                 and isinstance(body[MASS], (float, int)))):
                return False
        except TypeError:
            return False

    return True


def load_json_data(path_to_json: str) -> dict:
    """
    Loads JSON data file and tests if it is properly structured.

    Structure of data
    -----------------
    The structure of JSON file should follow this pattern::

        {
            "name_of_the_body" : {
                "position" : [
                    float,
                    float
                ],
                "velocity" : [
                    float,
                    float
                ],
                "mass" : float
            },
            ...
        }

    where ``"position"``, ``"velocity"`` and ``"mass"`` are keywords that
    have to be preserved. (Note that other parameters of a body are ignored)

    Number of bodies in the data file is not limited.

    :param path_to_json: Absolute or relative path to the JSON data file
    :type path_to_json: str (it can also be any type which is supported by
    the function ``open``)

    :returns: Dictionary of initial conditions
    :rtype: dict_data (dict)
    """
    # Read JSON file to dictionary
    with open(path_to_json, 'r') as infile:
        dict_data = json.load(infile)

    # Test the data structure
    if not try_structure(dict_data):
        raise RuntimeError(
            "The JSON data file does not meet the prescribed structure!")

    return dict_data
