import concurrent.futures
import multiprocessing
from copy import copy
from itertools import product
from math import ceil

import fast_histogram
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams, colors
from scipy.optimize import curve_fit
from scipy.signal import find_peaks
from sklearn.cluster import KMeans, DBSCAN


def cluster_tof(dld_highVoltage_peak, dld_t_peak, calibration_mode, num_cluster, plot=True, fig_size=(5, 5)):
    data = np.concatenate((dld_highVoltage_peak.reshape(-1, 1), dld_t_peak.reshape(-1, 1)), axis=1)
    # Calculate the number of elements to extract (20 percent)
    num_elements = int(0.05 * data.shape[0])  # Use shape[0] to get the number of rows
    # Create a mask of False (0) values with the same shape as the data array
    mask = np.zeros(data.shape[0], dtype=bool)
    # Randomly select num_elements indices to set to True (1) in the mask
    random_indices = np.random.choice(data.shape[0], num_elements, replace=False)
    mask[random_indices] = True
    # Use numpy.compress to filter the data based on the mask
    data_filtered = np.compress(mask, data, axis=0)

    k_means = KMeans(init="k-means++", n_clusters=num_cluster, n_init=10)
    k_means.fit(data_filtered)
    cluster_labels = k_means.predict(data)

    if plot:
        fig1, ax1 = plt.subplots(figsize=fig_size, constrained_layout=True)
        if calibration_mode == 'tof':
            ax1.set_ylabel("Time of Flight (ns)", fontsize=10)
            label = 't'
        elif calibration_mode == 'mc':
            ax1.set_ylabel("mc (Da)", fontsize=10)
            label = 'mc'
        mask = np.random.randint(0, len(dld_highVoltage_peak), 800)
        x = plt.scatter(np.array(dld_highVoltage_peak[mask]) / 1000, np.array(dld_t_peak[mask]),
                        c=cluster_labels[mask], label=label, s=1)
        ax1.set_xlabel("Voltage (kV)", fontsize=10)
        plt.grid(alpha=0.3, linestyle='-.', linewidth=0.4)
        plt.show()
    hv_range = []
    for i in range(num_cluster):

        dld_highVoltage_peak_c = dld_highVoltage_peak[cluster_labels == i]
        dld_t_peak_c = dld_t_peak[cluster_labels == i]
        if plot:
            mask = np.random.randint(0, len(dld_highVoltage_peak_c), 400)
            fig1, ax1 = plt.subplots(figsize=fig_size, constrained_layout=True)
            x = plt.scatter(np.array(dld_highVoltage_peak_c[mask]) / 1000, np.array(dld_t_peak_c[mask]), color='blue',
                            label=label, s=1)
            ax1.set_xlabel("Voltage (kV)", fontsize=10)
            plt.grid(alpha=0.3, linestyle='-.', linewidth=0.4)
            plt.show()
        hv_range.append([np.min(dld_highVoltage_peak_c), np.max(dld_highVoltage_peak_c)])

    return cluster_labels, [hv_range[0][:]]


def voltage_corr(x, a, b, c):
    """
    Returns the voltage correction value for a given x using a quadratic equation.

    Parameters:
    - x (array): The input array.
    - a (float): Coefficient of x^0.
    - b (float): Coefficient of x^1.
    - c (float): Coefficient of x^2.

    Returns:
    - array: The voltage correction value.

    """
    y = a + b * x + c * (x ** 2)
    # y = a / ((b * x) + c)
    return y


