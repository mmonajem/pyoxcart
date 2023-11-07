from copy import copy
from itertools import product

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams, colors
from scipy.optimize import curve_fit
from scipy.signal import find_peaks
from sklearn.cluster import KMeans


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
    return a + b * x + c * (x ** 2)


def voltage_correction(dld_highVoltage_peak, dld_t_peak, variables, maximum_location, index_fig, figname, sample_size,
                       mode, calibration_mode, peak_mode, num_cluster, cluster_labels, plot=True, save=False,
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
    - peak_mode (string): Type of peak_x mode (peak_x/mean/median).
    - outlier_remove (bool): Indicates whether to remove outliers. Default is True.
    - plot (bool): Indicates whether to plot the graph. Default is True.
    - save (bool): Indicates whether to save the plot. Default is False.
    - fig_size (tuple): Figure size in inches. Default is (7, 5).

    Returns:
    - fitresult (array): Corrected voltage array.

    """

    fit_result = []
    for j in range(num_cluster):
        dld_highVoltage_peak_i = dld_highVoltage_peak[cluster_labels == j]
        dld_t_peak_i = dld_t_peak[cluster_labels == j]
        high_voltage_mean_list = []
        dld_t_peak_list = []
        if mode == 'ion_seq':
            for i in range(int(len(dld_highVoltage_peak_i) / sample_size) + 1):
                dld_highVoltage_peak_selected = dld_highVoltage_peak_i[i * sample_size:(i + 1) * sample_size]
                dld_t_peak_selected = dld_t_peak_i[i * sample_size:(i + 1) * sample_size]
                if peak_mode == 'peak':
                    try:
                        bins = np.linspace(np.min(dld_t_peak_selected), np.max(dld_t_peak_selected),
                                           round(np.max(dld_t_peak_selected) / 0.1))
                        y, x = np.histogram(dld_t_peak_selected, bins=bins)
                        peaks, properties = find_peaks(y, height=0)
                        index_peak_max_ini = np.argmax(properties['peak_heights'])
                        max_peak = peaks[index_peak_max_ini]
                        dld_t_peak_list.append(x[max_peak] / maximum_location[j])

                        mask_v = np.logical_and((dld_t_peak_selected >= x[max_peak] - 0.2)
                                                , (dld_t_peak_selected <= x[max_peak] + 0.2))
                        high_voltage_mean_list.append(np.mean(dld_highVoltage_peak_selected[mask_v]))
                    except ValueError:
                        print('cannot find the maximum')
                        dld_t_mean = np.median(dld_t_peak_selected)
                        dld_t_peak_list.append(dld_t_mean / maximum_location[j])

                        high_voltage_mean = np.mean(dld_highVoltage_peak_selected)
                        high_voltage_mean_list.append(high_voltage_mean)
                elif peak_mode == 'mean':
                    dld_t_mean = np.mean(dld_t_peak_selected)
                    dld_t_peak_list.append(dld_t_mean / maximum_location[j])
                    high_voltage_mean = np.mean(dld_highVoltage_peak_selected)
                    high_voltage_mean_list.append(high_voltage_mean)
                elif peak_mode == 'median':
                    dld_t_mean = np.median(dld_t_peak_selected)
                    dld_t_peak_list.append(dld_t_mean / maximum_location[j])
                    high_voltage_mean = np.median(dld_highVoltage_peak_selected)
                    high_voltage_mean_list.append(high_voltage_mean)

        elif mode == 'voltage':
            for i in range(int((np.max(dld_highVoltage_peak_i) - np.min(dld_highVoltage_peak_i)) / sample_size) + 1):
                mask = np.logical_and((dld_highVoltage_peak_i >= (np.min(dld_highVoltage_peak_i) + (i) * sample_size)),
                                      (dld_highVoltage_peak_i < (np.min(dld_highVoltage_peak_i) + (i + 1) * sample_size)))
                dld_highVoltage_peak_selected = dld_highVoltage_peak_i[mask]
                dld_t_peak_selected = dld_t_peak_i[mask]

                bins = np.linspace(np.min(dld_t_peak_selected), np.max(dld_t_peak_selected),
                                   round(np.max(dld_t_peak_selected) / 0.1))
                y, x = np.histogram(dld_t_peak_selected, bins=bins)
                if peak_mode == 'peak':
                    try:
                        peaks, properties = find_peaks(y, height=0)
                        index_peak_max_ini = np.argmax(properties['peak_heights'])
                        max_peak = peaks[index_peak_max_ini]
                        dld_t_peak_list.append(x[max_peak] / maximum_location[j])

                        mask_v = np.logical_and((dld_t_peak_selected >= x[max_peak] - 0.2)
                                                , (dld_t_peak_selected <= x[max_peak] + 0.2))
                        high_voltage_mean_list.append(np.mean(dld_highVoltage_peak_selected[mask_v]))
                    except:
                        print('cannot find the maximum')
                        dld_t_mean = np.median(dld_t_peak_selected)
                        dld_t_peak_list.append(dld_t_mean / maximum_location[j])

                        high_voltage_mean = np.mean(dld_highVoltage_peak_selected)
                        high_voltage_mean_list.append(high_voltage_mean)
                elif peak_mode == 'mean':
                    dld_t_mean = np.mean(dld_t_peak_selected)
                    dld_t_peak_list.append(dld_t_mean / maximum_location[j])

                    high_voltage_mean = np.mean(dld_highVoltage_peak_selected)
                    high_voltage_mean_list.append(high_voltage_mean)
                elif peak_mode == 'median':
                    dld_t_mean = np.median(dld_t_peak_selected)
                    dld_t_peak_list.append(dld_t_mean / maximum_location[j])

                    high_voltage_mean = np.median(dld_highVoltage_peak_selected)
                    high_voltage_mean_list.append(high_voltage_mean)

        fitresult, _ = curve_fit(voltage_corr, np.array(high_voltage_mean_list), np.array(dld_t_peak_list))

        fit_result.append(fitresult)
        if plot or save:
            fig1, ax1 = plt.subplots(figsize=fig_size, constrained_layout=True)
            if calibration_mode == 'tof':
                ax1.set_ylabel("Time of Flight (ns)", fontsize=10)
                label = 't'
            elif calibration_mode == 'mc':
                ax1.set_ylabel("mc (Da)", fontsize=10)
                label = 'mc'

            x = plt.scatter(np.array(high_voltage_mean_list) / 1000, np.array(dld_t_peak_list) * maximum_location[j],
                            color="blue", label=label, s=1)
            ax1.set_xlabel("Voltage (kV)", fontsize=10)
            plt.grid(alpha=0.3, linestyle='-.', linewidth=0.4)

            ax2 = ax1.twinx()
            f_v = voltage_corr(np.array(high_voltage_mean_list), *fitresult)
            y = ax2.plot(np.array(high_voltage_mean_list) / 1000, f_v, color='r', label=r"$C_V$", linewidth=0.5)
            ax2.set_ylabel(r"$C_V$", color="red", fontsize=10)
            plt.legend(handles=[x, y[0]], loc='lower left', markerscale=5., prop={'size': 6})

            if save:
                # Enable rendering for text elements
                rcParams['svg.fonttype'] = 'none'
                plt.savefig(variables.result_path + "//vol_corr_%s_%s.svg" % (figname, index_fig), format="svg", dpi=600)
                plt.savefig(variables.result_path + "//vol_corr_%s_%s.png" % (figname, index_fig), format="png", dpi=600)

            if plot:
                plt.show()

    return fit_result


def voltage_corr_main(dld_highVoltage, variables, sample_size, mode, calibration_mode, peak_mode, index_fig, plot, save,
                      apply_local='all', num_cluster=2, maximum_cal_method='histogram', fig_size=(5, 5)):
    """
    Perform voltage correction on the given data.

    Args:
        dld_highVoltage (numpy.ndarray): Array of high voltages.
        sample_size (int): Size of the sample.
        mode (str): Mode of the correction.
        calibration_mode (str): Calibration mode ('tof' or 'mc').
        peak_mode (str): Peak mode.
        index_fig (int): Index of the figure.
        plot (bool): Whether to plot the results.
        save (bool): Whether to save the plots.
        apply_local (str, optional): Whether to apply local correction ('all', voltage', or 'voltage_temporal').
        num_cluster (int, optional): Number of clusters. Defaults to 2.
        maximum_cal_method (str, optional): Maximum calculation method ('histogram' or 'mean').
            Defaults to 'histogram'.
        fig_size (tuple, optional): Size of the figure. Defaults to (5, 5).
    """
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

    print(len(dld_highVoltage), len(mask_temporal))
    dld_highVoltage_peak_v = dld_highVoltage[mask_temporal]

    if num_cluster > 1:
        cluster_labels, hv_range = cluster_tof(dld_highVoltage_peak_v, dld_peak_b, calibration_mode, num_cluster,
                                               plot=plot, fig_size=fig_size)
    else:
        cluster_labels = np.zeros(len(dld_peak_b))
        hv_range = [[np.min(dld_highVoltage_peak_v), np.max(dld_highVoltage_peak_v)]]

    print('The number of ions is:', len(dld_highVoltage_peak_v))
    print('The number of samples is:', int(len(dld_highVoltage_peak_v) / sample_size))
    print('The number of clusters is:', len(hv_range))
    maximum_location = []
    for i in range(len(hv_range)):
        mask_range = np.logical_and(
            (dld_highVoltage_peak_v >= hv_range[i][0]),
            (dld_highVoltage_peak_v <= hv_range[i][1])
        )
        if maximum_cal_method == 'histogram':
            bins = np.linspace(np.min(dld_peak_b[mask_range]), np.max(dld_peak_b[mask_range]),
                               round(np.max(dld_peak_b[mask_range]) / 0.1))
            y, x = np.histogram(dld_peak_b[mask_range], bins=bins)
            peaks, properties = find_peaks(y, height=0)
            index_peak_max_ini = np.argmax(properties['peak_heights'])
            max_peak = peaks[index_peak_max_ini]
            maximum_location_i = x[max_peak]
        elif maximum_cal_method == 'mean':
            maximum_location_i = np.mean(dld_peak_b[mask_range])
        maximum_location.append(maximum_location_i)

    print('The maximum of histogram is located at:', maximum_location)

    fitresult = voltage_correction(dld_highVoltage_peak_v, dld_peak_b, variables,
                                   maximum_location, index_fig=index_fig,
                                   figname='voltage_corr',
                                   sample_size=sample_size, mode=mode, calibration_mode=calibration_mode,
                                   peak_mode=peak_mode, num_cluster=len(hv_range), cluster_labels=cluster_labels,
                                   plot=plot, save=save, fig_size=fig_size)
    print('The fit result are:', fitresult)
    print('high voltage ranges are:', hv_range)

    f_v_list_plot = []
    calibration_mc_tof = np.copy(variables.dld_t_calib) if calibration_mode == 'tof' else np.copy(variables.mc_calib)

    for i in range(len(hv_range)):
        dld_highVoltage_range = dld_highVoltage_peak_v[cluster_labels == i]
        dld_t_range = dld_peak_b[cluster_labels == i]

        print('The fit result [%s] is:' % i, fitresult[i])
        mask_range = np.logical_and(
            (dld_highVoltage > hv_range[i][0]),
            (dld_highVoltage < hv_range[i][1])
        )
        if apply_local == 'voltage_temporal':
            mask_fv = np.logical_and(mask_range, mask_temporal)
        elif apply_local == 'voltage':
            mask_fv = mask_temporal
        elif apply_local == 'all':
            mask_fv = np.ones_like(dld_highVoltage, dtype=bool)

        f_v = voltage_corr(dld_highVoltage[mask_fv], *fitresult[i])

        calibration_mc_tof[mask_fv] = calibration_mc_tof[mask_fv] / f_v

        if plot or save:
            # Plot how correction factor for selected peak_x
            fig1, ax1 = plt.subplots(figsize=fig_size, constrained_layout=True)
            if len(dld_highVoltage_range) > 1000:
                mask = np.random.randint(0, len(dld_highVoltage_range), 1000)
            else:
                mask = np.arange(len(dld_highVoltage_range))
            x = plt.scatter(dld_highVoltage_range[mask] / 1000, dld_t_range[mask], color="blue", label=r"$t$", s=1)

            if calibration_mode == 'tof':
                ax1.set_ylabel("Time of Flight (ns)", fontsize=10)
            elif calibration_mode == 'mc':
                ax1.set_ylabel("mc (Da)", fontsize=10)
            ax1.set_xlabel("Voltage (V)", fontsize=10)
            plt.grid(alpha=0.3, linestyle='-.', linewidth=0.4)

            # Plot high voltage curve
            ax2 = ax1.twinx()
            f_v_plot = voltage_corr(dld_highVoltage_range, *fitresult[i])
            f_v_list_plot.append(f_v_plot)

            y = ax2.plot(dld_highVoltage_range / 1000, 1 / f_v_plot, color='r', label=r"$C_{V}^{-1}$")
            ax2.set_ylabel(r"$C_{V}^{-1}$", color="red", fontsize=10)
            plt.legend(handles=[x, y[0]], loc='upper left', markerscale=5., prop={'size': 10})

            if save:
                # Enable rendering for text elements
                rcParams['svg.fonttype'] = 'none'
                plt.savefig(variables.result_path + "//vol_corr_%s.eps" % index_fig, format="svg", dpi=600)
                plt.savefig(variables.result_path + "//vol_corr_%s.png" % index_fig, format="png", dpi=600)
            plt.show()

            # Plot corrected tof/mc vs. uncalibrated tof/mc
            fig1, ax1 = plt.subplots(figsize=fig_size, constrained_layout=True)
            x = plt.scatter(dld_highVoltage_range[mask] / 1000, dld_t_range[mask], color="blue", label='t', s=1)
            if calibration_mode == 'tof':
                ax1.set_ylabel("Time of Flight (ns)", fontsize=10)
            elif calibration_mode == 'mc':
                ax1.set_ylabel("mc (Da)", fontsize=10)
            ax1.set_xlabel("Voltage (kV)", fontsize=10)
            plt.grid(alpha=0.3, linestyle='-.', linewidth=0.4)

            dld_t_plot = dld_t_range * (1 / f_v_plot)

            y = plt.scatter(dld_highVoltage_range[mask] / 1000, dld_t_plot[mask], color="red", label=r"$t_{C_{V}}$",
                            s=1)

            plt.legend(handles=[x, y], loc='upper right', markerscale=5., prop={'size': 10})

            if save:
                # Enable rendering for text elements
                rcParams['svg.fonttype'] = 'none'
                plt.savefig(variables.result_path + "//peak_tof_V_corr_%s.svg" % index_fig, format="svg", dpi=600)
                plt.savefig(variables.result_path + "//peak_tof_V_corr_%s.png" % index_fig, format="png", dpi=600)
            if plot:
                plt.show()

    if plot or save:
        # Plot corrected tof/mc vs. uncalibrated tof/mc
        fig1, ax1 = plt.subplots(figsize=fig_size, constrained_layout=True)
        mask = np.random.randint(0, len(dld_highVoltage_peak_v), 1000)
        x = plt.scatter(dld_highVoltage_peak_v[mask] / 1000, dld_peak_b[mask], color="blue", label='t', s=1)
        if calibration_mode == 'tof':
            ax1.set_ylabel("Time of Flight (ns)", fontsize=10)
        elif calibration_mode == 'mc':
            ax1.set_ylabel("mc (Da)", fontsize=10)
        ax1.set_xlabel("Voltage (kV)", fontsize=10)
        plt.grid(alpha=0.3, linestyle='-.', linewidth=0.4)

        dld_t_plot = np.copy(dld_peak_b)
        for i in range(len(hv_range)):
            dld_t_plot[cluster_labels == i] = dld_peak_b[cluster_labels == i] * (1 / f_v_list_plot[i])

        y = plt.scatter(dld_highVoltage_peak_v[mask] / 1000, dld_t_plot[mask], color="red", label=r"$t_{C_{V}}$", s=1)

        plt.legend(handles=[x, y], loc='upper right', markerscale=5., prop={'size': 10})

        if save:
            # Enable rendering for text elements
            rcParams['svg.fonttype'] = 'none'
            plt.savefig(variables.result_path + "//peak_tof_V_corr_%s.svg" % index_fig, format="svg", dpi=600)
            plt.savefig(variables.result_path + "//peak_tof_V_corr_%s.png" % index_fig, format="png", dpi=600)

        if plot:
            plt.show()

    variables.dld_t_calib = calibration_mc_tof

def bowl_corr_fit(data_xy, a, b, c, d, e, f):
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


def bowl_correction(dld_x_bowl, dld_y_bowl, dld_t_bowl, variables, det_diam, maximum_location, sample_size,
                    index_fig, plot, save, fig_size=(7, 5)):
    """
    Perform bowl correction on the input data.

    Args:
        dld_x_bowl (numpy.ndarray): X coordinates of the data points.
        dld_y_bowl (numpy.ndarray): Y coordinates of the data points.
        dld_t_bowl (numpy.ndarray): Time values of the data points.
        det_diam (float): Diameter of the detector.
        maximum_location (float): Maximum location for normalization.
        sample_size (int): Size of each sample.
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

    w1 = -int(det_diam)
    w2 = int(det_diam)
    h1 = w1
    h2 = w2


    d = sample_size  # sample size is in mm - so we change it to cm
    grid = product(range(h1, h2 - h2 % d, d), range(w1, w2 - w2 % d, d))
    x_y = np.vstack((dld_x_bowl, dld_y_bowl)).T

    for i, j in grid:
        # box = (j, i, j + d, i + d)   # box = (left, upper, right, lower)
        mask_x = np.logical_and((dld_x_bowl < j + d), (dld_x_bowl > j))
        mask_y = np.logical_and((dld_y_bowl < i + d), (dld_y_bowl > i))
        mask = np.logical_and(mask_x, mask_y)
        if len(mask[mask]) > 0:
            x_y_selected = x_y[mask]
            x_sample_list.append(np.median(x_y_selected[:, 0]))
            y_sample_list.append(np.median(x_y_selected[:, 1]))
            dld_t_peak_list.append(np.mean(dld_t_bowl[mask]) / maximum_location)

    parameters, covariance = curve_fit(bowl_corr_fit, [np.array(x_sample_list), np.array(y_sample_list)],
                                       np.array(dld_t_peak_list))

    if plot or save:
        model_x_data = np.linspace(-35, 35, 30)
        model_y_data = np.linspace(-35, 35, 30)
        X, Y = np.meshgrid(model_x_data, model_y_data)
        Z = bowl_corr_fit(np.array([X, Y]), *parameters)

        fig, ax = plt.subplots(figsize=fig_size, subplot_kw=dict(projection="3d"), constrained_layout=True)
        fig.add_axes(ax)
        cmap = copy(plt.cm.plasma)
        cmap.set_bad(cmap(0))
        ax.plot_surface(X, Y, 1 / Z, cmap=cmap)
        ax.set_xlabel('X_det (mm)', fontsize=10, labelpad=10)
        ax.set_ylabel('Y_det (mm)', fontsize=10, labelpad=10)
        ax.set_zlabel(r"${C_B}^{-1}$", fontsize=10, labelpad=5)
        ax.zaxis.set_major_formatter(plt.FormatStrFormatter('%.2f'))
        ax.view_init(elev=7, azim=-41)

        if save:
            # Enable rendering for text elements
            rcParams['svg.fonttype'] = 'none'
            plt.savefig(variables.result_path + "//bowl_corr_%s.svg" % index_fig, format="svg", dpi=600)
            plt.savefig(variables.result_path + "//bowl_corr_%s.png" % index_fig, format="png", dpi=600)
        if plot:
            plt.show()

    return parameters


def bowl_correction_main(dld_x, dld_y, dld_highVoltage, variables, det_diam, sample_size, calibration_mode, index_fig,
                         plot, save, apply_local='all',
                         maximum_cal_method='mean', fig_size=(5, 5)):
    """
    Perform bowl correction on the input data and plot the results.

    Args:
        dld_x (numpy.ndarray): X positions.
        dld_y (numpy.ndarray): Y positions.
        dld_highVoltage (numpy.ndarray): High voltage values.
        det_diam (float): Detector diameter.
        sample_size (int): Sample size.
        calibration_mode (str): Calibration mode ('tof' or 'mc').
        index_fig (int): Index figure.
        plot (bool): Flag indicating whether to plot the results.
        save (bool): Flag indicating whether to save the plots.
        apply_local (str, optional): Apply bowl correction locally ('all', 'temporal').
        maximum_cal_method (str, optional): Maximum calculation method ('mean' or 'histogram').
        fig_size (tuple, optional): Figure size.

    Returns:
        None

    """

    dld_x = dld_x * 10 # change the x position to mm from cm
    dld_y = dld_y * 10 # change the y position to mm from cm

    if calibration_mode == 'tof':
        mask_temporal = np.logical_and((variables.dld_t_calib > variables.selected_x1),
                                       (variables.dld_t_calib < variables.selected_x2))
    elif calibration_mode == 'mc':
        mask_temporal = np.logical_and((variables.mc_calib > variables.selected_x1),
                                       (variables.mc_calib < variables.selected_x2))

    dld_peak = variables.dld_t_calib[mask_temporal] if calibration_mode == 'tof' else variables.mc_calib[mask_temporal]
    print('The number of ions is:', len(dld_peak))

    # mask_1 = np.logical_and((dld_x[mask_temporal] > -8), (dld_x[mask_temporal] < 8))
    # mask_2 = np.logical_and((dld_y[mask_temporal] > -8), (dld_y[mask_temporal] < 8))
    # mask = np.logical_and(mask_1, mask_2)
    # dld_peak_mid = dld_peak[mask]
    dld_peak_mid = dld_peak
    if maximum_cal_method == 'histogram':
        try:
            bins = np.linspace(np.min(dld_peak_mid), np.max(dld_peak_mid), round(np.max(dld_peak_mid) / 0.1))
            y, x = np.histogram(dld_peak_mid, bins=bins)
            peaks, properties = find_peaks(y, height=0)
            index_peak_max_ini = np.argmax(properties['peak_heights'])
            maximum_location = x[peaks[index_peak_max_ini]]
        except:
            print('The histogram max calculation method failed, using mean instead.')
            maximum_location = np.mean(dld_peak_mid)
    elif maximum_cal_method == 'mean':
        maximum_location = np.mean(dld_peak_mid)
    print('The maximum of histogram is located at:', maximum_location)

    dld_x_peak = dld_x[mask_temporal]
    dld_y_peak = dld_y[mask_temporal]
    dld_highVoltage_peak = dld_highVoltage[mask_temporal]

    parameters = bowl_correction(dld_x_peak, dld_y_peak, dld_peak, variables, det_diam, maximum_location,
                                 sample_size=sample_size, index_fig=index_fig, plot=plot, save=save, fig_size=fig_size)
    print('The fit result is:', parameters)

    if apply_local == 'all':
        mask_fv = np.ones_like(dld_x, dtype=bool)
    elif apply_local == 'temporal':
        mask_fv = mask_temporal

    f_bowl = bowl_corr_fit([dld_x[mask_fv], dld_y[mask_fv]], *parameters)

    calibration_mc_tof = np.copy(variables.dld_t_calib) if calibration_mode == 'tof' else np.copy(variables.mc_calib)

    calibration_mc_tof[mask_fv] = calibration_mc_tof[mask_fv] / f_bowl

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

        f_bowl_plot = bowl_corr_fit([dld_x_peak[mask], dld_y_peak[mask]], *parameters)
        dld_t_plot = dld_peak[mask] / f_bowl_plot

        y = plt.scatter(dld_highVoltage_peak[mask] / 1000, dld_t_plot, color="red", label=r"$t_{C_{B}}$", s=1)

        plt.legend(handles=[x, y], loc='upper right', markerscale=5., prop={'size': 10})

        if save:
            # Enable rendering for text elements
            rcParams['svg.fonttype'] = 'none'
            plt.savefig(variables.result_path + "//peak_tof_bowl_corr_%s.svg" % index_fig, format="svg", dpi=600)
            plt.savefig(variables.result_path + "//peak_tof_bowl_corr_%s.png" % index_fig, format="png", dpi=600)

        plt.show()

        # Plot how bowl correction correct tof/mc vs dld_x position
        fig1, ax1 = plt.subplots(figsize=fig_size, constrained_layout=True)
        mask = np.random.randint(0, len(dld_highVoltage_peak), 10000)

        f_bowl_plot = bowl_corr_fit([dld_x_peak[mask], dld_y_peak[mask]], *parameters)
        dld_t_plot = dld_peak[mask] / f_bowl_plot

        x = plt.scatter(dld_x_peak[mask], dld_peak[mask], color="blue", label=r"$t$", s=1)
        y = plt.scatter(dld_x_peak[mask], dld_t_plot, color="red", label=r"$t_{C_{B}}$", s=1)

        if calibration_mode == 'tof':
            ax1.set_ylabel("Time of Flight (ns)", fontsize=10)
        elif calibration_mode == 'mc':
            ax1.set_ylabel("mc (Da)", fontsize=10)

        ax1.set_xlabel("X_det(mm)", fontsize=10)
        plt.grid(color='aqua', alpha=0.3, linestyle='-.', linewidth=0.4)
        plt.legend(handles=[x, y], loc='upper right', markerscale=5., prop={'size': 10})

        if save:
            # Enable rendering for text elements
            rcParams['svg.fonttype'] = 'none'
            plt.savefig(variables.result_path + "//peak_tof_bowl_corr_p_%s.svg" % index_fig, format="svg", dpi=600)
            plt.savefig(variables.result_path + "//peak_tof_bowl_corr_p_%s.png" % index_fig, format="png", dpi=600)
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
