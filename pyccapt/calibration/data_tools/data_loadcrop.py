"""
This is the main script of loading and cropping the dataset.
"""

from copy import copy

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import colors
from matplotlib.patches import Circle, Rectangle
from matplotlib.ticker import FormatStrFormatter
from matplotlib.widgets import RectangleSelector, EllipseSelector

from pyccapt.calibration.calibration_tools import logging_library
# Local module and scripts
from pyccapt.calibration.calibration_tools import variables
from pyccapt.calibration.data_tools import data_tools, selectors_data


def fetch_dataset_from_dld_grp(filename: "type: string - Path to hdf5(.h5) file", tdc: "type: string - model of tdc",
                               pulse_mode: "type: string - mode of pulse") -> "type: dataframes":
    """
        This function fetches dataset from HDF5 file. The HDF5 files
        contains data from the dld group. It fetches relevant
        information, assembles and return all the information
        in the form of dataframe

        Attributes:
            filename: Path to the HDF5 file (type: string)
            pulse_mode: Represents type of laser/voltage.(type: string)
        Returns:
            dldGroupStorage: dataframe containig all relevant information
                             from the dld group (type: pandas dataframe)
        
    """
    logger = logging_library.logger_creator('data_loadcrop')
    try:
        hdf5Data = data_tools.read_hdf5(filename, tdc)
        if hdf5Data is None:
            raise FileNotFoundError
        if tdc == 'surface_concept':
            dld_highVoltage = hdf5Data['dld/high_voltage'].to_numpy()
            if pulse_mode == 'laser':
                dld_pulse = hdf5Data['dld/laser_intensity'].to_numpy()
            elif pulse_mode == 'voltage':
                dld_pulse = hdf5Data['dld/pulse_voltage'].to_numpy()
            dld_startCounter = hdf5Data['dld/start_counter'].to_numpy()
            dld_t = hdf5Data['dld/t'].to_numpy()
            dld_x = hdf5Data['dld/x'].to_numpy()
            dld_y = hdf5Data['dld/y'].to_numpy()

            # if the recorded data in unequal in length we can crop it
            # print(dld_x.shape, dld_y.shape, dld_highVoltage.shape, dld_pulse.shape, dld_t.shape, dld_startCounter.shape)
            # # if len(dld_x) != len(dld_y) != len(dld_highVoltage) != len(dld_pulse) != len(dld_t):
            # mini = min(len(dld_x), len(dld_y), len(dld_highVoltage), len(dld_pulse), len(dld_t), len(dld_startCounter))
            # dld_x = dld_x[:mini]
            # dld_y = dld_y[:mini]
            # dld_highVoltage = dld_highVoltage[:mini]
            # dld_pulse = dld_pulse[:mini]
            # dld_t = dld_t[:mini]
            # dld_startCounter = dld_startCounter[:mini]

            # remove data that is location are out of the detector
            # mask_local = np.logical_and((np.abs(dld_x) <= det_diam/2), (np.abs(dld_y) <= det_diam/2))
            # mask_temporal = np.logical_and((dld_t > 0), (dld_t < max_tof))
            # mask = np.logical_and(mask_temporal, mask_local)
            # dld_highVoltage = dld_highVoltage[mask]
            # dld_pulse = dld_pulse[mask]
            # dld_startCounter = dld_startCounter[mask]
            # dld_t = dld_t[mask]
            # dld_x = dld_x[mask]
            # dld_y = dld_y[mask]

            # dld_highVoltage = np.expand_dims(dld_highVoltage, axis=1)
            # dld_pulse = np.expand_dims(dld_pulse, axis=1)
            # dld_startCounter = np.expand_dims(dld_startCounter, axis=1)
            # dld_t = np.expand_dims(dld_t, axis=1)
            # dld_x = np.expand_dims(dld_x, axis=1)
            # dld_y = np.expand_dims(dld_y, axis=1)

            dld_x = dld_x * 0.1 # to convert them from mm to cm
            dld_y = dld_y * 0.1 # to convert them from mm to cm



            dldGroupStorage = np.concatenate((dld_highVoltage, dld_pulse, dld_startCounter, dld_t, dld_x, dld_y),
                                             axis=1)

        elif tdc == 'roentdec':
            dld_highVoltage = hdf5Data['dld/high_voltage'].to_numpy()
            if pulse_mode == 'laser':
                dld_pulse = hdf5Data['dld/laser_intensity'].to_numpy()
            elif pulse_mode == 'voltage':
                dld_pulse = hdf5Data['dld/pulse_voltage'].to_numpy()
            dld_AbsoluteTimeStamp = hdf5Data['dld/AbsoluteTimeStamp'].to_numpy().astype(np.uintc)
            dld_t = hdf5Data['dld/t'].to_numpy()
            dld_x = hdf5Data['dld/x'].to_numpy()
            dld_y = hdf5Data['dld/y'].to_numpy()
            # remove data that is location are out of the detector
            # TODO
            dld_AbsoluteTimeStamp = np.copy(dld_t)

            # mask_local = np.logical_and((np.abs(dld_x) <= det_diam/2), (np.abs(dld_y) <= det_diam/2))
            # mask_temporal = np.logical_and((dld_t > 0), (dld_t < max_tof))
            # mask = np.logical_and(mask_temporal, mask_local)
            # dld_highVoltage = dld_highVoltage[mask]
            # dld_pulse = dld_pulse[mask]
            # # TODO
            # # dld_AbsoluteTimeStamp = dld_AbsoluteTimeStamp[mask]
            # dld_AbsoluteTimeStamp = dld_t[mask]
            # dld_t = dld_t[mask]
            # dld_x = dld_x[mask]
            # dld_y = dld_y[mask]

            # dld_highVoltage = np.expand_dims(dld_highVoltage, axis=1)
            # dld_pulse = np.expand_dims(dld_pulse, axis=1)
            # dld_AbsoluteTimeStamp = np.expand_dims(dld_AbsoluteTimeStamp, axis=1)
            # dld_t = np.expand_dims(dld_t, axis=1)
            # dld_x = np.expand_dims(dld_x, axis=1)
            # dld_y = np.expand_dims(dld_y, axis=1)

            dldGroupStorage = np.concatenate((dld_highVoltage, dld_pulse, dld_AbsoluteTimeStamp, dld_t, dld_x, dld_y),
                                             axis=1)
        dld_group_storage = create_pandas_dataframe(dldGroupStorage)
        return dld_group_storage
    except KeyError as error:
        logger.info(error)
        logger.critical("[*] Keys missing in the dataset")
    except FileNotFoundError as error:
        logger.info(error)
        logger.critical("[*] HDF5 file not found")


