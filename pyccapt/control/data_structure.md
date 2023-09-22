# HDF5 Data Structure of PyCCAPT Control Module

This document provides an overview of the data structure within the HDF5 file.

## Groups

### Group: `apt`

- `high_voltage`: Description of high voltage data.
- `pulse`: Description of pulse data.
- `num_event`: Description of the number of events data.
- `temperature`: Description of temperature data.
- `main_chamber_vacuum`: Description of main chamber vacuum data.
- `time_counter`: Description of time counter data.

### Group: `dld`

- `high_voltage`: Description of high voltage data.
- `pulse`: Description of pulse data.
- `start_counter`: Description of start counter data.
- `t`: Description of t data.
- `x`: Description of x data.
- `y`: Description of y data.

### Group: `tdc`

Raw data from the TDC system. Te data structure depends on the TDC system used.

#### Surface Concept TDC:

- `channel`: Description of channel data.
- `high_voltage`: Description of high voltage data.
- `pulse_voltage`: Description of pulse voltage data.
- `start_counter`: Description of start counter data.
- `time_data`: Description of time data.


#### RoentDek TDC:

- `ch0`: Description of channel 0 data.
- `ch1`: Description of channel 1 data.
- `ch2`: Description of channel 2 data.
- `ch3`: Description of channel 3 data.
- `ch4`: Description of channel 4 data.
- `ch5`: Description of channel 5 data.
- `ch6`: Description of channel 6 data.
- `ch7`: Description of channel 7 data.
- `high_voltage`: Description of high voltage data.
- `pulse`: Description of pulse data.



### Group: `time`

- `second`: Description of second data.
- `minute`: Description of minute data.
- `hour`: Description of hour data.