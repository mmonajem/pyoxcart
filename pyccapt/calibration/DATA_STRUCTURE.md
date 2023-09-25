# HDF5 Data Structure of PyCCAPT Calibration Module

This document provides an overview of the data structure within the HDF5 files of the PyCCAPT calibration module.


This HDF5 file in PyCCAPT contains data with the following columns:

- `x (nm)`: Reconstructed x position in nanometer (float64).
- `y (nm)`: Reconstructed y position in nanometer (float64).
- `z (nm)`: Reconstructed z position in nanometer (float64).
- `mc_c (Da)`: Calibrated mass-to-charge ratio in Daltons (float64).
- `mc (Da)`: Uncalibrated mass-to-charge ratio in Daltons (float64).
- `high-voltage (V)`: Applied DC voltage (float64).
- `pulse`: Applied pulse voltage or laser power (float64).
- `start_counter`: The TDC counter value (integer).
- `t_c (ns)`: Calibrated Time-of-flight in nanosecond (float64).
- `t (ns)`: Uncalibrated Time-of-flight in nanosecond (float64).
- `x_det (cm)`: Detector x hit position of ions (float64).
- `y_det (cm)`: Detector y hit position of ions (float64).
- `pulse_pi`: Pulse since the last detected event pulse (integer).
- `ion_pp`: Detected ions for each pulse (integer).