def concatenate_dataframes_of_dld_grp(
        dataframeList: "type:list - list of dataframes") -> "type:list - list of dataframes":
    """
        This function is helper function used to concatenate all relevant 
        information into a single list. 

        Attributes:
            dataframeList: List of different information from dld group. (type:list)
        Returns:
            dld_masterDataframe: Single concatenated list contaning 
                                 all relevant info (type: list)

    """
    dld_masterDataframeList = dataframeList
    dld_masterDataframe = pd.concat(dld_masterDataframeList, axis=1)
    return dld_masterDataframe


def plot_crop_experimetn_history(dldGroupStorage: "type: dataframes", max_tof=0, figure_size=(11/2.54, 5/2.54),
                                 rect=False, only_plot=False, save_name=False, laser=np.zeros(0)):
    """
        This function plots the experiment history. The plots showcase the 
        relationship between tof(time of flight) and voltage.

        Atrributes:
            dldGroupStorage: Dataframe containing info about dld group 
                             (type: pandas dataframe)
            max_tof: the maximum tof to be plot
            figure_size: The figure size
            only_plot: Default parameter set to false. if false it shows only the plot 
                       else it allows croppping functionality. (type: bool) 
            rect: Default parameter set to False. If true allows to crop
                  data by drawing a rectangular box (type: bool) 
            save_name: Default parameter set to False. Flag to choose whether
                       to save plot or not. (type: bool)
            laser: Default parameter set to False. Flag to choose whether
                       to plot laser intensity. (type: bool)
        Returns:
            Does not return anything.


    """
    fig1, ax1 = plt.subplots(figsize=figure_size, constrained_layout=True)

    # Plot tof and high voltage
    yaxis = dldGroupStorage['t (ns)'].to_numpy()
    high_voltage = dldGroupStorage['high_voltage (V)'].to_numpy()
    if max_tof > 0:
        high_voltage = high_voltage[yaxis < max_tof]
        yaxis = yaxis[yaxis < max_tof]

    high_voltage = high_voltage / 1000 # change to kv
    xaxis = np.arange(len(yaxis))

    heatmap, xedges, yedges = np.histogram2d(xaxis, yaxis, bins=(1200, 800))
    # heatmap[heatmap == 0] = 1  # to have zero after apply log
    # heatmap = np.log(heatmap)
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    # set x-axis label
    ax1.set_xlabel("Hit sequence Number", fontsize=12)
    # set y-axis label
    ax1.set_ylabel("Time of Flight [ns]", fontsize=12)
    img = plt.imshow(heatmap.T, extent=extent, origin='lower', aspect="auto")
    cmap = copy(plt.cm.plasma)
    cmap.set_bad(cmap(0))
    pcm = ax1.pcolormesh(xedges, yedges, heatmap.T, cmap=cmap, norm=colors.LogNorm(), rasterized=True)
    fig1.colorbar(pcm, ax=ax1, pad=0)

    # Make the x-axis ticks formatted to 0 decimal places
    ax1.xaxis.set_major_formatter(FormatStrFormatter('%0.0f'))

    # plot high voltage curve
    ax2 = ax1.twinx()

    xaxis2 = np.arange(len(high_voltage))
    ax2.plot(xaxis2, high_voltage, color='dodgerblue', linewidth=2)
    ax2.set_ylabel("High Voltage [kV]", color="dodgerblue", fontsize=12)
    if not only_plot:
        if not rect:
            rectangle_box_selector(ax2)
            plt.connect('key_press_event', selectors_data.toggle_selector)
        else:
            left, bottom, width, height = (
                variables.selected_x1, 0, variables.selected_x2 - variables.selected_x1, np.max(yaxis))
            rect = Rectangle((left, bottom), width, height, fill=True, alpha=0.3, color="r", linewidth=2)
            ax1.add_patch(rect)

    if len(laser) > 1:
        fig1.subplots_adjust(right=0.75)
        ax3 = ax1.twinx()
        ax3.plot(xaxis, laser, color='limegreen', linewidth=2)
        ax3.spines.right.set_position(("axes", 1.15))
        ax3.set_ylabel("Laser Intensity [${pJ}/{\mu m^2}$]", color="limegreen", fontsize=12)

    if save_name:
        plt.savefig("%s.png" % save_name, format="png", dpi=600)
        plt.savefig("%s.svg" % save_name, format="svg", dpi=600)
    # cax = ax1.inset_axes([1.14, 0.0, 0.05, 1])
    # plt.colorbar(img, ax=ax1, cax=cax)
    plt.show()


