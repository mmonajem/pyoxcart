import numpy as np
import h5py


def copy_from_cobold_txt_to_hdf5():
    # Path of text file
    txt_path = 'output_DAn.txt'

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


if __name__ == "__main__":
    copy_from_cobold_txt_to_hdf5()