# HDF5 Data Structure of PyCCAPT Calibration Module

This document provides an overview of the data structure within the HDF5 files of the PyCCAPT calibration module.


This HDF5 file in PyCCAPT contains data with the following columns:

- `x (nm)`: Description of the x-coordinate data in nanometers.
- `y (nm)`: Description of the y-coordinate data in nanometers.
- `z (nm)`: Description of the z-coordinate data in nanometers.
- `mc_c (Da)`: Description of the MC_c (mass-to-charge) data in Daltons.
- `mc (Da)`: Description of the MC (mass-to-charge) data in Daltons.
- `high-voltage (V)`: Description of the high-voltage data in Volts.
- `pulse`: Description of the pulse data.
- `start_counter`: Description of the start counter data.
- `t_c (ns)`: Description of the t_c (time) data in nanoseconds.
- `t (ns)`: Description of the t (time) data in nanoseconds.
- `x_det (cm)`: Description of the x_det (detection x-coordinate) data in centimeters.
- `y_det (cm)`: Description of the y_det (detection y-coordinate) data in centimeters.
- `pulse_pi`: Description of the pulse_pi data.
- `ion_pp`: Description of the ion