def plot_crop_FDM(data_crop: "type:list  - cropped list content", bins=(256, 256), figure_size=(10/2.54, 10/2.54),
                  circle=False, save_name=False, mask=True, only_plot=False):
    """
        This function is responsible for plotting the FDM. This function
        also allows  croping the plot to select the region of interest.

        Attributes:
            data_crop: Cropped dataset (type: list)
            bins: NA
            figure_size: size of the plot
            Circle: Default parameter set to False. If true, it allows 
                    to select region of interest by drawing the circle.
            save_name: Default parameter set to False. Flag to choose whether
                       to save plot or not. (type: bool) 
            only_plot: Default parameter set to false. if false it shows only the plot 
                       else it allows croppping functionality. (type: bool)
        Returns:
            Does not return anything.
    """
    fig1, ax1 = plt.subplots(figsize=figure_size, constrained_layout=True)
    logger = logging_library.logger_creator('data_loadcrop')
    # Plot and crop FDM
    x = data_crop['x_det (cm)'].to_numpy()
    y = data_crop['y_det (cm)'].to_numpy()

    FDM, xedges, yedges = np.histogram2d(x, y, bins=bins)

    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    # set x-axis label
    ax1.set_xlabel(r"$X_{det} (cm)$", fontsize=12)
    # set y-axis label
    ax1.set_ylabel(r"$Y_{det} (cm)$", fontsize=12)

    cmap = copy(plt.cm.plasma)
    cmap.set_bad(cmap(0))
    pcm = ax1.pcolormesh(xedges, yedges, FDM.T, cmap=cmap, norm=colors.LogNorm(), rasterized=True)
    fig1.colorbar(pcm, ax=ax1, pad=0)

    if not only_plot:
        if not circle:
            elliptical_shape_selector(ax1, fig1)
        else:
            print('x:', variables.selected_x_fdm, 'y:', variables.selected_y_fdm, 'roi:', variables.roi_fdm)
            circ = Circle((variables.selected_x_fdm, variables.selected_y_fdm), variables.roi_fdm, fill=True,
                          alpha=0.3, color='green', linewidth=1)
            ax1.add_patch(circ)
    if save_name:
        logger.info("Plot saved by the name {}".format(save_name))
        plt.savefig("%s.png" % save_name, format="png", dpi=300)
        plt.savefig("%s.eps" % save_name, format="eps", dpi=300)
    plt.show()


