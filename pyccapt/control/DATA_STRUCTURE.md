# HDF5 Data Structure of PyCCAPT Control Module

This document provides an overview of the data structure within the HDF5 file of the control software of the PyCCAPT.
In the descriptions below, the notation "(n, )(unit, datatype)" is used to represent one-dimensional arrays with the
unit and data type specified. This structure remains consistent for all other information. For example,
"(n, )(nm, float64)" indicates a one-dimensional array in float64 data type with the unit "nm" (nanometers).
"N/A" is used to indicate that there is no specific unit associated with the data.

## Groups

### Group: `apt`:

The `apt` group contains the data from the APT system in each iteration of the control loop. As a result the frequency
of saving data depends on the frequency of the control loop.

- `high_voltage` (n,) (V, float64): DC voltage value of the power supply.
- `num_event` (n,) (N/A, uint32): Number of detected ions
- `temperature` (n,) (k, float64): Measured Temperature of sample.
- `experiment_chamber_vacuum` (n,) (mBar, float64): Vacuum level in the experiment chamber.
- `time_counter` (n,) (N/A, uint64): Experiment loop iteration counter.
- `timestamps` (n,) (UNIX, float64): UNIX time at which the data was recorded in each iteration with micro second
  accuracy.

### Group: `dld`

The Delay Line Detector (`dld`) group contains the time of flight detector hit coordinates calculated via DLLs. The data
structure of the

- `high_voltage` (n,) (V, float64): DC voltage value of the power supply.
- `voltage_pulse` (n,) (V, float64): Pulse voltage.
- `laser_pulse` (n,) (pJ, float64): Laser pulse energy.
- `start_counter` (n,) (N/A, float64): Description of start counter data.
- `t` (n,) (ns, float64): Time-of-flight for the detected event.
- `x` (n,) (cm, float64): Detector x hit position for the detected event.
- `y` (n,) (cm, float64): Detector y hit position for the detected event.

### Group: `tdc`

Raw data from the Time to Digital Converter (`TDC`) system. The data structure depends on the TDC system used (Surface
Concept ot RoentDek).

#### Surface Concept TDC:

- `channel` (n,) (N/A, uint32): Description of channel data (integer).
- `start_counter` (n,) (N/A, uint64): Start counter of tdc (integer).
- `time_data` (n,) (N/A, uint64): Description of time data (integer).
- `high_voltage` (n,) (V, float64): Applied DC voltage for tdc events (float64).
- `voltage_pulse` (n,) (V, float64): Pulse voltage.
- `laser_pulse` (n,) (pJ, float64): Laser pulse energy.
#### RoentDek TDC:

- `ch0` (n,) (N/A, uint64): Time counter at channel 0 for tdc events, dld 1.
- `ch1` (n,) (N/A, uint64): Time counter at channel 1 for tdc events, dld 1.
- `ch2` (n,) (N/A, uint64): Time counter at channel 2 for tdc events, dld 2.
- `ch3` (n,) (N/A, uint64): Time counter at channel 3 for tdc events, dld 2.
- `ch4` (n,) (N/A, uint64): Time counter at channel 4 for tdc events, dld 3.
- `ch5` (n,) (N/A, uint64): Time counter at channel 5 for tdc events, dld 3.
- `ch6` (n,) (N/A, uint64): Time counter at channel 6 for tdc events, pulse trigger.
- `ch7` (n,) (N/A, uint64): Time counter at channel 7 for tdc events.
- `voltage_pulse` (n,) (V, float64): Pulse voltage.
- `laser_pulse` (n,) (pJ, float64): Laser pulse energy.
