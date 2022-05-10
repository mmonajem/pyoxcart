#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import exists, dirname, realpath
from setuptools import find_packages, setup
import sys


author = u"Mehrpad Monajem"
# authors in alphabetical order
description = 'A package for calibrating the APT data'
name = 'PyCCAPT_Control'
year = "2022"


sys.path.insert(0, realpath(dirname(__file__))+"/"+name)

try:
    from pyccapt import version
except BaseException:
    version = "unknown"

setup(
    name=name,
    author=author,
    author_email='mehrpad.monajem@fau.de',
    url='https://github.com/mmonajem/pyccapt',
    version=version,
    data_files=[('my_data', ['test/data'])],
    package_dir={'pyccapt.control': './pyccapt/control/'},
    packages=['pyccapt.control', 'pyccapt.control.apt', 'pyccapt.control.devices', 'pyccapt.control.devices_test',
              'pyccapt.control.drs', 'pyccapt.control.gui', 'pyccapt.control.tdc_roentdec',
              'pyccapt.control.tdc_surface_concept', 'pyccapt.control.tools'],
    include_package_data=True,
    license="GPL v3",
    description=description,
    long_description=open('README.md').read() if exists('README.md') else '',
    long_description_content_type="text/markdown",
    install_requires=[
                        "numpy",
                        "matplotlib",
                        "opencv-python",
                        "pandas",
                        "PyQt5",
                        "pyqtgraph",
                        "scikit_learn",
                        "ipywidgets",
                        "networkx",
                        "numba",
                        "requests",
                        "wget",
                        "h5py",
                        "nidaqmx",
                        "pypylon",
                        "tweepy",
                        "pyvisa",
                        "pyvisa-py",
                        "pyserial",
                      ],
    # not to be confused with definitions in pyproject.toml [build-system]
    setup_requires=["pytest-runner"],
    python_requires=">=3.8",
    tests_require=["pytest", "pytest-mock"],
    keywords=[],
    classifiers=['Operating System :: Windows',
                 'Programming Language :: Python :: 3',
                 'Topic :: Scientific/Engineering :: Visualization :: Atom Probe Tomography',
                 'Intended Audience :: Science/Research',
                 ],
    platforms=['ALL'],
)