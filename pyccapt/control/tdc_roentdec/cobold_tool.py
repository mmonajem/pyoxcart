import h5py
import numpy as np


def copy_xy_from_cobold_txt_to_hdf5(txt_path):
    # Read data from text file
    with open(txt_path, 'r') as f:
        data = np.loadtxt(f)

    xx = data[:, 6] / 10
    yy = data[:, 7] / 10
    with h5py.File('data_124_Apr-18-2023_18-46_LFIM1.h5', 'r+') as file:
        # Access the dataset you want to modify
        del file['dld/x']
        del file['dld/y']

        file.create_dataset('dld/x', data=xx)
        file.create_dataset('dld/y', data=yy)
        file.close()

    print('finish')


def cobold_txt_to_hdf5(txt_path):
    # (1) Event number (2) Pulse height (3) Absolute time  (4) Precise time (5)
    # number of ions (6) number of signals (7) x-pos (8) y-pos (9) time of flight
    # (10) used algorithm (11) x-pos2 (12) y-pos2 (13) TOF2 and so on
    #
    # (3) +(4) give the absolute time with high precision.

    # Read data from text file
    with open(txt_path, 'r') as f:
        data = np.loadtxt(f)

    xx = data[:, 6] / 10
    yy = data[:, 7] / 10
    tof = data[:, 8]

    with h5py.File('data_TiO2.h5', "w") as f:
        f.create_dataset("dld/x", data=xx, dtype='f')
        f.create_dataset("dld/y", data=yy, dtype='f')
        f.create_dataset("dld/t", data=tof, dtype='f')
        f.create_dataset("dld/start_counter", data=np.zeros(len(xx)), dtype='i')
        f.create_dataset("dld/high_voltage", data=np.full(len(xx), 5300), dtype='f')
        f.create_dataset("dld/pulse", data=np.zeros(len(xx)), dtype='f')

    print('finish')


if __name__ == "__main__":
    # # Path of text file
    # txt_path = 'output_DAn.txt'
    # copy_xy_from_cobold_txt_to_hdf5(txt_path)

    txt_path = 'LFIM14_DAn.txt'
    cobold_txt_to_hdf5(txt_path)
