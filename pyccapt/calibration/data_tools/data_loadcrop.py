from copy import copy

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import colors
from matplotlib.patches import Circle, Rectangle
from matplotlib.ticker import FormatStrFormatter
from matplotlib.widgets import RectangleSelector, EllipseSelector

from pyccapt.calibration.calibration_tools import logging_library
from pyccapt.calibration.data_tools import data_tools
from pyccapt.calibration.data_tools import selectors_data


def fetch_dataset_from_dld_grp(filename: str, tdc: str) -> pd.DataFrame:
    """
    Fetches dataset from HDF5 file.

    Args:
        filename: Path to the HDF5 file.
        tdc: Model of TDC.

    Returns:
        DataFrame: Contains relevant information from the dld group.
    """
    logger = logging_library.logger_creator('data_loadcrop')
    try:
        hdf5Data = data_tools.read_hdf5(filename, tdc)
        if hdf5Data is None:
            raise FileNotFoundError
        dld_highVoltage = hdf5Data['dld/high_voltage'].to_numpy()
        dld_pulse = hdf5Data['dld/pulse'].to_numpy()
        dld_startCounter = hdf5Data['dld/start_counter'].to_numpy()
        dld_t = hdf5Data['dld/t'].to_numpy()
        dld_x = hdf5Data['dld/x'].to_numpy()
        dld_y = hdf5Data['dld/y'].to_numpy()
        dldGroupStorage = np.concatenate((dld_highVoltage, dld_pulse, dld_startCounter, dld_t, dld_x, dld_y), axis=1)
        dld_group_storage = create_pandas_dataframe(dldGroupStorage)
        return dld_group_storage
    except KeyError as error:
        logger.info(error)
        logger.critical("[*] Keys missing in the dataset")
    except FileNotFoundError as error:
        logger.info(error)
        logger.critical("[*] HDF5 file not found")


def concatenate_dataframes_of_dld_grp(dataframeList: list) -> pd.DataFrame:
    """
    Concatenates dataframes into a single dataframe.

    Args:
        dataframeList: List of different information from dld group.

    Returns:
        DataFrame: Single concatenated dataframe containing all relevant information.
    """
    dld_masterDataframe = pd.concat(dataframeList, axis=1)
    return dld_masterDataframe


def plot_crop_experiment_history(dldGroupStorage: pd.DataFrame, variables, max_tof, frac, figure_size=(7, 3),
                                 draw_rect=False, data_crop=True, pulse=False, pulse_mode='voltage', save=True):
    """
    Plots the experiment history.

    Args:
        dldGroupStorage: DataFrame containing info about the dld group.
        max_tof: The maximum tof to be plotted.
        frac: Fraction of the data to be plotted.
        figure_size: The size of the figure.
        data_crop: Flag to control if only the plot should be shown or cropping functionality should be enabled.
        draw_rect: Flag to draw  a rectangle over the slected area.
        pulse: Flag to choose whether to plot pulse.
        pulse_mode: Flag to choose whether to plot pulse voltage or pulse.
        save: Flag to choose whether to save the plot or not.

    Returns:
        None.
    """
    # dldGroupStorage = dldGroupStorage.sample(frac=frac, random_state=42)
    # dldGroupStorage.reset_index(inplace=True, drop=True)
    fig1, ax1 = plt.subplots(figsize=figure_size, constrained_layout=True)

    # Plot tof and high voltage
    yaxis = dldGroupStorage['t (ns)'].to_numpy()
    high_voltage = dldGroupStorage['high_voltage (V)'].to_numpy()
    if max_tof > 0:
        high_voltage = high_voltage[yaxis < max_tof]
        yaxis = yaxis[yaxis < max_tof]

    high_voltage = high_voltage / 1000  # change to kV
    xaxis = np.arange(len(yaxis))

    heatmap, xedges, yedges = np.histogram2d(xaxis, yaxis, bins=(1200, 800))
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

    # Set x-axis label
    ax1.set_xlabel("Hit sequence Number", fontsize=10)
    # Set y-axis label
    ax1.set_ylabel("Time of Flight [ns]", fontsize=10)
    img = plt.imshow(heatmap.T, extent=extent, origin='lower', aspect="auto")
    cmap = copy(plt.cm.plasma)
    cmap.set_bad(cmap(0))
    pcm = ax1.pcolormesh(xedges, yedges, heatmap.T, cmap=cmap, norm=colors.LogNorm(), rasterized=True)
    fig1.colorbar(pcm, ax=ax1, pad=0)

    # Make the x-axis ticks formatted to 0 decimal places
    ax1.xaxis.set_major_formatter(FormatStrFormatter('%0.0f'))

    # Plot high voltage curve
    ax2 = ax1.twinx()
    xaxis2 = np.arange(len(high_voltage))
    ax2.plot(xaxis2, high_voltage, color='dodgerblue', linewidth=2)
    ax2.set_ylabel("High Voltage [kV]", color="dodgerblue", fontsize=10)

    if data_crop:
        if not draw_rect:
            rectangle_box_selector(ax2, variables)
            plt.connect('key_press_event', selectors_data.toggle_selector(variables))
        elif draw_rect:
            left, bottom, width, height = (
                variables.selected_x1, 0, variables.selected_x2 - variables.selected_x1, np.max(yaxis))
            rect = Rectangle((left, bottom), width, height, fill=True, alpha=0.3, color="r", linewidth=2)
            ax1.add_patch(rect)

    if pulse:
        fig1.subplots_adjust(right=0.75)
        ax3 = ax1.twinx()
        ax3.plot(xaxis, dldGroupStorage['pulse'].to_numpy(), color='limegreen', linewidth=2)
        ax3.spines.right.set_position(("axes", 1.15))
        if pulse_mode == 'laser':
            ax3.set_ylabel("Laser Intensity (${pJ}/{\mu m^2}$)", color="limegreen", fontsize=10)
        elif pulse_mode == 'voltage':
            ax3.set_ylabel("Pulse (V)", color="limegreen", fontsize=10)

    if save:
        plt.savefig("%s.png" % (variables.result_path + '//ex_hist_'), format="png", dpi=600)
        plt.savefig("%s.svg" % (variables.result_path + '//ex_hist_'), format="svg", dpi=600)

    plt.show()


