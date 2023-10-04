import struct

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


def ccapt_to_ato(file_path: str, data_frame: pd.DataFrame, mode: str):
    """
    Convert a pyccapt data frame to an .ato binary format file.

    Args:
        file_path: Path to save the .ato file
        data_frame: Pandas DataFrame containing pyccapt data
        mode: Type of mode (oxcart/ato)

    Returns:
        None
    """
    with open(file_path, 'wb') as f:
        num_atoms = len(data_frame)

        # Write zero, version, and num_atoms
        f.write(struct.pack('i', 0))
        f.write(struct.pack('i', 6))  # Version 6
        f.write(struct.pack('i', num_atoms))

        for i in range(num_atoms):
            atom_id = data_frame['atom_id'].iloc[i]
            pulse_pi = data_frame['pulse_pi'].iloc[i]
            x = int(data_frame['x (nm)'].iloc[i])
            y = int(data_frame['y (nm)'].iloc[i])
            z = int(data_frame['z (nm)'].iloc[i] * 10)
            mc = data_frame['mc (Da)'].iloc[i]
            tof = int(data_frame['tof (ns)'].iloc[i] / 1000)
            x_det = int(data_frame['x_det (mm)'].iloc[i] * 100)
            y_det = int(data_frame['y_det (mm)'].iloc[i] * 100)
            dc_voltage = int(data_frame['dc_voltage (V)'].iloc[i] * 2)
            mcp_amp = int(data_frame['mcp_amp'].iloc[i])
            num_cluster = data_frame['num_cluster'].iloc[i]
            cluster_id = data_frame['cluster_id'].iloc[i]

            # Write atom data
            f.write(struct.pack('I', atom_id))
            f.write(struct.pack('i', pulse_pi))
            f.write(struct.pack('h', x))
            f.write(struct.pack('h', y))
            f.write(struct.pack('f', z / 10.0))
            f.write(struct.pack('f', mc))
            f.write(struct.pack('f', tof))
            f.write(struct.pack('h', x_det))
            f.write(struct.pack('h', y_det))
            f.write(struct.pack('H', dc_voltage))
            f.write(struct.pack('H', mcp_amp))
            f.write(struct.pack('B', num_cluster))

            if num_cluster > 0:
                f.write(struct.pack('H' * num_cluster, *cluster_id))

        if mode == 'pyccapt':
            # Append additional data for PyCCAPT mode
            additional_data = np.zeros(num_atoms)
            f.write(struct.pack('d' * num_atoms, *additional_data))
