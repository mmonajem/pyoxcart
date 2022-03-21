# PyCCAPT 
# A modular, FAIR open-source python atom probe tomography control software package
![plot](pyccapt/files/logo.png)

Today, the vast majority of atom probe instruments in use are commercial systems with proprietary software. 
This is limiting for many experiments where low-level access to machine control or experiment result data is necessary.
In the beginning this package was implemented for the OXCART atom probe, which is an in-house atom probe. 
The unique feature of OXCART atom probe is that it has a measuring chamber made of titanium to generate a particularly low-hydrogen vacuum.
It was equipped with a highly efficient detector (approx. 80% detection efficiency). 
![plot](pyccapt/files/oxcart.png)
PyCCAPT package provides the basis of a fully FAIR atom probe data collection and analysis chain.  
This repository contains the GUI and control program, which control, visualize, and do the atom probe experiment.
The images below are an overview of the two version of user interface:
![plot](pyccapt/files/oxcart_gui.png)
![plot](pyccapt/files/physic_gui.png)

#  Installation
1- create the virtual environment via Anaconda:
    
    conda create -n myenv 

2- Activate the virtual environment:

    conda activate myenv
    

3- Install package:
    
    python -m pip install -e .
# Running an experiment
TODO
# Citing 
TODO

