.. PyCCAPT documentation master file, created by
   sphinx-quickstart on Wed Mar 23 16:07:41 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PyCCAPT:  A Modular, FAIR Open-source Python Package for Controlling and Calibrating Atom Probe Tomography
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
The webpage contains the documentation for the PyCCAPT package. The documentation is divided into several
sections, including installation, control, calibration, tutorials, and modules.
The documentation provides a comprehensive guide to the PyCCAPT package, including detailed descriptions of
the control and calibration data structures, as well as tutorials on how to use the package. The documentation
also includes information on how to install the package and how to configure it for use with different types of
atom probe instruments.


Most PyCCAPT software outputs are in the form of
`Pandas DataFrames <https://pandas.pydata.org/pandas-docs/stable/reference/frame.html>`_, offering flexibility for seamless expansion with
additional information across various levels of analysis. The control and calibration data structures can be referenced
`here <https://github.com/mmonajem/pyccapt/blob/main/pyccapt/control/DATA_STRUCTURE.md>`_. and `here <https://github.com/mmonajem/pyccapt/blob/main/pyccapt/calibration/DATA_STRUCTURE.md/>`_., respectively. Leveraging the capabilities of Pandas allows users to work with the analyzed data effortlessly,
facilitating interoperability.

The choice of HDF5 as a storage format is notable for its widespread readability across different programming languages.
HDF5 adopts a file directory-like structure, enabling users to organize data systematically within the file. Moreover,
HDF5 supports large, intricate, and heterogeneous datasets. Its inherent structure is self-description,
as users can embed metadata, enhancing the overall comprehensibility of the stored information.

PyCCAPT:
===================

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   installation
   control_index
   configuration
   calibration_index
   modules
   license
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
