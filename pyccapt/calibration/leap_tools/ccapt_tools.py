import struct
from itertools import chain
import numpy as np
import pandas as pd

# Local module and scripts
from pyccapt.calibration.leap_tools import leap_tools

def ccapt_to_pos(data, path=None, name=None):

    dd = data[['x (nm)', 'y (nm)', 'z (nm)', 'mc_c (Da)']]
    dd = dd.astype(np.single)
    records = dd.to_records(index=False)
    list_records = list(records)
    d = tuple(chain(*list_records))
    pos = struct.pack('>' + 'ffff' * len(dd), *d)
    if name is not None:
        with open(path + name, 'w+b') as f:
            f.write(pos)
    return pos


def ccapt_to_epos(data, pulse_mode, path=None, name=None):
    if pulse_mode == 'voltage':
        dd = data[
            ['x (nm)', 'y (nm)', 'z (nm)', 'mc_c (Da)', 't (ns)', 'high_voltage (V)', 'pulse (V)', 'x_det (cm)',
             'y_det (cm)',
             'pulse_pi', 'ion_pp']]
    elif pulse_mode == 'laser':
        dd = data[
            ['x (nm)', 'y (nm)', 'z (nm)', 'mc_c (Da)', 't (ns)', 'high_voltage (V)', 'pulse (deg)', 'x_det (cm)',
             'y_det (cm)',
             'pulse_pi', 'ion_pp']]

    dd = dd.astype(np.single)
    dd = dd.astype({'pulse_pi': np.uintc})
    dd = dd.astype({'ion_pp': np.uintc})

    records = dd.to_records(index=False)
    list_records = list(records)
    d = tuple(chain(*list_records))
    epos = struct.pack('>'+'fffffffffII'*len(dd), *d)
    if name is not None:
        with open(path + name, 'w+b') as f:
            f.write(epos)

    return epos

def pos_to_ccapt(data):

    pos = leap_tools.read_pos(data)
    length = len(pos['m/n (Da)'].to_numpy())
    ccapt = pd.DataFrame({'x (nm)': pos['x (nm)'].to_numpy(),
                          'y (nm)': pos['y (nm)'].to_numpy(),
                          'z (nm)': pos['z (nm)'].to_numpy(),
                          'mc_c (Da)': pos['m/n (Da)'].to_numpy(),
                          'mc (Da)': np.zeros(length),
                          'high_voltage (V)': np.zeros(length),
                          'pulse (V)': np.zeros(length),
                          'start_counter': np.zeros(length),
                          't (ns)': np.zeros(length),
                          't_c (nm)': np.zeros(length),
                          'x_det (cm)': np.zeros(length),
                          'y_det (cm)': np.zeros(length),
                          'pulse_pi': np.zeros(length, dtype=int),
                          'ion_pp': np.zeros(length, dtype=int),
                          })
    return ccapt


def epos_to_ccapt(data):
    epos = leap_tools.read_epos(data)
    length = len(epos['m/n (Da)'].to_numpy())
    ccapt = pd.DataFrame({'x (nm)': epos['x (nm)'].to_numpy(),
                          'y (nm)': epos['y (nm)'].to_numpy(),
                          'z (nm)': epos['z (nm)'].to_numpy(),
                          'mc_c (Da)': epos['m/n (Da)'].to_numpy(),
                          'mc (Da)': np.zeros(length),
                          'high_voltage (V)': epos['HV_DC (V)'].to_numpy(),
                          'pulse (V)': epos['pulse (V)'].to_numpy(),
                          'start_counter': np.zeros(length),
                          't (ns)': epos['TOF (ns)'].to_numpy(),
                          't_c (nm)': np.zeros(length),
                          'x_det (cm)': epos['det_x (cm)'].to_numpy(),
                          'y_det (cm)': epos['det_y (cm)'].to_numpy(),
                          'pulse_pi': epos['pslep'].to_numpy(),
                          'ion_pp': epos['ipp'].to_numpy(),
                          })
    return ccapt