# HDF5 Data Structure of PyCCAPT Calibration Module

This document provides an overview of the data structure within the HDF5 files of the PyCCAPT calibration module.


This HDF5 file in PyCCAPT contains data with the following columns:

- `x (nm)`: Reconstructed x position in nanometer.
- `y (nm)`: Reconstructed y position in nanometer.
- `z (nm)`: Reconstructed z position in nanometer.
- `mc_c (Da)`: Calibrated mass-to-charge ratio in Daltons.
- `mc (Da)`: Uncalibrated mass-to-charge ratio in Daltons.
- `high-voltage (V)`: Applied DC voltage.
- `pulse`: Applied pulse voltage or laser power.
- `start_counter`: The TDC counter value.
- `t_c (ns)`: Calibrated Time-of-flight in nanosecond.
- `t (ns)`: Uncalibrated Time-of-flight in nanosecond.
- `x_det (cm)`: Detector x hit position of ions.
- `y_det (cm)`: Detector y hit position of ions.
- `pulse_pi`: Pulse since last detected event pulse.
- `ion_pp`: Detected ions for each pulse.