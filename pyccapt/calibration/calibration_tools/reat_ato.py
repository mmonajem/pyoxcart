import re
import struct

import numpy as np
import pandas as pd

def ato_to_hdf(file, mode):
    with open(file, 'rb') as f:
        data = f.read()
        # The first thing in the file is a 0
        zero = struct.unpack('i', data[:4])
        print(zero)
        # The second thing is the version of the file
        version = struct.unpack('i', data[4:8])
        print(version)
        # The Third thing is the version of the file
        num_atoms = struct.unpack('i', data[8:12])
        print(num_atoms)
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
            # for each ions we have cluster ids base on the number of cluster in num_cluster
            if num_cluster_tmp > 0:
                cluster_id.append(struct.unpack('H' * num_cluster_tmp, data[bias+33:bias+33+num_cluster_tmp*2])[0])
            # we have 33 + num_cluster_tmp * 2 bytes for each ion
            bias = 12 + (35 * (i+1))

        # convert values to right unit
        # unpack data
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
                                'dc_voltage (v)': dc_voltage,
                                'mcp_amp': mcp_amp,
                                'num_cluster': num_cluster,
                                'cluster_id': cluster_id,})
        elif mode == 'oxcart':
            data_f = pd.DataFrame({'high_voltage (V)': dc_voltage,
                                   'pulse (V)': np.zeros(len(dc_voltage)),
                                   'start counter': np.zeros(len(dc_voltage)),
                                   't (ns)': tof,
                                   'mc (Da)': mc,
                                   'x_det (mm)': x_det,
                                   'y_det (mm)': y_det,
                                   'pulse_pi': pulse_pi,
                                   'ion_pp': np.zeros(len(dc_voltage)),})
    return data_f


if __name__ == "__main__":
    # save data as csv
    data_f = ato_to_hdf(file='Bicrys_version5_Al_1_12_22_francois_V6.ato', mode='oxcart')
    data_f.to_hdf('Bicrys_version5_Al_1_12_22_francois_V6_our_structure.h5', 'df', mode='w')
    # save data in csv format
    # data_f.to_csv('Bicrys_version5_Al_1_12_22_francois_V6.csv', encoding='utf-8', index=False)