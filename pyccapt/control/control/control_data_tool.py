import h5py
import numpy as np


def rename_subcategory(hdf5_file_path, old_name, new_name):
    """
        rename subcategory

        Args:
            hdf5_file_path: path to the hdf5 file
            old_name: old name of the subcategory
            new_name: new name of the subcategory

        Returns:
            None
    """

    with h5py.File(hdf5_file_path, 'r+') as file:
        # data_x = file['dld/x']
        # del file[new_name]
        # file.create_dataset(new_name, data=np.zeros(len(data_x)), dtype=np.int64)
        if old_name in file:
            file[new_name] = file[old_name]
            del file[old_name]
            print(f"Subcategory '{old_name}' renamed to '{new_name}'")
        else:
            print(f"Subcategory '{old_name}' not found in the HDF5 file.")


def correct_surface_concept_old_data(hdf5_file_path):
    """
        correct surface concept old data

        Args:
            hdf5_file_path: path to the hdf5 file

        Returns:
            None
    """
    # surface concept tdc specific binning and factors
    TOFFACTOR = 27.432 / (1000.0 * 4.0)  # 27.432 ps/bin, tof in ns, data is TDC time sum
    DETBINS = 4900.0
    BINNINGFAC = 2.0
    XYFACTOR = 80.0 / DETBINS * BINNINGFAC  # XXX mm/bin
    XYBINSHIFT = DETBINS / BINNINGFAC / 2.0  # to center detector

    with h5py.File(hdf5_file_path, 'r+') as file:
        data_x = file['dld/x']
        data_y = file['dld/y']
        data_t = file['dld/t']

        data_x = np.array(data_x)
        data_y = np.array(data_y)
        data_t = np.array(data_t)

        modified_t = (data_t.astype(np.float64) * TOFFACTOR)
        del file['dld/t']
        file.create_dataset('dld/t', data=modified_t, dtype=np.float64)
        modified_x = ((data_x.astype(np.float64) - XYBINSHIFT) * XYFACTOR) / 10.0
        del file['dld/x']
        file.create_dataset('dld/x', data=modified_x, dtype=np.float64)
        modified_y = ((data_y.astype(np.float64) - XYBINSHIFT) * XYFACTOR) / 10.0
        del file['dld/y']
        file.create_dataset('dld/y', data=modified_y, dtype=np.float64)


def copy_npy_to_hdf_surface_concept(path, hdf5_file_name):
    """
        copy npy data to hdf5 file for surface concept TDC

        Args:
            path: path to the npy files
            hdf5_file_name: name of the hdf5 file

        Returns:
            None
    """
    TOFFACTOR = 27.432 / (1000 * 4)  # 27.432 ps/bin, tof in ns, data is TDC time sum
    DETBINS = 4900
    BINNINGFAC = 2
    XYFACTOR = 80 / DETBINS * BINNINGFAC  # XXX mm/bin
    XYBINSHIFT = DETBINS / BINNINGFAC / 2  # to center detector

    hdf5_file_path = path + hdf5_file_name
    high_voltage = np.load(path + 'voltage_data.npy')
    pulse = np.load(path + 'pulse_data.npy')
    start_counter = np.load(path + 'start_counter.npy')
    t = np.load(path + 't_data.npy')
    x_det = np.load(path + 'x_data.npy')
    y_det = np.load(path + 'y_data.npy')

    channel = np.load(path + 'channel_data.npy')
    high_voltage_tdc = np.load(path + 'voltage_data_tdc.npy')
    pulse_tdc = np.load(path + 'pulse_data_tdc.npy')
    start_counter_tdc = np.load(path + 'tdc_start_counter.npy')
    time_data = np.load(path + 'time_data.npy')

    xx_tmp = (((x_det - XYBINSHIFT) * XYFACTOR) * 0.1)  # from mm to in cm by dividing by 10
    yy_tmp = (((y_det - XYBINSHIFT) * XYFACTOR) * 0.1)  # from mm to in cm by dividing by 10
    tt_tmp = (t * TOFFACTOR)  # in ns

    with h5py.File(hdf5_file_path, 'r+') as file:
        del file['dld/t']
        del file['dld/x']
        del file['dld/y']
        del file['dld/pulse']
        del file['dld/high_voltage']
        del file['dld/start_counter']
        file.create_dataset('dld/t', data=tt_tmp, dtype=np.float64)
        file.create_dataset('dld/x', data=xx_tmp, dtype=np.float64)
        file.create_dataset('dld/y', data=yy_tmp, dtype=np.float64)
        file.create_dataset('dld/pulse', data=pulse, dtype=np.float64)
        file.create_dataset('dld/high_voltage', data=high_voltage, dtype=np.float64)
        file.create_dataset('dld/start_counter', data=start_counter, dtype=np.uint64)

        del file['tdc/channel']
        del file['tdc/high_voltage']
        del file['tdc/pulse']
        del file['tdc/start_counter']
        del file['tdc/time_data']
        file.create_dataset('tdc/channel', data=channel, dtype=np.uint32)
        file.create_dataset('tdc/high_voltage', data=high_voltage_tdc, dtype=np.float64)
        file.create_dataset('tdc/pulse', data=pulse_tdc, dtype=np.float64)
        file.create_dataset('tdc/start_counter', data=start_counter_tdc, dtype=np.uint64)
        file.create_dataset('tdc/time_data', data=time_data, dtype=np.uint64)


if __name__ == '__main__':
    path = 'D:/pyccapt/pyccapt/data/1780_Mar-25-2024_13-15_Al_test_1/'
    name = '1780_Mar-25-2024_13-15_Al_test_1.h5'
    # copy_npy_to_hdf(path, name)

    # rename_subcategory(path + name, old_name='dld', new_name='dld_1')
    copy_npy_to_hdf_surface_concept(path, name)
    # rename_subcategory(path + name, old_name='dld/AbsoluteTimeStamp', new_name='dld/start_counter')
    # rename_subcategory(path + name, old_name='dld/pulse_voltage', new_name='dld/pulse')
    print('Done')