def voltage_correction(dld_highVoltage_peak, dld_t_peak, variables, maximum_location, index_fig, figname, sample_size,
                       mode, calibration_mode, sample_range_max, plot=True, save=False,
                       fig_size=(5, 5)):
    """
    Performs voltage correction and plots the graph based on the passed arguments.

    Parameters:
    - dld_highVoltage_peak (array): Array of high voltage peaks.
    - dld_t_peak (array): Array of t peaks.
    - maximum_location (float): Maximum location value.
    - index_fig (string): Index of the saved plot.
    - figname (string): Name of the saved plot image.
    - sample_size (string): Sample size.
    - mode (string): Mode ('ion_seq'/'voltage').
    - calibration_mode (string): Type of calibration mode (tof/mc).
    - sample_range_max (string): Type of peak_x mode (histogram/mean/median).
    - outlier_remove (bool): Indicates whether to remove outliers. Default is True.
    - plot (bool): Indicates whether to plot the graph. Default is True.
    - save (bool): Indicates whether to save the plot. Default is False.
    - fig_size (tuple): Figure size in inches. Default is (7, 5).

    Returns:
    - fitresult (array): Corrected voltage array.

    """
    dld_t_peak_list = []
    high_voltage_mean_list = []
    if mode == 'ion_seq':
        for i in range(int(len(dld_highVoltage_peak) / sample_size) + 1):
            dld_highVoltage_peak_selected = dld_highVoltage_peak[i * sample_size:(i + 1) * sample_size]
            dld_t_peak_selected = dld_t_peak[i * sample_size:(i + 1) * sample_size]
            if sample_range_max == 'histogram':
                try:
                    bins = np.linspace(np.min(dld_t_peak_selected), np.max(dld_t_peak_selected),
                                       round(np.max(dld_t_peak_selected) / 0.1))
                    y, x = np.histogram(dld_t_peak_selected, bins=bins)
                    peaks, properties = find_peaks(y, height=0)
                    index_peak_max_ini = np.argmax(properties['peak_heights'])
                    max_peak = peaks[index_peak_max_ini]
                    dld_t_peak_list.append(x[max_peak] / maximum_location)

                    mask_v = np.logical_and((dld_t_peak_selected >= x[max_peak] - 0.1)
                                            , (dld_t_peak_selected <= x[max_peak] + 0.1))
                    high_voltage_mean_list.append(np.mean(dld_highVoltage_peak_selected[mask_v]))
                except ValueError:
                    print('cannot find the maximum')
                    dld_t_mean = np.median(dld_t_peak_selected)
                    dld_t_peak_list.append(dld_t_mean / maximum_location)

                    high_voltage_mean = np.mean(dld_highVoltage_peak_selected)
                    high_voltage_mean_list.append(high_voltage_mean)
            elif sample_range_max == 'mean':
                dld_t_mean = np.mean(dld_t_peak_selected)
                dld_t_peak_list.append(dld_t_mean / maximum_location)
                high_voltage_mean = np.mean(dld_highVoltage_peak_selected)
            elif sample_range_max == 'median':
                dld_t_mean = np.median(dld_t_peak_selected)
                dld_t_peak_list.append(dld_t_mean / maximum_location)
                high_voltage_mean = np.median(dld_highVoltage_peak_selected)
                high_voltage_mean_list.append(high_voltage_mean)

    elif mode == 'voltage':
        for i in range(int((np.max(dld_highVoltage_peak) - np.min(dld_highVoltage_peak)) / sample_size) + 1):
            mask = np.logical_and((dld_highVoltage_peak >= (np.min(dld_highVoltage_peak) + (i) * sample_size)),
                                  (dld_highVoltage_peak < (np.min(dld_highVoltage_peak) + (i + 1) * sample_size)))
            dld_highVoltage_peak_selected = dld_highVoltage_peak[mask]
            dld_t_peak_selected = dld_t_peak[mask]

            if sample_range_max == 'histogram':
                try:
                    bins = np.linspace(np.min(dld_t_peak_selected), np.max(dld_t_peak_selected),
                                       round(np.max(dld_t_peak_selected) / 0.1))
                    y, x = np.histogram(dld_t_peak_selected, bins=bins)
                    peaks, properties = find_peaks(y, height=0)
                    index_peak_max_ini = np.argmax(properties['peak_heights'])
                    max_peak = peaks[index_peak_max_ini]
                    dld_t_peak_list.append(x[max_peak] / maximum_location)

                    mask_v = np.logical_and((dld_t_peak_selected >= x[max_peak] - 0.2)
                                            , (dld_t_peak_selected <= x[max_peak] + 0.2))
                    high_voltage_mean_list.append(np.mean(dld_highVoltage_peak_selected[mask_v]))
                except ValueError:
                    print('cannot find the maximum')
                    dld_t_mean = np.median(dld_t_peak_selected)
                    dld_t_peak_list.append(dld_t_mean / maximum_location)

                    high_voltage_mean = np.mean(dld_highVoltage_peak_selected)
                    high_voltage_mean_list.append(high_voltage_mean)
            elif sample_range_max == 'mean':
                dld_t_mean = np.mean(dld_t_peak_selected)
                dld_t_peak_list.append(dld_t_mean / maximum_location)

                high_voltage_mean = np.mean(dld_highVoltage_peak_selected)
                high_voltage_mean_list.append(high_voltage_mean)
            elif sample_range_max == 'median':
                dld_t_mean = np.median(dld_t_peak_selected)
                dld_t_peak_list.append(dld_t_mean / maximum_location)

                high_voltage_mean = np.median(dld_highVoltage_peak_selected)
                high_voltage_mean_list.append(high_voltage_mean)

    fitresult, _ = curve_fit(voltage_corr, np.array(high_voltage_mean_list), np.array(dld_t_peak_list))

    if plot or save:
        fig1, ax1 = plt.subplots(figsize=fig_size, constrained_layout=True)
        if calibration_mode == 'tof':
            ax1.set_ylabel("Time of Flight (ns)", fontsize=10)
            label = 't'
        elif calibration_mode == 'mc':
            ax1.set_ylabel("mc (Da)", fontsize=10)
            label = 'mc'

        x = plt.scatter(np.array(high_voltage_mean_list) / 1000, np.array(dld_t_peak_list) * maximum_location,
                        color="forestgreen", label=r"$%s_{wp}$" % label, s=5)
        ax1.set_xlabel("Voltage (kV)", fontsize=10)
        plt.grid(alpha=0.3, linestyle='-.', linewidth=0.4)

        ax2 = ax1.twinx()
        f_v = voltage_corr(np.array(high_voltage_mean_list), *fitresult)
        y = ax2.plot(np.array(high_voltage_mean_list) / 1000, f_v, color='r', label=r"$C_V$")
        ax2.set_ylabel(r"$C_V$", color="red", fontsize=10)  # Get the current axis
        ax2.tick_params(axis='y', colors='red')  # Change color and thickness of tick labels on y-axis
        ax2.spines['right'].set_color('red')  # Change color of right border
        plt.legend(handles=[x, y[0]], loc='lower left', markerscale=5., prop={'size': 10})

        if save:
            # Enable rendering for text elements
            rcParams['svg.fonttype'] = 'none'
            plt.savefig(variables.result_path + "//vol_corr_%s_%s.svg" % (figname, index_fig), format="svg", dpi=600)
            plt.savefig(variables.result_path + "//vol_corr_%s_%s.png" % (figname, index_fig), format="png", dpi=600)

        if plot:
            plt.show()

    return fitresult


