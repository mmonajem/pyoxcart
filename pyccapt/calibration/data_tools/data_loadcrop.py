from copy import copy

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import colors
from matplotlib.patches import Circle, Rectangle
from matplotlib.widgets import RectangleSelector

from pyccapt.calibration.calibration_tools import logging_library
from pyccapt.calibration.data_tools import data_tools
from pyccapt.calibration.data_tools import selectors_data


def fetch_dataset_from_dld_grp(filename: str) -> pd.DataFrame:
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
        hdf5Data = data_tools.read_hdf5(filename)
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


def plot_crop_experiment_history(data: pd.DataFrame, variables, max_tof, frac=1.0, bins=(1200, 800), figure_size=(7, 3),
                                 draw_rect=False, data_crop=True, pulse=False, pulse_mode='voltage', save=True,
                                 figname=''):
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
        figname: Name of the figure to be saved.

    Returns:
        None.
    """
    if max_tof > 0:
        mask_1 = (data['t (ns)'].to_numpy() > max_tof)
        data.drop(np.where(mask_1)[0], inplace=True)
        data.reset_index(inplace=True, drop=True)
    if frac < 1:
        # set axis limits based on fraction of data
        dldGroupStorage = data.sample(frac=frac, random_state=42)
        dldGroupStorage.sort_index(inplace=True)
    else:
        dldGroupStorage = data

    fig1, ax1 = plt.subplots(figsize=figure_size, constrained_layout=True)

    # extract tof and high voltage from the data frame
    tof = dldGroupStorage['t (ns)'].to_numpy()
    high_voltage = data['high_voltage (V)'].to_numpy()
    high_voltage = high_voltage / 1000  # change to kV

    xaxis = np.arange(len(tof))

    heatmap, xedges, yedges = np.histogram2d(xaxis, tof, bins=bins)
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

    # Plot high voltage curve
    ax2 = ax1.twinx()
    xaxis2 = np.arange(len(high_voltage))
    ax2.plot(xaxis2, high_voltage, color='dodgerblue', linewidth=2)
    ax2.set_ylabel("High Voltage [kV]", color="dodgerblue", fontsize=10)

    if frac < 1:
        # extract tof
        tof_lim = data['t (ns)'].to_numpy()
        high_voltage_lim = data['high_voltage (V)'].to_numpy()
        high_voltage_lim = high_voltage_lim / 1000  # change to kV
        # set axis limits based on entire data
        ax1.set_xlim([0, len(tof)])
        ax1.set_ylim([min(tof_lim), max(tof_lim)])
        ax2.set_xlim([0, len(high_voltage_lim)])
        ax2.set_ylim([min(high_voltage_lim), max(high_voltage_lim)])

    if data_crop:
        rectangle_box_selector(ax2, variables)
        plt.connect('key_press_event', selectors_data.toggle_selector(variables))
    if draw_rect:
        left, bottom, width, height = (
            variables.selected_x1, 0, variables.selected_x2 - variables.selected_x1, np.max(tof))
        rect = Rectangle((left, bottom), width, height, fill=True, alpha=0.3, color="r", linewidth=5)
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
        plt.savefig("%s.png" % (variables.result_path + figname), format="png", dpi=600)
        plt.savefig("%s.svg" % (variables.result_path + figname), format="svg", dpi=600)

    plt.show()


def plot_crop_fdm(data, variables, bins=(256, 256), frac=1.0, data_crop=False, figure_size=(5, 4), draw_circle=False,
                  save=True, figname=''):
    """
    Plot and crop the FDM with the option to select a region of interest.

    Args:
        data: Cropped dataset (type: list)
        bins: Number of bins for the histogram
        figure_size: Size of the plot
        draw_circle: Flag to enable circular region of interest selection
        save: Flag to choose whether to save the plot or not
        data_crop: Flag to control whether only the plot is shown or cropping functionality is enabled
        figname: Name of the figure to be saved

    Returns:
        None
    """
    if frac < 1:
        # set axis limits based on fraction of data
        dldGroupStorage = data.sample(frac=frac, random_state=42)
        dldGroupStorage.sort_index(inplace=True)
    else:
        dldGroupStorage = data

    fig1, ax1 = plt.subplots(figsize=figure_size, constrained_layout=True)

    # Plot and crop FDM
    x = dldGroupStorage['x_det (cm)'].to_numpy()
    y = dldGroupStorage['y_det (cm)'].to_numpy()

    FDM, xedges, yedges = np.histogram2d(x, y, bins=bins)

    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    ax1.set_xlabel(r"$X_{det} (cm)$", fontsize=10)
    ax1.set_ylabel(r"$Y_{det} (cm)$", fontsize=10)

    cmap = copy(plt.cm.plasma)
    cmap.set_bad(cmap(0))
    pcm = ax1.pcolormesh(xedges, yedges, FDM.T, cmap=cmap, norm=colors.LogNorm(), rasterized=True)
    fig1.colorbar(pcm, ax=ax1, pad=0)

    if frac < 1:
        # extract tof
        x_lim = dldGroupStorage['x_det (cm)'].to_numpy()
        y_lim = dldGroupStorage['y_det (cm)'].to_numpy()

        ax1.set_xlim([min(x_lim), max(x_lim)])
        ax1.set_ylim([min(y_lim), max(y_lim)])

    if data_crop:
        elliptical_shape_selector(ax1, fig1, variables)
    if draw_circle:
        print('x:', variables.selected_x_fdm, 'y:', variables.selected_y_fdm, 'roi:', variables.roi_fdm)
        circ = Circle((variables.selected_x_fdm, variables.selected_y_fdm), variables.roi_fdm, fill=True,
                      alpha=0.3, color='green', linewidth=5)
        ax1.add_patch(circ)
    if save:
        plt.savefig("%s.png" % (variables.result_path + figname), format="png", dpi=600)
        plt.savefig("%s.svg" % (variables.result_path + figname), format="svg", dpi=600)
    plt.show()


def rectangle_box_selector(axisObject, variables):
    """
    Enable the creation of a rectangular box to select the region of interest.

    Args:
        axisObject: Object to create the rectangular box

    Returns:
        None
    """
    selectors_data.toggle_selector.RS = RectangleSelector(axisObject,
                                                          lambda eclick, erelease: selectors_data.line_select_callback(
                                                              eclick, erelease, variables),
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
        variables: Variables object

    Returns:
        data_crop: Cropped dataset
    """
    data_crop = dld_master_dataframe.loc[int(variables.selected_x1):int(variables.selected_x2), :]
    data_crop.reset_index(inplace=True, drop=True)
    return data_crop


