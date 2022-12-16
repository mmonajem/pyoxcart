import struct
from itertools import chain
import numpy as np

def hdf5_to_pos(data, path=None, name=None):
    """
    Loads an APT a pandas dataframe as .pos file .

    Columns:
        x: Reconstructed x position
        y: Reconstructed y position
        z: Reconstructed z position
        Da: Mass/charge ratio of i
    """
    dd = data[['x (nm)', 'y (nm)', 'z (nm)', 'mc (Da)']]
    dd = dd.astype(np.single)
    records = dd.to_records(index=False)
    list_records = list(records)
    d = tuple(chain(*list_records))
    pos = struct.pack('>' + 'ffff' * len(dd), *d)
    if name is not None:
        with open(path + name, 'w+b') as f:
            f.write(pos)
    return pos


def hdf5_to_epos(data, path=None, name=None):
    """
    Loads an APT a pandas dataframe as .epos file .

    Columns:
        x: Reconstructed x position
        y: Reconstructed y position
        z: Reconstructed z position
        Da: Mass/charge ratio of ion
        ns: Ion Time Of Flight
        DC_kV: Potential
        pulse_kV: Size of voltage pulse (voltage pulsing mode only)
        det_x: Detector x position
        det_y: Detector y position
        pslep: Pulses since last event pulse (i.e. ionisation rate)
        ipp: Ions per pulse (multihits)

     [x,y,z,Da,ns,DC_kV,pulse_kV,det_x,det_y,pslep,ipp].
        pslep = pulses since last event pulse
        ipp = ions per pulse

    When more than one ion is recorded for a given pulse, only the
    first event will have an entry in the "Pulses since last evenT
    pulse" column. Each subsequent event for that pulse will have
    an entry of zero because no additional pulser firings occurred
    before that event was recorded. Likewise, the "Ions Per Pulse"
    column will contain the total number of recorded ion events for
    a given pulse. This is normally one, but for a sequence of records
    a pulse with multiply recorded ions, the first ion record will
    have the total number of ions measured in that pulse, while the
    remaining records for that pulse will have 0 for the Ions Per
    Pulse value.
        ~ Appendix A of 'Atom Probe tomography: A Users Guide',
          notes on ePOS format.
    """
    dd = data[
        ['x (nm)', 'y (nm)', 'z (nm)', 'mc (Da)', 't (ns)', 'high_voltage (V)', 'pulse (V)', 'x_det (cm)', 'y_det (cm)',
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