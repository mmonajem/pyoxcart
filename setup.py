#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import exists, dirname, realpath
from setuptools import setup, find_packages
import sys

author = u"Mehrpad Monajem"
# authors in alphabetical order
description = 'Atom Probe Tomography Experiment Control with Python'
name = 'APT_PyControl'
year = "2022"


sys.path.insert(0, realpath(dirname(__file__))+"/"+name)
try:
    from apt_pycontrol import version
except BaseException:
    version = "unknown"

    # packages=['calibration'],
setup(
    name=name,
    author=author,
    author_email='mehrpad.monajem@fau.de',
    url='https://github.com/mmonajem/apt_pycontrol',
    version=version,
    packages=find_packages(),
    entry_points={
            'console_scripts': [
                'my_start=my_package.__main__:main',
            ]
    },
    data_files=[('my_data', ['test/data'])],
    package_dir={name: name},
    include_package_data=True,
    license="GPL v3",
    description=description,
    long_description=open('README.md').read() if exists('README.md') else '',
    long_description_content_type="text/markdown",
    install_requires=[
                        "numpy>=1.19.0",
                        "scipy>=0.14.0",
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
                        "pyserial",
                      ],
    # not to be confused with definitions in pyproject.toml [build-system]
    setup_requires=["pytest-runner"],
    python_requires=">=3.7",
    tests_require=["pytest", "pytest-mock"],
    keywords=[],
    classifiers=['Operating System :: Windows',
                 'Programming Language :: Python :: 3',
                 'Topic :: Scientific/Engineering :: Visualization',
                 'Intended Audience :: Science/Research',
                 ],
    platforms=['ALL'],
)