def elliptical_shape_selector(axisObject, figureObject, variables):
    """
    Enable the creation of an elliptical box to select the region of interest.

    Args:
        axisObject: Object to create the axis of the plot
        figureObject: Object to create the figure
        variables: Variables object

    Returns:
        None
    """
    # selectors_data.toggle_selector.ES = EllipseSelector(axisObject,
    #                                                     lambda eclick, erelease: selectors_data.onselect(eclick,
    #                                                                                                      erelease,
    #                                                                                                      variables),
    #                                                     useblit=True,
    #                                                     button=[1, 3],
    #                                                     minspanx=1, minspany=1,
    #                                                     spancoords='pixels',
    #                                                     interactive=True)
    selectors_data.toggle_selector.ES = selectors_data.CircleSelector(axisObject,
                                                                      lambda eclick, erelease: selectors_data.onselect(
                                                                          eclick,
                                                                          erelease,
                                                                          variables),
                                                                      useblit=True,
                                                                      button=[1, 3],
                                                                      minspanx=1, minspany=1,
                                                                      spancoords='pixels',
                                                                      interactive=True)
    figureObject.canvas.mpl_connect('key_press_event', selectors_data.toggle_selector)


def crop_data_after_selection(data_crop, variables):
    """
    Crop the dataset after the region of interest has been selected.

    Args:
        data_crop: Original dataset to be cropped
        variables: Variables object

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


def calculate_ppi_and_ipp(data):
    """
    Calculate pulses since the last event pulse and ions per pulse.

    Args:
        data (dict): A dictionary containing the 'start_counter' data.

    Returns:
        tuple: A tuple containing two numpy arrays: pulse_pi and ion_pp.

    Raises:
        IndexError: If the length of counter is less than 1.

    """

    counter = data['start_counter'].to_numpy()
    pulse_pi = np.zeros(len(counter))
    ion_pp = np.zeros(len(counter))

    pulse_to_previous_ion = 0
    multi_hit_count = 1
    previous_counter = counter[0]

    for i, current_counter in enumerate(counter):
        pulse_pi[i] = current_counter - previous_counter

        if current_counter == previous_counter:
            multi_hit_count += 1
        else:
            pulse_to_previous_ion = current_counter - previous_counter

            for j in range(multi_hit_count):
                ion_pp[i + j] = multi_hit_count
                pulse_pi[i + j] = pulse_to_previous_ion

            multi_hit_count = 1
            previous_counter = current_counter

    return pulse_pi, ion_pp
