import os

import h5py
import numpy as np
import pandas as pd
import scipy.io

from pyccapt.calibration.calibration_tools import share_variables
# Local module and scripts
from pyccapt.calibration.data_tools import ato_tools
from pyccapt.calibration.data_tools import data_loadcrop
from pyccapt.calibration.data_tools import data_tools
from pyccapt.calibration.leap_tools import ccapt_tools
from pyccapt.calibration.mc import mc_tools, tof_tools


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


def save_data(data, variables, hdf=True, epos=False, pos=False, ato_6v=False, csv=False):
    """
    save data in different formats

    Args:
        data (pandas.DataFrame): DataFrame containing the data.
        vsriables (class): class containing the variables.
        hdf (bool): save data as hdf5 file.
        epos (bool): save data as epos file.
        pos (bool): save data as pos file.
        ato_6v (bool): save data as ato file.
        csv (bool): save data as csv file.

    Returns:
        None. The DataFrame is modified in-place.

    """
    if hdf:
        # save the dataset to hdf5 file
        hierarchyName = 'df'
        store_df_to_hdf(data, hierarchyName, variables.result_data_path + '//' + variables.result_data_name + '.h5')
    if epos:
        # save data as epos file
        ccapt_tools.ccapt_to_epos(data, path=variables.result_path,
                                  name=variables.result_data_name + '.epos')
    if pos:
        # save data in pos format
        ccapt_tools.ccapt_to_pos(data, path=variables.result_path, name=variables.result_data_name + '.pos')
    if ato_6v:
        # save data as ato file in  ersion 6
        ato_tools.ccapt_to_ato(data, path=variables.result_path, name=variables.result_data_name + '.ato')
    if csv:
        # save data in csv format
        store_df_to_csv(data, variables.result_path + variables.result_data_name + '.csv')


def load_data(dataset_path, tdc, mode='processed'):
    """
    save data in different formats

    Args:
        dataset_path (string): path to the dataset.
        tdc (string): type of the dataset.

    Returns:
        data (pandas.DataFrame): DataFrame containing the data.

    """
    if tdc == 'leap_pos' or tdc == 'leap_epos':
        if tdc == 'leap_epos':
            data = ccapt_tools.epos_to_ccapt(dataset_path)
        else:
            print('The file has to be epos. With pos information this tutorial cannot be run')
            data = ccapt_tools.pos_to_ccapt(dataset_path)
    elif tdc == 'ato_v6':
        data = ato_tools.ato_to_ccapt(dataset_path, moed='pyccapt')
    elif (tdc == 'surface_concept' or tdc == 'roentdec') and mode == 'raw':
        data = data_loadcrop.fetch_dataset_from_dld_grp(dataset_path, tdc)
    elif (tdc == 'surface_concept' or tdc == 'roentdec') and mode == 'processed':
        data = data_tools.read_hdf5_through_pandas(dataset_path)
    return data


def extract_data(dataset_path, flightPathLength_d, t0_d, max_mc, tdc, pulse_mode, mode='processed'):
    """
    exctract data from the dataset

    Args:
        dataset_path (string): path to the dataset.
        flightPathLength_d (float): flight path length in m.
        t0_d (float): time of flight offset in ns.
        max_mc (float): maximum time of flight in ns.
        tdc (string): type of the dataset.
        pulse_mode (string): pulse mode of the dataset.
        mode (string): mode of the dataset.
    Returns:
        data (pandas.DataFrame): DataFrame containing the data.
        variables (class): class containing the variables.
    """
    # Create data farame out of hdf5 file dataset
    data = data_tools.load_data(dataset_path, tdc, mode='processed')
    # exctract needed data from Pandas data frame as an numpy array

    # create an instance of the Variables opject
    variables = share_variables.Variables()
    variables.pulse_mode = pulse_mode
    dataset_main_path = os.path.dirname(dataset_path)
    dataset_name_with_extention = os.path.basename(dataset_path)
    variables.dataset_name = os.path.splitext(dataset_name_with_extention)[0]
    variables.result_data_path = dataset_main_path + '/' + variables.dataset_name
    variables.result_data_name = 'tof_calibration_' + variables.dataset_name
    variables.result_path = dataset_main_path + '/' + '/tof_calibration/'

    if not os.path.isdir(variables.result_path):
        os.makedirs(variables.result_path, mode=0o777, exist_ok=True)

    # Create data farame out of hdf5 file dataset
    data = data_tools.load_data(dataset_path, tdc, mode='processed')

    variables.dld_high_voltage = data['high_voltage (V)'].to_numpy()
    variables.dld_pulse = data['pulse'].to_numpy()
    variables.dld_t = data['t (ns)'].to_numpy()
    variables.dld_x_det = data['x_det (cm)'].to_numpy()
    variables.dld_y_det = data['y_det (cm)'].to_numpy()
    variables.mc = mc_tools.tof2mc(variables.dld_t, t0_d, variables.dld_high_voltage, variables.dld_x_det,
                                   variables.dld_y_det, flightPathLength_d, V_pulse=variables.dld_pulse,
                                   mode='dc_voltage')

    # Calculate the maximum possible time of flight (TOF)
    variables.max_tof = int(tof_tools.mc2tof(max_mc, 1000, 0, 0, flightPathLength_d))
    variables.dld_t_calib = data['t (ns)'].to_numpy()
    variables.dld_t_calib_backup = data['t (ns)'].to_numpy()
    # ion_distance = np.sqrt(flightPathLength_d**2 + (variables.dld_x_det*10)**2 + (variables.dld_y_det*10)**2)
    # ion_distance = flightPathLength_d / ion_distance
    # variables.dld_t = variables.dld_t * ion_distance
    return data, variables
