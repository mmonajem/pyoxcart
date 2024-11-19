#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import exists

from setuptools import setup

try:
    from pyccapt import version
except BaseException:
    version = "0.0.35"

colab_deps = [
]
common_deps = [
    "numpy",
    "matplotlib",
    "pandas",
    "PyQt6",
    "numba",
    "requests",
    "wget",
    "deepdiff",
]

control_deps = [
    "opencv-python",
    "networkx",
    "pyqt6-tools",
    "pyqtgraph",
    "nidaqmx",
    "pypylon",
    "pyvisa",
    "pyserial",
    "deepdiff",
    "scipy",
    "h5py",
    "tables",
    "mcculw",
    "simple-pid",
]

calibration_deps = [
    "ipywidgets",
    "ipympl",
    "scikit_learn",
    "vispy",
    "plotly",
    "faker",
    "scipy",
    "nodejs",
    "adjustText",
    "pybaselines ",
    "kaleido",
    "pymatgen",
    "ase",
    "imageio",
    "nglview",
    "jupyterlab",
    "tqdm",
    "fast-histogram",
]

package_list_control = ['pyccapt', 'tests', 'pyccapt.control', 'pyccapt.control.apt', 'pyccapt.control.control',
                        'pyccapt.control.devices', 'pyccapt.control.devices_test', 'pyccapt.control.drs',
                        'pyccapt.control.gui', 'pyccapt.control.nkt_photonics', 'pyccapt.control.tdc_roentdek',
                        'pyccapt.control.tdc_surface_concept', 'pyccapt.control.thorlabs_apt',
                        'pyccapt.control.usb_switch']

package_list_calibration = ['pyccapt', 'tests', 'pyccapt.calibration', 'pyccapt.calibration.calibration',
                            'pyccapt.calibration.clustering', 'pyccapt.calibration.data_tools',
                            'pyccapt.calibration.leap_tools', 'pyccapt.calibration.mc',
                            'pyccapt.calibration.reconstructions', 'pyccapt.calibration.tutorials',
                            'pyccapt.calibration.tutorials.tutorials_helpers']

dependency_list = control_deps + calibration_deps + common_deps
package_list = package_list_control + package_list_calibration

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
    packages=package_list,
    license="GPL v3",
    description='A package for controlling APT experiment and calibrating the APT data',
    long_description=open('README.md').read() if exists('README.md') else '',
    long_description_content_type="text/markdown",
    install_requires=dependency_list,
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