def voltage_corr_main(dld_highVoltage, variables, sample_size, mode, calibration_mode, index_fig, plot, save,
                      apply_local='all', noise_remove=True, maximum_cal_method='mean',
                      maximum_sample_method='mean', fig_size=(5, 5)):
    """
    Perform voltage correction on the given data.

    Args:
        dld_highVoltage (numpy.ndarray): Array of high voltages.
        sample_size (int): Size of the sample.
        mode (str): Mode of the correction.
        calibration_mode (str): Calibration mode ('tof' or 'mc').
        index_fig (int): Index of the figure.
        plot (bool): Whether to plot the results.
        save (bool): Whether to save the plots.
        apply_local (str, optional): Whether to apply local correction ('all', voltage', or 'voltage_temporal').
        noise_remove (bool, optional): Whether to remove noise. Defaults to True.
        maximum_cal_method (str, optional): Maximum calculation method ('mean', 'histogram', 'median').
        maximum_sample_method (str, optional): Sample range maximum ('mean', 'histogram', 'median').
        fig_size (tuple, optional): Size of the figure. Defaults to (5, 5).
    """
    print('The left and right side of the main peak is:', variables.selected_x1, variables.selected_x2)
    if calibration_mode == 'tof':
        mask_temporal = np.logical_and(
            (variables.dld_t_calib > variables.selected_x1),
            (variables.dld_t_calib < variables.selected_x2)
        )
        dld_peak_b = variables.dld_t_calib[mask_temporal]
    elif calibration_mode == 'mc':
        mask_temporal = np.logical_and(
            (variables.mc_calib > variables.selected_x1),
            (variables.mc_calib < variables.selected_x2)
        )
        dld_peak_b = variables.mc_calib[mask_temporal]

    dld_highVoltage_peak_v = dld_highVoltage[mask_temporal]

    if noise_remove:
        data = np.column_stack((dld_highVoltage_peak_v, dld_peak_b))
        # Use DBSCAN to cluster the data
        num_cores = multiprocessing.cpu_count()
        half_cores = max(1, ceil(num_cores / 2))
        dbscan = DBSCAN(eps=1, min_samples=5, n_jobs=half_cores)
        labels = dbscan.fit_predict(data)
        # hdbscan = HDBSCAN(min_cluster_size=10, min_samples=10, n_jobs=half_cores)
        # labels = hdbscan.fit_predict(data)
        noise_mask = labels == -1  # Points labeled as noise
        if plot or save:
            # Plot how correction factor for selected peak_x
            fig1, ax1 = plt.subplots(figsize=fig_size, constrained_layout=True)
            if len(dld_highVoltage_peak_v) > 1000:
                mask_t = np.random.randint(0, len(dld_highVoltage_peak_v), 1000)
            else:
                mask_t = np.ones(len(dld_highVoltage_peak_v), dtype=bool)

            mask = np.copy(~noise_mask)
            mask[~mask_t] = False
            x = plt.scatter(dld_highVoltage_peak_v[mask] / 1000, dld_peak_b[mask], color='blue', label=r"$t$", s=1,)
            mask = np.copy(noise_mask)
            mask[~mask_t] = False
            y = plt.scatter(dld_highVoltage_peak_v[mask] / 1000, dld_peak_b[mask], color='red', label=r"$t_{noise}$",
                            s=1)
            plt.legend(handles=[x, y], loc='upper left', markerscale=5., prop={'size': 10})
            if save:
                # Enable rendering for text elements
                rcParams['svg.fonttype'] = 'none'
                plt.savefig(variables.result_path + "//noise_remove_%s.svg" % index_fig, format="svg", dpi=600)
                plt.savefig(variables.result_path + "//noise_remove_%s.png" % index_fig, format="png", dpi=600)
            if plot:
                plt.show()

            print('The noise is removed from the data')
            print('The percentage of noise is:', len(dld_highVoltage_peak_v[noise_mask]) / len(dld_highVoltage_peak_v))

        cleaned_data = data[~noise_mask]
        # Update the original arrays with cleaned data
        dld_highVoltage_peak_v = cleaned_data[:, 0]
        dld_peak_b = cleaned_data[:, 1]

    print('The number of ions is:', len(dld_highVoltage_peak_v))
    if sample_size > len(dld_highVoltage_peak_v):
        sample_size = int(len(dld_highVoltage_peak_v) / 10)
        print('The sample size is larger than the number of ions. The sample size is set to:', sample_size)

    print('The number of samples is:', int(len(dld_highVoltage_peak_v) / sample_size))

    if maximum_cal_method == 'histogram':
        bins = np.linspace(np.min(dld_peak_b), np.max(dld_peak_b),
                           round(np.max(dld_peak_b) / 0.1))
        # y, x = np.histogram(dld_peak_b, bins=bins)
        y = fast_histogram.histogram1d(dld_peak_b, bins=bins, range=(np.min(dld_peak_b), np.max(dld_peak_b)))
        x = bins
        peaks, properties = find_peaks(y, height=0)
        index_peak_max_ini = np.argmax(properties['peak_heights'])
        max_peak = peaks[index_peak_max_ini]
        maximum_location = x[max_peak]
    elif maximum_cal_method == 'mean':
        maximum_location = np.mean(dld_peak_b)
    elif maximum_cal_method == 'median':
        maximum_location = np.median(dld_peak_b)


    print('The maximum/mean/median of histogram is located at:', maximum_location)
    print('The high voltage ranges are:', np.min(dld_highVoltage_peak_v), np.max(dld_highVoltage_peak_v))
    print('The mean of tof/mc  before voltage calibration is:', np.mean(dld_peak_b))
    fitresult = voltage_correction(dld_highVoltage_peak_v, dld_peak_b, variables,
                                   maximum_location, index_fig=index_fig,
                                   figname='voltage_corr',
                                   sample_size=sample_size, mode=mode, calibration_mode=calibration_mode,
                                   sample_range_max=maximum_sample_method, plot=plot, save=save, fig_size=fig_size)

    calibration_mc_tof = np.copy(variables.dld_t_calib) if calibration_mode == 'tof' else np.copy(variables.mc_calib)



    print('The fit result is:', fitresult)
    if apply_local == 'voltage_temporal':
        mask_fv = mask_temporal
    elif apply_local == 'voltage':
        mask_fv = mask_temporal
    elif apply_local == 'all':
        mask_fv = np.ones_like(dld_highVoltage, dtype=bool)

    f_v = voltage_corr(dld_highVoltage[mask_fv], *fitresult)

    calibration_mc_tof[mask_fv] = calibration_mc_tof[mask_fv] / f_v

    if plot or save:
        # Plot how correction factor for selected peak_x
        fig1, ax1 = plt.subplots(figsize=fig_size, constrained_layout=True)
        if len(dld_highVoltage_peak_v) > 1000:
            mask = np.random.randint(0, len(dld_highVoltage_peak_v), 1000)
        else:
            mask = np.arange(len(dld_highVoltage_peak_v))
        x = plt.scatter(dld_highVoltage_peak_v[mask] / 1000, dld_peak_b[mask], color="blue", label=r"$t$", s=1)

        if calibration_mode == 'tof':
            ax1.set_ylabel("Time of Flight (ns)", fontsize=10)
        elif calibration_mode == 'mc':
            ax1.set_ylabel("mc (Da)", fontsize=10)
        ax1.set_xlabel("Voltage (V)", fontsize=10)
        plt.grid(alpha=0.3, linestyle='-.', linewidth=0.4)

        # Plot high voltage curve
        ax2 = ax1.twinx()
        f_v_plot = voltage_corr(dld_highVoltage_peak_v, *fitresult)
        f_v_list_plot = f_v_plot

        y = ax2.plot(dld_highVoltage_peak_v / 1000, 1 / f_v_plot, color='r', label=r"$C_{V}^{-1}$")
        ax2.set_ylabel(r"$C_{V}^{-1}$", color="red", fontsize=10)
        ax2.tick_params(axis='y', colors='red')  # Change color and thickness of tick labels on y-axis
        ax2.spines['right'].set_color('red')  # Change color of right border
        plt.legend(handles=[x, y[0]], loc='upper left', markerscale=5., prop={'size': 10})

        if save:
            # Enable rendering for text elements
            rcParams['svg.fonttype'] = 'none'
            plt.savefig(variables.result_path + "//vol_corr_%s.svg" % index_fig, format="svg", dpi=600)
            plt.savefig(variables.result_path + "//vol_corr_%s.png" % index_fig, format="png", dpi=600)
        plt.show()

        # Plot corrected tof/mc vs. uncalibrated tof/mc
        fig1, ax1 = plt.subplots(figsize=fig_size, constrained_layout=True)
        x = plt.scatter(dld_highVoltage_peak_v[mask] / 1000, dld_peak_b[mask], color="blue", label='t', s=1)
        if calibration_mode == 'tof':
            ax1.set_ylabel("Time of Flight (ns)", fontsize=10)
        elif calibration_mode == 'mc':
            ax1.set_ylabel("mc (Da)", fontsize=10)
        ax1.set_xlabel("Voltage (kV)", fontsize=10)
        plt.grid(alpha=0.3, linestyle='-.', linewidth=0.4)

        dld_t_plot = dld_peak_b * (1 / f_v_plot)

        y = plt.scatter(dld_highVoltage_peak_v[mask] / 1000, dld_t_plot[mask], color="red", label=r"$t_{C_{V}}$",
                        s=1)

        plt.legend(handles=[x, y], loc='upper right', markerscale=5., prop={'size': 10})

        if save:
            # Enable rendering for text elements
            rcParams['svg.fonttype'] = 'none'
            plt.savefig(variables.result_path + "//peak_tof_V_corr_%s.svg" % index_fig, format="svg", dpi=600)
            plt.savefig(variables.result_path + "//peak_tof_V_corr_%s.png" % index_fig, format="png", dpi=600)
        if plot:
            plt.show()

    print('The mean of tof/mc  after voltage calibration is:', np.mean(calibration_mc_tof[mask_temporal]))
    variables.dld_t_calib = calibration_mc_tof


