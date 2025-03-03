#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup configuration for PyCCAPT package.
"""
import os
from pathlib import Path
from typing import List, Dict

from setuptools import setup, find_packages

try:
    from pyccapt import version
except BaseException:
    version = "0.1.11"

# Read the README file
def read_me() -> str:
    """Read the README.md file."""
    readme_path = Path(__file__).parent / "README.md"
    if readme_path.exists():
        return readme_path.read_text(encoding="utf-8")
    return ""

# Define package dependencies
def get_dependencies() -> Dict[str, List[str]]:
    """Get package dependencies organized by category."""
    return {
        "calibration": [
            # Core scientific computing
            "numpy>=1.21.0",
            "scipy>=1.7.0",
            "pandas>=1.3.0",
            
            # Data visualization
            "matplotlib>=3.4.0",
            "vispy>=0.10.0",
            "plotly>=5.3.0",
            "kaleido>=0.2.0",
            "pyvista>=0.32.0",
            
            # Data handling
            "h5py>=3.6.0",
            "tables>=3.6.0",
            
            # Data analysis
            "scikit-learn>=0.24.0",
            "pybaselines>=0.2.0",
            "fast-histogram>=0.10.0",
            
            # Jupyter integration
            "ipywidgets>=7.6.0",
            "ipympl>=0.7.0",
            "jupyterlab>=3.0.0",
            
            # Material science
            "pymatgen>=2022.0.0",
            "ase>=3.21.0",
            
            # Utilities
            "numba>=0.54.0",
            "requests>=2.26.0",
            "wget>=3.2.0",
            "deepdiff>=5.5.0",
            "adjustText>=0.7.0",
            "tqdm>=4.62.0",
            "imageio>=2.9.0",
            "nglview>=2.7.0",
        ],
        "control": [
            # GUI components
            "PyQt6>=6.2.0",
            "pyqt6-tools>=6.2.0",
            "pyqtgraph>=0.13.0",
            
            # Hardware control
            "nidaqmx>=0.6.0",
            "pypylon>=2.0.0",
            "pyvisa>=1.11.0",
            "pyserial>=3.5.0",
            "mcculw>=0.1.0",
            
            # Control algorithms
            "simple-pid>=1.0.0",
            
            # Image processing
            "opencv-python>=4.5.0",
            "networkx>=2.6.0",
        ],
        "development": [
            "pytest>=6.2.0",
            "pytest-mock>=3.6.0",
            "pytest-runner>=5.3.0",
            "black>=21.7b0",
            "flake8>=3.9.0",
            "mypy>=0.910",
            "isort>=5.9.0",
            "pre-commit>=2.13.0",
        ],
    }

def get_package_data() -> List[str]:
    """Get package data files."""
    return [
        "*.json",
        "*.txt",
        "*.md",
        "*.yaml",
        "*.yml",
        "files/*",
        "files/readme_images/*",
        "files/logo2.png",
    ]

# Define package extras
def get_extras_require() -> Dict[str, List[str]]:
    """Get package extras with their dependencies."""
    deps = get_dependencies()
    return {
        "dev": deps["development"],
        "full": deps["control"],  # full includes calibration (default) + control
    }

setup(
    name="pyccapt",
    version=version,
    author="Mehrpad Monajem",
    author_email="mehrpad.monajem@fau.de",
    description="A package for controlling APT experiment and calibrating the APT data",
    long_description=read_me(),
    long_description_content_type="text/markdown",
    url="https://github.com/mmonajem/pyccapt",
    project_urls={
        "Bug Tracker": "https://github.com/mmonajem/pyccapt/issues",
        "Documentation": "https://pyccapt.readthedocs.io/",
        "Source Code": "https://github.com/mmonajem/pyccapt",
    },
    packages=find_packages(),
    package_data={"pyccapt": get_package_data()},
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "pyccapt=pyccapt.control.__main__:main",
        ],
    },
    install_requires=get_dependencies()["calibration"],  # Calibration module by default
    extras_require=get_extras_require(),
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    keywords=[
        "atom probe tomography",
        "APT",
        "data analysis",
        "scientific visualization",
        "experiment control",
        "calibration",
    ],
    platforms=["Windows"],
    zip_safe=False,
)
