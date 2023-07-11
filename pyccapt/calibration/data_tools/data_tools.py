import h5py
import numpy as np
import pandas as pd
import scipy.io

# Local module and scripts
from pyccapt.calibration.data_tools import ato_tools
from pyccapt.calibration.leap_tools import ccapt_tools


def read_hdf5(filename: "type: string - Path to hdf5(.h5) file",
              tdc: "type: string - model of tdc") -> "type: dataframe":
    """
    This function differs from read_hdf5_through_pandas as it does not assume that 
    the contents of the HDF5 file as argument was created using pandas. It could have been
    created using other tools like h5py/MATLAB.
    """
    try:
        TOFFACTOR = 27.432 / (1000 * 4)  # 27.432 ps/bin, tof in ns, data is TDC time sum
        DETBINS = 4900
        BINNINGFAC = 2
        XYFACTOR = 78 / DETBINS * BINNINGFAC  # XXX mm/bin
        XYBINSHIFT = DETBINS / BINNINGFAC / 2  # to center detector
        dataframeStorage = {}
        groupDict = {}

        with h5py.File(filename, 'r') as hdf:
            groups = list(hdf.keys())

            for item in groups:
                groupDict[item] = list(hdf[item].keys())
            print(groupDict)
            for key, value in groupDict.items():
                for item in value:
                    dataset = pd.DataFrame(np.array(hdf['{}/{}'.format(key, item)]), columns=['values'])
                    if tdc == 'surface_concept':
                        if key == 'dld' and item == 't':
                            dataset = dataset * TOFFACTOR
                        elif key == 'dld' and item == 'x':
                            dataset = (dataset - XYBINSHIFT) * XYFACTOR * 0.1  # to convert them from mm to cm
                        elif key == 'dld' and item == 'y':
                            dataset = (dataset - XYBINSHIFT) * XYFACTOR * 0.1  # to convert them from mm to cm
                    else:
                        dataset = dataset
                    dataframeStorage["{}/{}".format(key, item)] = dataset

            return dataframeStorage
    except FileNotFoundError as error:
        print("[*] HDF5 File could not be found")

    except IndexError as error:
        print("[*] No Group keys could be found in HDF5 File")


def read_hdf5_through_pandas(filename: "type:string - Path to hdf5(.h5) file") -> "type: dataframe - Pandas Dataframe":
    """
    This function is different from read_hdf5 function. As it assumes, the content 
    of the HDF5 file passed as argument was created using the Pandas library.

        Attributes:
            filename: Path to the hdf5 file. (type: string)
        Return:
            hdf5_file_response:  content of hdf5 file (type: dataframe)       
    """
    try:
        hdf5_file_response = pd.read_hdf(filename, mode='r')
        return hdf5_file_response
    except FileNotFoundError as error:
        print("[*] HDF5 File could not be found")


def read_mat_files(filename: "type:string - Path to .mat file") -> " type: dict - Returns the content .mat file":
    """
        This function read data from .mat files.
        Attributes:
            filename: Path to the .mat file. (type: string)
        Return:
            hdf5_file_response:  content of hdf5 file (type: dict)  
    """
    try:
        hdf5_file_response = scipy.io.loadmat(filename)
        return hdf5_file_response
    except FileNotFoundError as error:
        print("[*] Mat File could not be found")


def convert_mat_to_df(hdf5_file_response: "type: dict - content of .mat file"):
    """
        This function converts converts contents read from the .mat file
        to pandas dataframe.
        Attributes:
            hdf5_file_response: contents of .mat file (type: dict)
        Returns:
            pd_dataframe: converted dataframes (type: pandas dataframe)
    """
    pd_dataframe = pd.DataFrame(hdf5_file_response['None'])
    key = 'dataframe/isotope'
    filename = 'isotopeTable.h5'
    store_df_to_hdf(filename, pd_dataframe, key)
    return pd_dataframe


def store_df_to_hdf(dataframe: "dataframe which is to be stored in h5 file",
                    key: "DirectoryStructure/columnName of content",
                    filename: "type: string - name of hdf5 file"):
    """
        This function stores dataframe to hdf5 file.

        Atrributes:
            filename: filename of hdf5 where dataframes needs to stored
            dataframe: dataframe that needs to be stored.
            key: Key that defines hierarchy of the hdf5
        Returns:
            Does not return anything
    """
    dataframe.to_hdf(filename, key, mode='w')


def store_df_to_csv(data, path):
    """
        This function stores dataframe to csv file.

        Atrributes:
            path: filename of hdf5 where dataframes needs to stored
            data: data that needs to be stored.
        Returns:
            Does not return anything
    """

    data.to_csv(path, encoding='utf-8', index=False, sep=';')


def remove_invalid_data(dld_group_storage, max_tof):
    """
    Removes the data with time-of-flight (TOF) values greater than max_tof or lower than 0.

    Args:
        dld_group_storage (pandas.DataFrame): DataFrame containing the DLD group storage data.
        max_tof (float): Maximum allowable TOF value.

    Returns:
        None. The DataFrame is modified in-place.

    """
    # Create a mask for data with TOF values greater than max_tof
    mask_1 = dld_group_storage['t (ns)'].to_numpy() > max_tof

    mask_2 = (dld_group_storage['t (ns)'].to_numpy() < 0)
    mask = np.logical_or(mask_1, mask_2)

    # Calculate the number of data points over max_tof
    num_over_max_tof = len(mask[mask])

    # Remove data points with TOF values greater than max_tof
    dld_group_storage.drop(np.where(mask)[0], inplace=True)

    # Reset the index of the DataFrame
    dld_group_storage.reset_index(inplace=True, drop=True)

    # Print the number of data points over max_tof
    print('The number of data over max_tof:', num_over_max_tof)

    return dld_group_storage


def save_data(data, variables, hdf=True, epos=False, pos=False, ato=False, csv=False):
    if hdf:
        # save the dataset to hdf5 file
        hierarchyName = 'df'
        store_df_to_hdf(data, hierarchyName, variables.result_path + '//' + variables.dataset_name + '_cropped' + '.h5')
    if epos:
        # save data as epos file
        epos = ccapt_tools.ccapt_to_epos(data, pulse_mode=variables.pulse_mode, path=variables.result_path,
                                         name=variables.dataset_name + '.epos')
    if pos:
        # save data in pos format
        pos = ccapt_tools.ccapt_to_pos(data, path=variables.result_path, name=variables.dataset_name + '.pos')
    if ato:
        # save data as ato file in  ersion 6
        ato_tools.ccapt_to_ato(data, path=variables.result_path, name=variables.dataset_name + '.ato')
    if csv:
        # save data in csv format
        store_df_to_csv(data, variables.result_path + variables.dataset_name + '.csv')
