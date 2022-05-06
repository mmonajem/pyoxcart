.. PyCCAPT documentation master file, created by
   sphinx-quickstart on Wed Mar 23 16:07:41 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PyCCAPT:  A modular, FAIR open-source Python package for controlling and calibrating atom probe tomography
===================================

Historically, atom probe tomography (APT) detection systems have used compiled systems with hardware-software co-design to deal with the high data rates generated at the detector.
In recent years, while computer hardware power has continuously increased, the rate of atoms measured has not significantly increased due to the physical limitations of the experiment [1].
As a result, more and more computationally expensive high level programming approaches can be used to control APT instruments.
Additionally, the highly complex field evaporation in laser pulsed atom probe has made it highly desirable to get ever deeper insights into the detector events [2].

PyCCAPT is an open-source atom probe control and calibrate system written in the Python programming language.
The collected data is stored in a FAIR (findable, accessible, interoperable and reusable) data format (HDF5) which contains all data collected during the experiment, including detector raw data.
This control system therefore provides the basis of a fully FAIR atom probe data collection and analysis chain.

Documentation
========================
The documentation webpage of PyCCAPT modules can be found here.

PyCCAPT:
===================

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   installation
   tutorials
   pyccapt
   code_reference
   appendix
   bibliography


Bibliography
========================
1. B. Gault et al., Atom probe tomography. Nat Rev Methods Primers 1, 52 (2021).
2. D. W. Saxey, Correlated ion analysis and the interpretation of atom probe mass spectra Ultramicroscopy 111 473–9 (2011).

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
