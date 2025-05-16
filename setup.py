# Setup python script for the installation of this package

# Imports
from setuptools import setup, find_packages

# Setting up
setup(
    name='planetary2d',  # Name of the package
    version='1.0.0',  # Version of the package
    license='MIT',  # License of the package to be distributed under
    packages=find_packages(),  # ??????
    # Packages required for this package (maybe 'numba')
    install_requires=['json', 'numpy', 'matplotlib']
)

# For mp4 format it needs ffmpeg to be installed in the system!!!
