from setuptools import setup, find_packages

setup(
    name='planetary2d',
    version='1.0.0',
    license='MIT',
    packages=find_packages(),
    # Packages required for this package (maybe 'numba')
    install_requires=['json', 'numpy', 'matplotlib']
)

# For mp4 format it needs ffmpeg to be installed in the system!!!