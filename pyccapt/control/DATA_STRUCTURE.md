# HDF5 Data Structure of PyCCAPT Control Module

This document provides an overview of the data structure within the HDF5 file of the control software of the PyCCAPT.

## Groups

### Group: `apt`

- `high_voltage`: Applied DC voltage in the current iteration (float64).
- `pulse`: Applied pulse voltage or laser power in the current iteration (float64).
- `num_event`: Number of detected ions since last control loop iteration (integer).
- `temperature`: Temperature level in each control loop iteration (float64).
- `main_chamber_vacuum`: Vacuum level in each control loop iteration (float64).
- `time_counter`: Experiment time counter of the PyCCAPT control software (integer).
- `second`: Time at which the data was recorded in each iteration (integer).
- `minute`: Time at which the data was recorded in each iteration (integer).
- `hour`: Time at which the data was recorded in each iteration (integer).

### Group: `dld`

- `high_voltage`: Applied DC voltage for dld events (float64).
- `pulse`: Applied pulse voltage or laser power for dld events (float64).
- `start_counter`: Description of start counter data (float64).
- `t`: Time-of-flight for the detected event (float64).
- `x`: Detector x hit position for the detected event (float64).
- `y`: Detector y hit position for the detected event (float64).

### Group: `tdc`

Raw data from the TDC system. Te data structure depends on the TDC system used.

#### Surface Concept TDC:

- `channel`: Description of channel data (integer).
- `high_voltage`: Applied DC voltage for tdc events (float64).
- `pulse_voltage`: Applied pulse voltage or laser power for tdc events (float64).
- `start_counter`: Start counter of tdc (integer).
- `time_data`: Description of time data (integer).


#### RoentDek TDC:

- `ch0`: Time counter at channel 0 for tdc events, dld 1 (integer).
- `ch1`: Time counter at channel 1 for tdc events, dld 1 (integer).
- `ch2`: Time counter at channel 2 for tdc events, dld 2 (integer).
- `ch3`: Time counter at channel 3 for tdc events, dld 2 (integer).
- `ch4`: Time counter at channel 4 for tdc events, dld 3 (integer).
- `ch5`: Time counter at channel 5 for tdc events, dld 3 (integer).
- `ch6`: Time counter at channel 6 for tdc events, pulse trigger (integer).
- `ch7`: Time counter at channel 7 for tdc events (integer).
- `high_voltage`: Applied DC voltage for tdc events (float64).
- `pulse`: Applied pulse voltage or laser power for tdc events (float64).