def plot_crop_FDM(data_crop, variables, bins=(256, 256), figure_size=(6, 6), circle=False,
                  save_name=False, only_plot=False):
    """
    Plot and crop the FDM with the option to select a region of interest.

    Args:
        data_crop: Cropped dataset (type: list)
        bins: Number of bins for the histogram
        figure_size: Size of the plot
        circle: Flag to enable circular region of interest selection
        save_name: Flag to choose whether to save the plot or not
        only_plot: Flag to control whether only the plot is shown or cropping functionality is enabled

    Returns:
        None
    """
    fig1, ax1 = plt.subplots(figsize=figure_size, constrained_layout=True)

    # Plot and crop FDM
    x = data_crop['x_det (cm)'].to_numpy()
    y = data_crop['y_det (cm)'].to_numpy()

    FDM, xedges, yedges = np.histogram2d(x, y, bins=bins)

    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    ax1.set_xlabel(r"$X_{det} (cm)$", fontsize=10)
    ax1.set_ylabel(r"$Y_{det} (cm)$", fontsize=10)

    cmap = copy(plt.cm.plasma)
    cmap.set_bad(cmap(0))
    pcm = ax1.pcolormesh(xedges, yedges, FDM.T, cmap=cmap, norm=colors.LogNorm(), rasterized=True)
    fig1.colorbar(pcm, ax=ax1, pad=0)

    if not only_plot:
        if not circle:
            rectangle_box_selector(ax1)
        else:
            print('x:', variables.selected_x_fdm, 'y:', variables.selected_y_fdm, 'roi:', variables.roi_fdm)
            circ = Circle((variables.selected_x_fdm, variables.selected_y_fdm), variables.roi_fdm, fill=True,
                          alpha=0.3, color='green', linewidth=1)
            ax1.add_patch(circ)
    if save_name:
        plt.savefig("%s.png" % save_name, format="png", dpi=600)
        plt.savefig("%s.svg" % save_name, format="svg", dpi=600)
    plt.show()


def rectangle_box_selector(axisObject, variables):
    """
    Enable the creation of a rectangular box to select the region of interest.

    Args:
        axisObject: Object to create the rectangular box

    Returns:
        None
    """
    selectors_data.toggle_selector.RS = RectangleSelector(axisObject, selectors_data.line_select_callback(variables),
                                                          useblit=True,
                                                          button=[1, 3],
                                                          minspanx=1, minspany=1,
                                                          spancoords='pixels',
                                                          interactive=True)


def crop_dataset(dld_master_dataframe, variables):
    """
    Crop the dataset based on the selected region of interest.

    Args:
        dld_master_dataframe: Concatenated dataset

    Returns:
        data_crop: Cropped dataset
    """
    data_crop = dld_master_dataframe.loc[int(variables.selected_x1):int(variables.selected_x2), :]
    data_crop.reset_index(inplace=True, drop=True)
    return data_crop


def elliptical_shape_selector(axisObject, figureObject):
    """
    Enable the creation of an elliptical box to select the region of interest.

    Args:
        axisObject: Object to create the axis of the plot
        figureObject: Object to create the figure

    Returns:
        None
    """
    selectors_data.toggle_selector.ES = EllipseSelector(axisObject, selectors_data.onselect, useblit=True,
                                                        button=[1, 3],
                                                        minspanx=1, minspany=1,
                                                        spancoords='pixels',
                                                        interactive=True)
    figureObject.canvas.mpl_connect('key_press_event', selectors_data.toggle_selector)


def crop_data_after_selection(data_crop):
    """
    Crop the dataset after the region of interest has been selected.

    Args:
        data_crop: Original dataset to be cropped

    Returns:
        data_crop: Cropped dataset
    """
    x = data_crop['x_det (cm)'].to_numpy()
    y = data_crop['y_det (cm)'].to_numpy()
    detector_dist = np.sqrt((x - variables.selected_x_fdm) ** 2 + (y - variables.selected_y_fdm) ** 2)
    mask_fdm = (detector_dist > variables.roi_fdm)
    data_crop.drop(np.where(mask_fdm)[0], inplace=True)
    data_crop.reset_index(inplace=True, drop=True)
    return data_crop


def create_pandas_dataframe(data_crop):
    """
    Create a pandas dataframe from the cropped data.

    Args:
        data_crop: Cropped dataset

    Returns:
        hdf_dataframe: Dataframe to be inserted in the HDF file
    """
    hdf_dataframe = pd.DataFrame(data=data_crop,
                                 columns=['high_voltage (V)', 'pulse', 'start_counter', 't (ns)',
                                          'x_det (cm)', 'y_det (cm)'])

    hdf_dataframe['start_counter'] = hdf_dataframe['start_counter'].astype('uint32')
    return hdf_dataframe