def bowl_corr(data_xy, a, b, c, d, e, f):
    """
    Compute the result of a quadratic equation based on the input data.

    Args:
        data_xy (list): Tuple containing the x and y data points.
        a, b, c, d, e, f (float): Coefficients of the quadratic equation.

    Returns:
        result (numpy.ndarray): Result of the quadratic equation.
    """
    x = data_xy[0]
    y = data_xy[1]
    result = a + b * x + c * y + d * (x ** 2) + e * x * y + f * (y ** 2)
    return result


def hemisphere_corr(data_xy, a, b, c, r):
    """
    Objective function for the bowl correction.

    Args:
        data_xy (list): Tuple containing the x and y data points.
        a (float): Coefficient controlling the curvature in the x-direction.
        b (float): x-coordinate of the center of the hemisphere in the xy-plane.
        c (float): Coefficient controlling the curvature in the y-direction.
        r (float): Radius of the hemisphere.
        hemisphere. In the provided function hemisphere_fit, these coefficients are associated with the squared terms
        (x - b)^2 and (y - b)^2.
        r (float): The radius of the hemisphere.

    Returns:
        result (numpy.ndarray): Result of the quadratic equation.
    """
    x = data_xy[0]
    y = data_xy[1]
    result = a * (x - b) ** 2 + c * (y - b) ** 2 + r ** 2
    return result


