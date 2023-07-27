import struct
from itertools import chain

import numpy as np
import pandas as pd


def ato_to_ccapt(file_path: str, mode: str) -> pd.DataFrame:
    """
    Read data from an .ato file version 6 and convert it into a pandas DataFrame.

    Args:
        file_path: Path to the .ato file
        mode: Type of mode (oxcart/ato)

    Returns:
        Pandas DataFrame containing the converted data
    """
    with open(file_path, 'rb') as f:
        data = f.read()

        zero = struct.unpack('i', data[:4])
        version = struct.unpack('i', data[4:8])
        num_atoms = struct.unpack('i', data[8:12])

        atom_id = []
        pulse_pi = []
        x = []
        y = []
        z = []
        mc = []
        tof = []
        x_det = []
        y_det = []
        dc_voltage = []
        mcp_amp = []
        num_cluster = []
        cluster_id = []
        bias = 12

        for i in range(num_atoms[0]):
            atom_id.append(struct.unpack('I', data[bias:bias+4])[0])
            pulse_pi.append(struct.unpack('i', data[bias+4:bias+8])[0])
            x.append(struct.unpack('h', data[bias+8:bias+10])[0])
            y.append(struct.unpack('h', data[bias+10:bias+12])[0])
            z.append(struct.unpack('f', data[bias+12:bias+16])[0] * 0.1)
            mc.append(struct.unpack('f', data[bias+16:bias+20])[0])
            tof.append(struct.unpack('f', data[bias+20:bias+24])[0] * 1000)
            x_det.append(struct.unpack('h', data[bias+24:bias+26])[0] * 0.01)
            y_det.append(struct.unpack('h', data[bias+26:bias+28])[0] * 0.01)
            dc_voltage.append(struct.unpack('H', data[bias+28:bias+30])[0] * 0.5)
            mcp_amp.append(struct.unpack('H', data[bias+30:bias+32])[0])
            num_cluster_tmp = struct.unpack('B', data[bias+32:bias+33])[0]
            num_cluster.append(num_cluster_tmp)

            if num_cluster_tmp > 0:
                cluster_id.append(struct.unpack('H' * num_cluster_tmp, data[bias+33:bias+33+num_cluster_tmp*2])[0])

            bias = 12 + (35 * (i+1))

        if mode == 'ato':
            data_f = pd.DataFrame({'atom_id': atom_id,
                                   'pulse_pi': pulse_pi,
                                   'x (nm)': x,
                                   'y (nm)': y,
                                   'z (nm)': z,
                                   'mc (Da)': mc,
                                   'tof (ns)': tof,
                                   'x_det (mm)': x_det,
                                   'y_det (mm)': y_det,
                                   'dc_voltage (V)': dc_voltage,
                                   'mcp_amp': mcp_amp,
                                   'num_cluster': num_cluster,
                                   'cluster_id': cluster_id})
        elif mode == 'pyccapt':
            data_f = pd.DataFrame({
                'x (nm)': np.zeros(len(dc_voltage)),
                'y (nm)': np.zeros(len(dc_voltage)),
                'z (nm)': np.zeros(len(dc_voltage)),
                'mc_c (Da)': np.zeros(len(dc_voltage)),
                'mc (Da)': np.zeros(len(dc_voltage)),
                'high_voltage (V)': dc_voltage,
                'pulse': np.zeros(len(dc_voltage)),
                'start_counter': np.zeros(len(dc_voltage)),
                't_c (ns)': np.zeros(len(dc_voltage)),
                't (ns)': tof,
                'mc (Da)': mc,
                'x_det (mm)': x_det,
                'y_det (mm)': y_det,
                'pulse_pi': pulse_pi,
                'ion_pp': np.zeros(len(dc_voltage))})
    return data_f


def ccapt_to_ato(data, path=None, name=None):
    """
    Converts CCAPT data to ATO file format.
        Args:
        data (pd.DataFrame): Input data containing the columns:
            'x (nm)', 'y (nm)', 'z (nm)', 'mc_c (Da)', 't (ns)', 'high_voltage (V)', 'pulse (V)', 'x_det (cm)',
            'y_det (cm)', 'pulse_pi', 'ion_pp'.
        path (str): Optional path to save the ATO file. If not provided, the file will not be saved.
        name (str): Optional name for the ATO file. If not provided, the file will not be named.

    Returns:
        bytes: ATO file data.

    """
    # TODO: correct it for ato files
    dd = data[
        ['x (nm)', 'y (nm)', 'z (nm)', 'mc_c (Da)', 't (ns)', 'high_voltage (V)', 'pulse', 'x_det (cm)',
         'y_det (cm)',
         'pulse_pi', 'ion_pp']]

    dd = dd.astype(np.single)
    dd = dd.astype({'pulse_pi': np.uintc})
    dd = dd.astype({'ion_pp': np.uintc})

    records = dd.to_records(index=False)
    list_records = list(records)
    d = tuple(chain(*list_records))
    ato = struct.pack('>' + 'IihhfffhhHHb' * len(dd), *d)
    if name is not None:
        with open(path + name, 'w+b') as f:
            f.write(ato)

    return ato