def rectangle_box_selector(axisObject: "type:object"):
    # drawtype is 'box' or 'line' or 'none'
    """
        This function allows to create rectangular box to select region 
        of interest. 

        Atrributes:
            axisObject: Object to create rectangular box
        
        Returns:
            Does not return anything

    """
    selectors_data.toggle_selector.RS = RectangleSelector(axisObject, selectors_data.line_select_callback,
                                                          useblit=True,
                                                          button=[1, 3],  # don't use middle button
                                                          minspanx=1, minspany=1,
                                                          spancoords='pixels',
                                                          interactive=True)


def crop_dataset(dld_master_dataframe: "type: dataframes") -> "type: dataframe":
    """
        This function allows to crop dataset.    

        Atrributes:
            dld_master_dataframe: concatenated dataset (type: dataframe)
        Returns:
            data_crop: cropped dataset (type: dataframe)

    """
    data_crop = dld_master_dataframe.loc[int(variables.selected_x1):int(variables.selected_x2), :]
    data_crop.reset_index(inplace=True, drop=True)
    return data_crop


def elliptical_shape_selector(axisObject: "type:object", figureObject: "type:object"):
    """
       This function allows to create elliptical box to select region 
       of interest. 

        Atrributes:
            axisObject: Object to create axis of the plot.
            figureObject: Object to create figure.
        Returns:
            Does not return anything.
        
    """
    selectors_data.toggle_selector.ES = EllipseSelector(axisObject, selectors_data.onselect, useblit=True,
                                                        button=[1, 3],  # don't use middle button
                                                        minspanx=1, minspany=1,
                                                        spancoords='pixels',
                                                        interactive=True)
    figureObject.canvas.mpl_connect('key_press_event', selectors_data.toggle_selector)


def crop_data_after_selection(data_crop: "dataframe") -> "dataframe":
    """
        This function crops the dataset after region of interest has been
        selected.

        Atrributes:
            data_crop: Original dataset that is to be cropped. (type:dataframe)
        Returns:
            data_crop: Cropped dataset. (type: dataframe)
        
    """
    # crop the data based on selected are of FDM
    x = data_crop['x_det (cm)'].to_numpy()
    y = data_crop['y_det (cm)'].to_numpy()
    detector_dist = np.sqrt(
        (x - variables.selected_x_fdm) ** 2 + (y - variables.selected_y_fdm) ** 2)
    mask_fdm = (detector_dist > variables.roi_fdm)
    data_crop.drop(np.where(mask_fdm)[0], inplace=True)
    data_crop.reset_index(inplace=True, drop=True)
    return data_crop


def create_pandas_dataframe(data_crop: "type:numpy array"):
    """
        This function create a pandas dataframe from the cropped data. 

        Attributes:
            data_crop: Cropped dataset (type: dataframe) (type: string)
            tdc: Type of tdc (surface_concept/roentdec) (type: string)
            pulser_mode: Type of pulse mode (voltage/laser) (type: string)
        Returns:
            hdf_dataframe: dataframe that is to be inserted in hdf file. 
                           (type: dataframe)
    """
    hdf_dataframe = pd.DataFrame(data=data_crop,
                                 columns=['high_voltage (V)', 'pulse', 'start_counter', 't (ns)',
                                          'x_det (cm)', 'y_det (cm)'])

    hdf_dataframe['start_counter'] = hdf_dataframe['start_counter'].astype('uint32')
    return hdf_dataframe