def compute_sample(i, j, d, dld_x_bowl, dld_y_bowl, dld_t_bowl, maximum_location, sample_range_max):
    """
    Compute the sample for the given data.

    Args:
        i (int): Index i.
        j (int): Index j.
        d (int): Sample size.
        dld_x_bowl (numpy.ndarray): X coordinates of the data points.
        dld_y_bowl (numpy.ndarray): Y coordinates of the data points.
        dld_t_bowl (numpy.ndarray): Time values of the data points.
        maximum_location (float): Maximum location for normalization.
        sample_range_max (str): Sample range maximum ('mean' or 'histogram').

    Returns:
        x_sample (float): X sample value.
        y_sample (float): Y sample value.
        dld_t_peak (float): Time peak value.
    """
    mask_x = np.logical_and((dld_x_bowl < j + d), (dld_x_bowl > j))
    mask_y = np.logical_and((dld_y_bowl < i + d), (dld_y_bowl > i))
    mask = np.logical_and(mask_x, mask_y)

    if len(mask[mask]) > 0:
        x_y_selected = np.vstack((dld_x_bowl[mask], dld_y_bowl[mask])).T
        x_sample = np.median(x_y_selected[:, 0])
        y_sample = np.median(x_y_selected[:, 1])

        if sample_range_max == 'mean':
            dld_t_peak = np.mean(dld_t_bowl[mask]) / maximum_location
        elif sample_range_max == 'histogram':
            try:
                dld_t_bowl_selected = dld_t_bowl[mask]
                if len(dld_t_bowl_selected) > 500000:
                    dld_t_bowl_selected = np.random.choice(dld_t_bowl_selected, 500000, replace=False)

                bins = np.linspace(np.min(dld_t_bowl_selected), np.max(dld_t_bowl_selected),
                                   round(np.max(dld_t_bowl_selected) / 0.1))

                y_hist = fast_histogram.histogram1d(dld_t_bowl_selected,
                                                    bins=round(np.max(dld_t_bowl_selected) / 0.1) - 1,
                                                    range=(np.min(dld_t_bowl_selected), np.max(dld_t_bowl_selected)))
                peaks, properties = find_peaks(y_hist, height=0)

                if len(peaks) > 0:
                    index_peak_max_ini = np.argmax(properties['peak_heights'])
                    max_peak = peaks[index_peak_max_ini]
                    dld_t_peak = bins[max_peak] / maximum_location
                else:
                    dld_t_peak = np.mean(dld_t_bowl[mask]) / maximum_location
            except ValueError:
                print('cannot find the maximum')
                dld_t_peak = np.mean(dld_t_bowl[mask]) / maximum_location

            return x_sample, y_sample, dld_t_peak
    return None, None, None  # Return None if no samples found


def bowl_correction(dld_x_bowl, dld_y_bowl, dld_t_bowl, variables, det_diam, maximum_location, sample_range_max,
                    sample_size, calibration_mode, fit_mode, index_fig, plot, save, fig_size=(7, 5)):
    """
    Perform bowl correction on the input data.

    Args:
        dld_x_bowl (numpy.ndarray): X coordinates of the data points.
        dld_y_bowl (numpy.ndarray): Y coordinates of the data points.
        dld_t_bowl (numpy.ndarray): Time values of the data points.
        det_diam (float): Diameter of the detector.
        maximum_location (float): Maximum location for normalization.
        sample_range_max (str, optional): Sample range maximum ('mean' or 'histogram').
        sample_size (int): Size of each sample.
        calibration_mode (str): Calibration mode ('tof' or 'mc').
        fit_mode (str): Fit mode ('curve_fit' or 'hemisphere_fit').
        index_fig (int): Index for figure naming.
        plot (bool): Flag indicating whether to plot the surface.
        save (bool): Flag indicating whether to save the plot.
        fig_size (tuple): Size of the figure.

    Returns:
        parameters (numpy.ndarray): Optimized parameters of the bowl correction.
    """
    x_sample_list = []
    y_sample_list = []
    dld_t_peak_list = []

    w1 = int(np.min(dld_x_bowl))
    w2 = int(np.max(dld_x_bowl))
    h1 = int(np.min(dld_y_bowl))
    h2 = int(np.max(dld_y_bowl))

    d = sample_size  # sample size is in mm - so we change it to cm
    grid = product(range(h1, h2 - h2 % d, d), range(w1, w2 - w2 % d, d))

    # Use ThreadPoolExecutor or ProcessPoolExecutor
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(compute_sample, i, j, d, dld_x_bowl, dld_y_bowl, dld_t_bowl, maximum_location,
                                   sample_range_max)
                   for i, j in grid]

        for future in concurrent.futures.as_completed(futures):
            x_sample, y_sample, dld_t_peak = future.result()
            if x_sample is not None:
                x_sample_list.append(x_sample)
                y_sample_list.append(y_sample)
                dld_t_peak_list.append(dld_t_peak)

    # The rest of your function remains unchanged
    if fit_mode == 'curve_fit':
        parameters, covariance = curve_fit(bowl_corr, [np.array(x_sample_list), np.array(y_sample_list)],
                                           np.array(dld_t_peak_list))
    elif fit_mode == 'hemisphere_fit':
        # Initial guess for the parameters (a, b, c, r)
        initial_guess = [1.0, 0.0, 1.0, 1.0]
        parameters, covariance = curve_fit(hemisphere_corr, [np.array(x_sample_list), np.array(y_sample_list)],
                                           np.array(dld_t_peak_list), p0=initial_guess)
        print('The cx, cy, r, c0 are:', parameters)

    if plot or save:
        if calibration_mode == 'tof':
            label = 't'
        elif calibration_mode == 'mc':
            label = 'mc'
        model_x_data = np.array(x_sample_list)
        model_y_data = np.array(y_sample_list)
        X, Y = np.meshgrid(model_x_data, model_y_data)
        if fit_mode == 'curve_fit':
            Z = bowl_corr(np.array([X, Y]), *parameters)
        elif fit_mode == 'hemisphere_fit':
            Z = hemisphere_corr(np.array([X, Y]), *parameters)

        fig, ax = plt.subplots(figsize=fig_size, subplot_kw=dict(projection="3d"), constrained_layout=True)
        box = ax.get_position()
        ax.set_position([box.x0 + 0.1, box.y0 + 0.1, box.width * 0.75, box.height * 0.75])
        scat = ax.scatter(model_x_data, model_y_data, zs=1 / np.array(dld_t_peak_list), color="forestgreen",
                          label=r"$%s_{wp}$" % label, s=3)
        fig.add_axes(ax)
        cmap = copy(plt.cm.plasma)
        cmap.set_bad(cmap(0))
        surf = ax.plot_surface(X, Y, 1 / Z, color='red', alpha=0.05, label='bowl')
        ax.set_xlabel(r'$X_{det}$ (mm)', fontsize=10, labelpad=10)
        ax.set_ylabel(r'$Y_{det}$ (mm)', fontsize=10, labelpad=10)
        ax.set_zlabel(r"${C_B}^{-1}$", fontsize=10, labelpad=5, color='red')
        ax.zaxis.set_major_formatter(plt.FormatStrFormatter('%.2f'))
        ax.zaxis.line.set_color('red')

        # Change z-axis tick label color
        for tick in ax.get_zaxis().get_ticklabels():
            tick.set_color('red')
        ax.view_init(elev=7, azim=-41)

        if save:
            # Enable rendering for text elements
            rcParams['svg.fonttype'] = 'none'
            plt.savefig(variables.result_path + "//bowl_corr_%s.svg" % index_fig, format="svg", dpi=600)
            plt.savefig(variables.result_path + "//bowl_corr_%s.png" % index_fig, format="png", dpi=600)
        if plot:
            plt.show()

    return parameters


