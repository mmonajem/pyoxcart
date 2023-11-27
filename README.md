# PyCCAPT (APT_PyControl)

# A modular, FAIR open-source python atom probe tomography software package for experiment control and data calibration

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7588996.svg)](https://doi.org/10.5281/zenodo.7588996)
[![Documentation Status](https://readthedocs.org/projects/pyccapt/badge/?version=latest)](https://pyccapt.readthedocs.io/en/latest/?badge=latest)
<!--[![coverage report](https://gitlab.com/jesseds/apav/badges/master/coverage.svg)](https://gitlab.com/jesseds/apav/commits/master)
[![pipeline status](https://gitlab.com/jesseds/apav/badges/master/pipeline.svg)](https://gitlab.com/jesseds/apav/-/commits/master)-->

<img align="right" src="pyccapt/files/logo2.png" alt="Alt Text" width="300" height="300">

This package aims to provide open-source software for controlling atom probe systems and calibrating data.
The package is modular and adaptable for a wide range of devices in atom probe instrument. So far it is
capable of collecting data from Surface consept and ReoenDek TDC systems. The package is developed in Python 3.9.
Additionally, the package encompasses a comprehensive calibration module that provides various functionalities,
including t<sub>0</sub> and flight path calculation, region of interest (ROI) selection, voltage and bowl calibration,
as well as
3D reconstruction techniques.
This module enhances the capabilities of PyCCAPT by providing essential tools for accurate data interpretation and
analysis.

----------
![](https://github.com/mmonajem/pyccapt/blob/main/pyccapt/files/logo2.png)

# Presentation

PyCCAPT was initially developed and rigorously tested on the OXCART atom probe, an in-house atom probe system situated
within the Department of Materials Science & Engineering at the University of Erlangen-Nürnberg. Distinguished by its
unique attribute, the OXCART atom probe boasts a titanium-based measuring chamber that facilitates an ultra-low hydrogen 
vacuum environment. This system also features a state-of-the-art detector with a high detection
efficiency of approximately 80%. While tailor-made for the OXCART, the PyCCAPT package offers versatility, extending its
capabilities to effectively manage diverse atom probe systems.

![](https://github.com/mmonajem/pyccapt/blob/main/pyccapt/files/oxcart.jpg)

The package is designed with modularity in mind, making it highly adaptable to a diverse array of instruments. This
adaptability extends to instruments like Pfeifer gauges, Fug power supplies, and Siglent signal generators. Notably, the
PyCCAPT package has already demonstrated its proficiency in collecting data from Surface Concept and ReoenDek TDC
systems, showcasing its versatility across various setups and applications.

The PyCCAPT package forms the foundation of a fully FAIR atom probe data collection and processing chain. This
repository includes the graphical user interface (GUI) and control program, which enable experiment control,
visualization, and data acquisition. The following images provide an overview of the user interface:

![](https://github.com/mmonajem/pyccapt/blob/main/pyccapt/files/advance_gui.png)

 ---------------------

# Directory structure
```
pyccapt/
├── pyccapt/
│   ├── __init__.py
│   ├── config.json   
│   ├── calibration/
│   │   ├── __init__.py
│   │   └── module_folders   
│   ├── control/
│   │   ├── __init__.py
│   │   └── module_folders
│   └── files/
├── docs/
├── setup.py
├── README.md
├── CONTRIBUTION.md
├── MANIFEST.in
├── Licence
└── tox.ini
└── tests/
    ├── __init__.py
    ├── data/
    └── tests
```
 ---------------------

# Installation

1. Create a virtual environment using Anaconda:

   ```bash
   conda create -n apt_env python=3.9
    ```

2. Activate the virtual environment:

   ```bash
   conda activate apt_env
   ```

3. Clone or download this repository, unzip it, and in the project directory run:

   ```bash
   pip install -e .
   ```

After installation, you can run the control GUI by entering the following command in the console:

   ```bash
   pyccapt
   ```

or if the above command does not work, you can run the following command:

   ```bash
   python -m pyccapt.control
   ```


To start the tutorial, please follow these steps:

1- Open your terminal.

2- Navigate to the project folder using the cd command.

3- Once you're inside the project folder, go to the tutorial folder by running the following command:

   ```bash
   Jupyter lab
   ```

--------------

# Documentation

The latest documentation is available on
[ReadTheDocs](https://pyccapt.readthedocs.io/en/latest/?#) page. It provides feature descriptions, tutorials, and
valuable information.


---------------------
# Using PyCCAPT

For control part of the package you can follow the steps
on [documentation](https://pyccapt.readthedocs.io/en/latest/configuration.html).

For calibration, review the [tutorial](https://pyccapt.readthedocs.io/en/latest/tutorials.html) to understand package
features.

---------------------
# Data structure

For checking the data structure of the control module you can check [here](pyccapt/control/DATA_STRUCTURE.md). For the 
calibration module, you can check [here](pyccapt/calibration/DATA_STRUCTURE.md).

---------------------
# Test data

For start using the calibration package, you can use the test data (pure Aluminium) provided in the following link. The
link contains the raw dataset that is collected from the OXCART atom probe from a pure Aluminium sample. It also
contains
the output file from the calibration module, which contains the calibrated data as well as the reconstructed data. The
link also contain the range file (HDF5) that is calculated by the calibration module.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10131887.svg)](https://doi.org/10.5281/zenodo.10131887)

------------------
# Bug reports

Report bugs, issues, ask for help, or provide feedback on
the [github section](https://github.com/mmonajem/pyccapt/issues).

Qestions/comments:
  - Mehrpad Monajem, mehrpad.monajem@fau.de

-----------

# Citing

-----------

# Contributing

Contributions to PyCCAPT are always welcome, and they are greatly appreciated! Our contribution
policy can be found [here](CONTRIBUTING.md).

------------

# License

This project is licensed under the GNU General Public License v3.0. See
the [LICENSE](LICENSE) file for details.