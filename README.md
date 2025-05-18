# A repository for the project to Scientifical Computations in Python
This is a repository that serves for submitting the project to Scientifical Computations in Python. \
Author: Timoteus KUP0148

This Python package implements a small but simply extendable object-oriented framework for video visualization
of 2D simulations of gravitational systems of bodies, particularly systems of planets. Saving into files is also possible. (Note that saving in `mp4` or `avi` requires `ffmpeg`)

More information can be found in docstrings.


## General introduction
The package `planetary2d` consists of the following modules:
- `animator` - a module for handling animations of a system of bodies,
- `bodies_system` - a module implementing core computations of the simulations within one class,
- `data` - a module for a deserialization and data-handling concerning systems of bodies,

**TODO: - `random` - a module for creating random systems of bodies.**

All modules are closely related to each other. The user interface of the package provides several classes and functions which are available from the `planetary2d` namespace.

Classes and functions designated for the user interface:
- `SystemOfBodies` - represents a system of bodies (it is iterable),
- `Animator` - represents a kind of controller for animations of a system of bodies,
- `Randomizer` - represents a generator of random initial conditions of a system of bodies,
- `load_json_data()` - serves to load data from a JSON file.


## Installation notes
To install this package, you can use the `pip` package manager in the root directory (the one with `setup.py` file):
> pip install .


## Examples
You can find examples of usage of the package in `examples/examples.ipynb` Jupyter notebook.


## Simulation quality and degradation
The 2D simulation of a system of bodies utilizes a time discretization (with the assumption of constant
gravitational acceleration over a short period of time).
As a consequence, there is a base discretization interval Δt whose length significantly influences
the quality of the simulation. \
If the base interval is small enough, the simulation is smooth and the degradation
(i.e. the accumulation of the errors) comes into being in much longer time. \
If the base interval is chosen too long, the approximation of the gravitational interactions
breaks very soon, as the acceleration can vary a lot in the meanwhile and the error arising from the
assumption of a constant acceleration over the base interval Δt may grow in a few discretized time steps.
