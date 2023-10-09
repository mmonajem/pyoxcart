# HDF5 Data Structure of PyCCAPT Calibration Module and related range file

This document provides an overview of the data structure within the HDF5 files of the PyCCAPT calibration module.

### HDF5 file structure of PyCCAPT calibration module


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

There is also possibility to convert the PyCCAPT HDF5 file data to EPOS, POS, ATO, and CSV file. You can find the
example code in the tutorial section.


### Range HDF5 file structure of PyCCAPT 

The range file contains the range of the mass-to-charge ratio. The range file is a HDF5 file with the following

- `ion`: Ions name in latex format (string).
- `mass`: The mass-to-charge ratio of the peak base on the elements weight and complexity (float64).
- `mc`: Mass-to-charge ratio in the dataset for the peak (float64).
- `mc_low`: The lower bound of the mass-to-charge ratio in the dataset for the peak (float64).
- `mc_up`: The upper bound of the mass-to-charge ratio in the dataset for the peak (float64).
- `color`: The color of the peak in the plot (hex).
- `element`: list of elements in the peak (list of string).
- `complex`: complexity of the element (integer).
- `isotope`: isotope list of element (list of integer).
- `charge`: charge of the element (integer).

