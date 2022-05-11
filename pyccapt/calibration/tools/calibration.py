"""
This is the python version of data load and crop tutorial.
"""

import os
import matplotlib.pyplot as plt

from pyccapt.calibration.tools import data_loadcrop, variables
from pyccapt.calibration.module_dir import MODULE_DIR


def data_crop(filename, savename, dataset_name):
    dldGroupStorage = data_loadcrop.fetch_dataset_from_dld_grp(filename)
    dld_masterDataframe = data_loadcrop.concatenate_dataframes_of_dld_grp(dldGroupStorage)
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    data_loadcrop.plot_graph_for_dld_high_voltage(ax1, dldGroupStorage, save_name=variables.result_path + '//ex_hist_' + dataset_name)
    data_crop = data_loadcrop.crop_dataset(dld_masterDataframe)
    fig1, ax1 = plt.subplots(figsize=(8, 8))
    data_loadcrop.plot_crop_FDM(ax1, fig1, data_crop, save_name=variables.result_path + '//FDM_' + dataset_name)
    fig1, ax1 = plt.subplots(figsize=(8, 8))
    data_loadcrop.plot_FDM_after_selection(ax1, fig1, data_crop, save_name=variables.result_path + 'FDM_c' + dataset_name)
    data_crop_FDM = data_loadcrop.crop_data_after_selection(data_crop)
    fig1, ax1 = plt.subplots(figsize=(8, 8))
    data_loadcrop.plot_FDM(ax1, fig1, data_crop_FDM, save_name=variables.result_path + '//FDM_crop_' + dataset_name)
    data_loadcrop.save_croppped_data_to_hdf5(data_crop_FDM, dld_masterDataframe, savename)


if __name__ == "__main__":

    variables.path = os.path.join(os.path.split(os.path.split(MODULE_DIR)[0])[0], 'tests//data')
    variables.result_path = os.path.join(os.path.split(os.path.split(MODULE_DIR)[0])[0], 'results')
    if not os.path.isdir(variables.result_path):
        os.makedirs(variables.result_path, mode=0o777, exist_ok=True)
    # dataset name
    dataset_name = 'OLO_AL_6_data'
    filename = variables.path + '//' + dataset_name + '.h5'
    savename = variables.result_path + '//' + dataset_name + '.h5'

    data_crop(filename, savename, dataset_name)
