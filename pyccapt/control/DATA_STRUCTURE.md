# HDF5 Data Structure of PyCCAPT Control Module

This document provides an overview of the data structure within the HDF5 file of the control software of the PyCCAPT.

## Groups

### Group: `apt`

- `high_voltage`: Applied DC voltage in the current iteration.
- `pulse`: Applied pulse voltage or laser power in the current iteration.
- `num_event`: Number of detected ions since last control loop iteration.
- `temperature`: Temperature level in each control loop iteration.
- `main_chamber_vacuum`: Vacuum level in each control loop iteration.
- `time_counter`: Experiment time counter of the PyCCAPT control software.
- `second`: Time at which the data was recorded in each iteration.
- `minute`: Time at which the data was recorded in each iteration.
- `hour`: Time at which the data was recorded in each iteration.

### Group: `dld`

- `high_voltage`: Applied DC voltage for dld events.
- `pulse`: Applied pulse voltage or laser power for dld events.
- `start_counter`: Description of start counter data.
- `t`: Description of t data.
- `x`: Description of x data.
- `y`: Description of y data.

### Group: `tdc`

Raw data from the TDC system. Te data structure depends on the TDC system used.

#### Surface Concept TDC:

- `channel`: Description of channel data.
- `high_voltage`: Applied DC voltage for tdc events.
- `pulse_voltage`: Applied pulse voltage or laser power for tdc events.
- `start_counter`: Start counter of tdc.
- `time_data`: Description of time data.


#### RoentDek TDC:

- `ch0`: Time counter at channel 0 for tdc events (dld 1).
- `ch1`: Time counter at channel 1 for tdc events (dld 1).
- `ch2`: Time counter at channel 2 for tdc events (dld 2).
- `ch3`: Time counter at channel 3 for tdc events (dld 2).
- `ch4`: Time counter at channel 4 for tdc events (dld 3).
- `ch5`: Time counter at channel 5 for tdc events (dld 3).
- `ch6`: Time counter at channel 6 for tdc events (pulse trigger).
- `ch7`: Time counter at channel 7 for tdc events.
- `high_voltage`: Applied DC voltage for tdc events.
- `pulse`: Applied pulse voltage or laser power for tdc events.