def bowl_correction_main(dld_x, dld_y, dld_highVoltage, variables, det_diam, sample_size, fit_mode, calibration_mode,
                         index_fig, plot, save, apply_local='all', maximum_cal_method='mean', maximum_sample_method='mean',
                         fig_size=(5, 5), fast_calibration=False):
    """
    Perform bowl correction on the input data and plot the results.

    Args:
        dld_x (numpy.ndarray): X positions.
        dld_y (numpy.ndarray): Y positions.
        dld_highVoltage (numpy.ndarray): High voltage values.
        det_diam (float): Detector diameter.
        sample_size (int): Sample size.
        fit_mode (str): Fit mode ('curve_fit' or 'hemisphere_fit').
        calibration_mode (str): Calibration mode ('tof' or 'mc').
        index_fig (int): Index figure.
        plot (bool): Flag indicating whether to plot the results.
        save (bool): Flag indicating whether to save the plots.
        apply_local (str, optional): Apply bowl correction locally ('all', 'temporal').
        maximum_cal_method (str, optional): Maximum calculation method ('mean' or 'histogram').
        maximum_sample_method (str, optional): Sample range maximum ('mean' or 'histogram').
        fig_size (tuple, optional): Figure size.
        fast_calibration (bool, optional): Flag indicating whether to perform fast calibration.

    Returns:
        None

    """
    dld_x = dld_x * 10 # change the x position to mm from cm
    dld_y = dld_y * 10 # change the y position to mm from cm

    print('The left and right side of the main peak is:', variables.selected_x1, variables.selected_x2)
    if calibration_mode == 'tof':
        mask_temporal = np.logical_and((variables.dld_t_calib > variables.selected_x1),
                                       (variables.dld_t_calib < variables.selected_x2))
    elif calibration_mode == 'mc':
        mask_temporal = np.logical_and((variables.mc_calib > variables.selected_x1),
                                       (variables.mc_calib < variables.selected_x2))

    dld_peak = variables.dld_t_calib[mask_temporal] if calibration_mode == 'tof' else variables.mc_calib[mask_temporal]
    print('The number of ions is:', len(dld_peak))

    dld_peak_mid = np.copy(dld_peak)
    if len(dld_peak_mid) > 4000000 and fast_calibration:
        dld_peak_mid = np.random.choice(dld_peak_mid, 4000000, replace=False)
    if maximum_cal_method == 'histogram':
        try:
            bins = np.linspace(np.min(dld_peak_mid), np.max(dld_peak_mid), round(np.max(dld_peak_mid) / 0.1))
            # y, x = np.histogram(dld_peak_mid, bins=bins)
            y = fast_histogram.histogram1d(dld_peak_mid, bins=round(np.max(dld_peak_mid) / 0.1) - 1,
                                           range=(np.min(dld_peak_mid), np.max(dld_peak_mid)))
            x = bins
            peaks, properties = find_peaks(y, height=0)
            index_peak_max_ini = np.argmax(properties['peak_heights'])
            maximum_location = x[peaks[index_peak_max_ini]]
        except:
            print('The histogram max calculation method failed, using mean instead.')
            maximum_location = np.mean(dld_peak_mid)
    elif maximum_cal_method == 'mean':
        maximum_location = np.mean(dld_peak_mid)
    print('The maximum/mean of peak is located at:', maximum_location)

    dld_x_peak = dld_x[mask_temporal]
    dld_y_peak = dld_y[mask_temporal]
    dld_highVoltage_peak = dld_highVoltage[mask_temporal]

    print('The mean of tof  before bowl calibration is:', np.mean(dld_peak))
    parameters = bowl_correction(dld_x_peak, dld_y_peak, dld_peak, variables, det_diam, maximum_location,
                                 maximum_sample_method, sample_size=sample_size, calibration_mode=calibration_mode,
                                 fit_mode=fit_mode, index_fig=index_fig, plot=plot, save=save, fig_size=fig_size)
    print('The fit result is:', parameters)

    if apply_local == 'all':
        mask_fv = np.ones_like(dld_x, dtype=bool)
    elif apply_local == 'temporal':
        mask_fv = mask_temporal

    if fit_mode == 'curve_fit':
        f_bowl = bowl_corr([dld_x[mask_fv], dld_y[mask_fv]], *parameters)
    elif fit_mode == 'hemisphere_fit':
        f_bowl = hemisphere_corr([dld_x[mask_fv], dld_y[mask_fv]], *parameters)

    calibration_mc_tof = np.copy(variables.dld_t_calib) if calibration_mode == 'tof' else np.copy(variables.mc_calib)

    calibration_mc_tof[mask_fv] = calibration_mc_tof[mask_fv] / f_bowl

    print('The mean of tof  before bowl calibration is:', np.mean(calibration_mc_tof[mask_temporal]))

    if plot or save:
        # Plot how bowl correct tof/mc vs high voltage
        fig1, ax1 = plt.subplots(figsize=fig_size, constrained_layout=True)
        mask = np.random.randint(0, len(dld_highVoltage_peak), 10000)

        x = plt.scatter(dld_highVoltage_peak[mask] / 1000, dld_peak[mask], color="blue", label=r"$t$", s=1)

        if calibration_mode == 'tof':
            ax1.set_ylabel("Time of Flight (ns)", fontsize=10)
        elif calibration_mode == 'mc':
            ax1.set_ylabel("mc (Da)", fontsize=10)

        ax1.set_xlabel("Voltage (kV)", fontsize=10)
        plt.grid(alpha=0.3, linestyle='-.', linewidth=0.4)

        if fit_mode == 'curve_fit':
            f_bowl_plot = bowl_corr([dld_x_peak[mask], dld_y_peak[mask]], *parameters)
        elif fit_mode == 'hemisphere_fit':
            f_bowl_plot = hemisphere_corr([dld_x_peak[mask], dld_y_peak[mask]], *parameters)
        dld_t_plot = dld_peak[mask] / f_bowl_plot

        y = plt.scatter(dld_highVoltage_peak[mask] / 1000, dld_t_plot, color="red", label=r"$t_{C_{B}}$", s=1)

        plt.legend(handles=[x, y], loc='upper right', markerscale=5., prop={'size': 10})

        if save:
            # Enable rendering for text elements
            rcParams['svg.fonttype'] = 'none'
            plt.savefig(variables.result_path + "//peak_tof_bowl_corr_%s.svg" % index_fig, format="svg", dpi=600)
            plt.savefig(variables.result_path + "//peak_tof_bowl_corr_%s.png" % index_fig, format="png", dpi=600)

        if plot:
            plt.show()

        # Plot how bowl correction correct tof/mc vs dld_x position
        fig1, ax1 = plt.subplots(figsize=fig_size, constrained_layout=True)
        mask = np.random.randint(0, len(dld_highVoltage_peak), 10000)
        if fit_mode == 'curve_fit':
            f_bowl_plot = bowl_corr([dld_x_peak[mask], dld_y_peak[mask]], *parameters)
        elif fit_mode == 'hemisphere_fit':
            f_bowl_plot = hemisphere_corr([dld_x_peak[mask], dld_y_peak[mask]], *parameters)
        dld_t_plot = dld_peak[mask] / f_bowl_plot

        x = plt.scatter(dld_x_peak[mask], dld_peak[mask], color="blue", label=r"$t$", s=1)
        y = plt.scatter(dld_x_peak[mask], dld_t_plot, color="red", label=r"$t_{C_{B}}$", s=1)

        if calibration_mode == 'tof':
            ax1.set_ylabel("Time of Flight (ns)", fontsize=10)
        elif calibration_mode == 'mc':
            ax1.set_ylabel("mc (Da)", fontsize=10)

        ax1.set_xlabel(r"$X_{det}$ (mm)", fontsize=10)
        plt.grid(color='aqua', alpha=0.3, linestyle='-.', linewidth=0.4)
        plt.legend(handles=[x, y], loc='upper right', markerscale=5., prop={'size': 10})

        if save:
            # Enable rendering for text elements
            rcParams['svg.fonttype'] = 'none'
            plt.savefig(variables.result_path + "//peak_tof_bowl_corr_p_%s.svg" % index_fig, format="svg", dpi=600)
            plt.savefig(variables.result_path + "//peak_tof_bowl_corr_p_%s.png" % index_fig, format="png", dpi=600)
        if plot:
            plt.show()

        fig, ax = plt.subplots(figsize=fig_size, subplot_kw=dict(projection="3d"), constrained_layout=True)
        # Adjust the subplot parameters to make the plot smaller
        box = ax.get_position()
        ax.set_position([box.x0 + 0.1, box.y0 + 0.1, box.width * 0.75, box.height * 0.75])
        mask = np.random.randint(0, len(dld_highVoltage_peak), 500)
        if fit_mode == 'curve_fit':
            f_bowl_plot = bowl_corr([dld_x_peak[mask], dld_y_peak[mask]], *parameters)
        elif fit_mode == 'hemisphere_fit':
            f_bowl_plot = hemisphere_corr([dld_x_peak[mask], dld_y_peak[mask]], *parameters)
        dld_t_plot = dld_peak[mask] / f_bowl_plot

        scat_1 = ax.scatter(dld_x_peak[mask], dld_y_peak[mask], zs=dld_peak[mask], color="blue",
                            label=r"$t$", s=1)
        scat_2 = ax.scatter(dld_x_peak[mask], dld_y_peak[mask], zs=dld_t_plot, color="red",
                            label=r"$t_{C_{B}}$", s=1)
        plt.legend(handles=[scat_1, scat_2], loc='upper left', markerscale=5., prop={'size': 10})

        ax.set_xlabel(r'$X_{det}$ (mm)', fontsize=10, labelpad=10)
        ax.set_ylabel(r'$Y_{det}$ (mm)', fontsize=10, labelpad=10)
        ax.set_zlabel(r"$t_{C_{B}}}$", fontsize=10, labelpad=5)
        ax.view_init(elev=7, azim=-41)

        if save:
            # Enable rendering for text elements
            rcParams['svg.fonttype'] = 'none'
            plt.savefig(variables.result_path + "//peak_tof_bowl_corr_3d_%s.svg" % index_fig, format="svg", dpi=600)
            plt.savefig(variables.result_path + "//peak_tof_bowl_corr_3d_%s.png" % index_fig, format="png", dpi=600)
        if plot:
            plt.show()

    if calibration_mode == 'tof':
        variables.dld_t_calib = calibration_mc_tof
    elif calibration_mode == 'mc':
        variables.mc_calib = calibration_mc_tof

