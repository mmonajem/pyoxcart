#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import exists

from setuptools import setup, find_packages

try:
    from pyccapt import version
except BaseException:
    version = "0.0.35"

common_deps = [
    "numpy",
    "matplotlib",
    "pandas",
    "PyQt6",
    "networkx",
    "numba",
    "requests",
    "wget",
    "h5py",
    "tables",
    "deepdiff",
]

control_deps = [
    "opencv-python",
    "pyqt6-tools",
    "pyqtgraph",
    "nidaqmx",
    "pypylon",
    "pyvisa",
    "pyvisa-py",
    "pyserial",
    "deepdiff",
    "scipy",
    "mcculw",
]

calibration_deps = [
    "ipywidgets",
    "ipympl",
    "scikit_learn",
    "vispy",
    "plotly",
    "faker",
    "jupyterlab",
    "scipy",
    "nodejs",
    "adjustText",
    "pybaselines ",
    "kaleido",
    "pymatgen",
    "ase",
    "imageio",
	"nglview",
]

setup(
    name='pyccapt',
    author=u"Mehrpad Monajem",
    author_email='mehrpad.monajem@fau.de',
    url='https://github.com/mmonajem/pyccapt',
    version=version,
    entry_points={
            'console_scripts': {
                'pyccapt=pyccapt.control.__main__:main',
                }
    },
    data_files=[('my_data', ['./tests/data'])],
    packages=find_packages(),
    license="GPL v3",
    description='A package for controlling APT experiment and calibrating the APT data',
    long_description=open('README.md').read() if exists('README.md') else '',
    long_description_content_type="text/markdown",
    install_requires=common_deps + control_deps + calibration_deps,
    # not to be confused with definitions in pyproject.toml [build-system]
    setup_requires=["pytest-runner"],
    python_requires=">=3.9",
    tests_require=["pytest", "pytest-mock"],
    keywords=[],
    classifiers=['Operating System :: Microsoft :: Windows',
                 'Programming Language :: Python :: 3',
                 'Topic :: Scientific/Engineering :: Visualization',
                 'Intended Audience :: Science/Research',
                 ],
    platforms=['ALL'],
)