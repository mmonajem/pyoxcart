Installation
===============================

From PyPi
---------

To install PyCCAPT using PyPi, enter the following command in the console:

``pip install pyccapt``

to install the control packages, enter the following command:

``pip install pyccapt-control``

and to to install the calibration packages separately, enter the following command:

``pip install pyccapt-calibration``


Local installation of PyCCAPT
----------------------------
Clone/download this repository and unzip it. In the project directory enter the following command:

``pip install -e .``

to install the control packages, enter the following command:

``cd pyccapt/control && pip install -e .``

and to to install the calibration packages separately, enter the following command:

``cd pyccapt/calibration && pip install -e .``


Running PyCCAPT control GUI
------------------
Once the installation is done and the python environment is activated, enter the following command in the
console:

``pyccapt``


Running PyCCAPT Tutorials
------------------------
Once the installation is done and the python environment is activated, enter the following command in the console:

``python -m pyccapt.Tutorials``


Testing
-------
To run the tests, please activate the PyCCAPT virtual environment. In the project directory,
in the console, enter the following command:

``python setup.py test``

