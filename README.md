# PyCCAPT 
# A modular, FAIR open-source python atom probe tomography software package for controlling experiment and calibrating data 
![plot](pyccapt/files/logo.png)
[![Documentation Status](https://readthedocs.org/projects/pyccapt/badge/?version=latest)](https://pyccapt.readthedocs.io/en/latest/?badge=latest)
[![PyPi version](https://badgen.net/pypi/v/pyccapt/)](https://pypi.org/project/pyccapt)

/pypi/license/pip
This package aims to provide an open-source software for controlind atom probe systems and calibrate 
the data. The package is modular and can be used in a wide range of applications.

----------

# Presentation

Today, the vast majority of atom probe instruments in use are commercial systems with proprietary software. 
This is limiting for many experiments where low-level access to machine control or experiment result data is necessary.
This package was tested on the OXCART atom probe, which is an in-house atom probe. 
The unique feature of OXCART atom probe is that it has a measuring chamber made of titanium to generate a particularly low-hydrogen vacuum.
It was equipped with a highly efficient detector (approx. 80% detection efficiency). This package is also used to control
other atom probe systems.

![plot](pyccapt/files/oxcart.png)

PyCCAPT package provides the basis of a fully FAIR atom probe data collection and analysis chain.  
This repository contains the GUI and control program, which control, visualize, and do the atom probe experiment.
The images below are an overview of the two version of user interface:

![plot](pyccapt/files/oxcart_gui.png)
![plot](pyccapt/files/physic_gui.png)

 ---------------------

#  Installation
1- create the virtual environment via Anaconda:
    
    conda create -n apt_env python=3.8 

2- Activate the virtual environment:

    conda activate apt_env

3- Install the package:

    pip install pyccapt

if you want to only install control package then:

    pip install pyccapt-control

or for calibration package:

    pip install pyccapt-calibration

4- Install package locally:
    
    pip install -e .

if you want to only install control package then:
    
    cd pyccapt/control
    pip install -e .

or for calibration package:

    cd pyccapt/calibration
    pip install -e .


--------------
# Documentation

The latest versions of the documentation can be accessed on our
[ReadTheDocs](https://pyccapt.readthedocs.io/en/latest/?#) page. It contains descriptions of
Crappy's features, tutorials, and other useful information.

--------------------

# Edite GUI 

Edite the GUI with Qt-Designer and run command below to create your own GUI
UI (simple or advance) in the GUI module. 

    pyuic5 -x gui_simple_layout.ui -o gui_simple_layout.py. You should then merge the created file with the targeted 
---------------------
# Running an experiment

modify the congig.json file. Type pyccapt in your command line.

------------------
# Bug reports

Please report bugs, issues, ask for help or give feedback in the [github section](https://github.com/mmonajem/pyccapt/issues).

-----------
# Citing 