def plot_fdm(x, y, variables, save, bins_s, index_fig, figure_size=(5, 4)):
    """
    Plot the File Desorption Map (FDM) based on the given x and y data and tof vs high voltage and x_det, and y_det.

    Args:
        x (array-like): The x-coordinates of the data points.
        y (array-like): The y-coordinates of the data points.
        variables (object): The variables object.
        save (bool): Flag indicating whether to save the plot.
        bins_s (int or array-like): The number of bins or bin edges for histogram2d.
        figure_size (tuple, optional): The size of the figure in inches (width, height)
    """

    fig1, ax1 = plt.subplots(figsize=figure_size, constrained_layout=True)

    FDM, xedges, yedges = np.histogram2d(x, y, bins=bins_s)

    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    ax1.set_xlabel(r"$X_{det} (cm)$", fontsize=10)
    ax1.set_ylabel(r"$Y_{det} (cm)$", fontsize=10)

    cmap = copy(plt.cm.plasma)
    cmap.set_bad(cmap(0))
    pcm = ax1.pcolormesh(xedges, yedges, FDM.T, cmap=cmap, norm=colors.LogNorm(), rasterized=True)
    fig1.colorbar(pcm, ax=ax1, pad=0)

    if save:
        # Enable rendering for text elements
        rcParams['svg.fonttype'] = 'none'
        plt.savefig(variables.result_path + "fdm_%s.png" % index_fig, format="png", dpi=600)
        plt.savefig(variables.result_path + "fdm_%s.svg" % index_fig, format="svg", dpi=600)
    plt.show()


def initial_calibration(data, flight_path_length):
    """
    Perform the initial calibration based on the given variables and flight path length
    Args:
        data: The data frame containing the data
        flight_path_length:  The flight path length.

    Returns:
        dld_t_calib: The calibrated time-of-flight values.
    """
    v_dc = data['high_voltage (V)'].to_numpy()
    t = data['t (ns)'].to_numpy()
    xDet = data['x_det (cm)'].to_numpy() * 1E-2
    yDet = data['y_det (cm)'].to_numpy() * 1E-2
    flightPathLength = flight_path_length * 1E-3
    flightPathLength = xDet ** 2 + yDet ** 2 + flightPathLength ** 2
    ini_calib_factor_flight_path = flightPathLength / np.mean(flightPathLength)
    ini_calib_factor_voltage = np.sqrt(v_dc / np.median(v_dc))
    dld_t_calib = t * ini_calib_factor_flight_path * ini_calib_factor_voltage
    return dld_t_calib

def plot_selected_statistic(variables, bin_fdm, index_fig, calibration_mode, save, fig_size=(5, 4)):
    """
    Plot the selected statistic based on the selected peak_x.

        Args:
            variables (object): The variables object.
            bin_fdm (int or array-like): The number of bins or bin edges for histogram2d.
            index_fig (int): The index of the figure.
            calibration_mode (str): The calibration mode.
            save (bool): Flag indicating whether to save the plot.
            fig_size (tuple, optional): The size of the figure in inches (width, height)

        Return:
            None
    """
    if variables.selected_x1 == 0 or variables.selected_x2 == 0:
        print('Please first select a peak_x')
    else:
        print('Selected tof are: (%s, %s)' % (variables.selected_x1, variables.selected_x2))
        mask_temporal = np.logical_and((variables.dld_t_calib > variables.selected_x1),
                                       (variables.dld_t_calib < variables.selected_x2))
        x = variables.dld_x_det[mask_temporal]
        y = variables.dld_y_det[mask_temporal]
        dld_high_voltage = variables.dld_high_voltage[mask_temporal]
        t = variables.dld_t_calib[mask_temporal]
        bins = [bin_fdm, bin_fdm]

        plot_fdm(x, y, variables, save, bins, index_fig)

        fig1, ax1 = plt.subplots(figsize=fig_size, constrained_layout=True)
        mask = np.random.randint(0, len(x), 1000)
        plt.scatter(dld_high_voltage[mask], t[mask], color="blue", label=r"$t$", s=1)
        if calibration_mode == 'tof':
            ax1.set_ylabel("Time of Flight (ns)", fontsize=10)
            label = 'tof'
        elif calibration_mode == 'mc':
            ax1.set_ylabel("mc (Da)", fontsize=10)
            label = 'mc'
        ax1.set_ylabel(label, fontsize=10)
        ax1.set_xlabel("Voltage (V)", fontsize=10)
        plt.grid(color='aqua', alpha=0.3, linestyle='-.', linewidth=0.4)
        if save:
            # Enable rendering for text elements
            rcParams['svg.fonttype'] = 'none'
            plt.savefig(variables.result_path + "v_t_%s.png" % index_fig, format="png", dpi=600)
            plt.savefig(variables.result_path + "v_t_%s.svg" % index_fig, format="svg", dpi=600)
        plt.show()
        fig1, ax1 = plt.subplots(figsize=fig_size, constrained_layout=True)
        plt.scatter(x[mask], t[mask], color="blue", label=r"$t$", s=1)
        ax1.set_xlabel(r"$X_{det} (cm)$", fontsize=10)
        ax1.set_ylabel(label, fontsize=10)
        plt.grid(color='aqua', alpha=0.3, linestyle='-.', linewidth=0.4)
        if save:
            # Enable rendering for text elements
            rcParams['svg.fonttype'] = 'none'
            plt.savefig(variables.result_path + "x_t_%s.png" % index_fig, format="png", dpi=600)
            plt.savefig(variables.result_path + "x_t_%s.svg" % index_fig, format="svg", dpi=600)
        plt.show()
        fig1, ax1 = plt.subplots(figsize=fig_size, constrained_layout=True)
        plt.scatter(x[mask], t[mask], color="blue", label=r"$t$", s=1)
        ax1.set_xlabel(r"$Y_{det} (cm)$", fontsize=10)
        ax1.set_ylabel(label, fontsize=10)
        plt.grid(alpha=0.3, linestyle='-.', linewidth=0.4)
        if save:
            plt.savefig(variables.result_path + "y_t_%s.png" % index_fig, format="png", dpi=600)
            plt.savefig(variables.result_path + "y_t_%s.svg" % index_fig, format="svg", dpi=600)
        plt.show()
