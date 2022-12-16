import numpy as np
import math
from itertools import product
from sklearn.preprocessing import MinMaxScaler
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.signal import find_peaks

# Local module and scripts
from pyccapt.calibration.calibration_tools import variables


def voltage_corr(x, a, b, c, d):
    #     return a / np.sqrt((b + (c * x) + (d * (x**2))))
    #     return a / (b * (x ** 2) + c * x + d)
    return a + (b * (x ** 2) + (c * x) + d)


def voltage_correction(dld_highVoltage_peak, dld_t_peak, index_fig, figname, sample_size, mode, plot=True, save=False):
    high_voltage_mean_list = []
    dld_t_peak_list = []

    if mode == 'ion_seq':
        for i in range(int(len(dld_highVoltage_peak) / sample_size) + 1):
            dld_highVoltage_peak_selected = dld_highVoltage_peak[(i) * sample_size:(i + 1) * sample_size]
            dld_t_peak_selected = dld_t_peak[(i) * sample_size:(i + 1) * sample_size]

            high_voltage_mean = np.mean(dld_highVoltage_peak_selected)
            high_voltage_mean_list.append(high_voltage_mean)

            bins = np.linspace(np.min(dld_t_peak_selected), np.max(dld_t_peak_selected),
                               round(np.max(dld_t_peak_selected) / 0.1))
            y, x = np.histogram(dld_t_peak_selected, bins=bins)
            peaks, properties = find_peaks(y)
            index_max_ini = np.argmax(peaks)
            max_peak = peaks[index_max_ini]
            dld_t_peak_list.append(x[max_peak])

    #             dld_t_mean = np.median(dld_t_peak_selected)
    #             dld_t_peak_list.append(dld_t_mean)

    elif mode == 'voltage':
        for i in range(int((np.max(dld_highVoltage_peak) - np.min(dld_highVoltage_peak)) / sample_size) + 1):
            mask = np.logical_and((dld_highVoltage_peak >= (np.min(dld_highVoltage_peak) + (i) * sample_size)),
                                  (dld_highVoltage_peak < (np.min(dld_highVoltage_peak) + (i + 1) * sample_size)))
            dld_highVoltage_peak_selected = dld_highVoltage_peak[mask]
            dld_t_peak_selected = dld_t_peak[mask]

            high_voltage_mean = np.mean(dld_highVoltage_peak_selected)
            high_voltage_mean_list.append(high_voltage_mean)

            dld_t_mean = np.median(dld_t_peak_selected)
            dld_t_peak_list.append(dld_t_mean)

    fitresult, _ = curve_fit(voltage_corr, np.array(high_voltage_mean_list), np.array(dld_t_peak_list))
    #     fitresult, _ = curve_fit(voltage_corr, np.array(high_voltage_mean_list), np.array(dld_t_peak_list), bounds=(0, 3), max_nfev=30)

    if plot:
        # plot fitted curve
        fig1, ax1 = plt.subplots(figsize=(8, 4))
        mask = np.random.randint(0, len(high_voltage_mean_list), 1000)
        x = plt.scatter(np.array(high_voltage_mean_list)[mask], np.array(dld_t_peak_list)[mask], color="blue",
                        label='t', alpha=0.1)
        ax1.set_ylabel("Time of flight (ns)", color="red", fontsize=10)
        ax1.set_xlabel("Voltage (V)", color="red", fontsize=10)
        plt.grid(color='aqua', alpha=0.3, linestyle='-.', linewidth=2)

        # plot high voltage curve
        ax2 = ax1.twinx()
        f_v = voltage_corr(np.array(high_voltage_mean_list), *fitresult)
        y = ax2.plot(np.array(high_voltage_mean_list), (f_v / f_v[0]), color='r', label=r"$F_V$")
        ax2.set_ylabel(r"$F_V$", color="red", fontsize=10)
        plt.legend(handles=[x, y[0]], loc='upper right')

        if save:
            plt.savefig(variables.result_path + "//vol_corr_%s_%s.svg" % (figname, index_fig), format="svg", dpi=600)
            plt.savefig(variables.result_path + "//vol_corr_%s_%s.png" % (figname, index_fig), format="png", dpi=600)

        plt.show()

    return fitresult


def voltage_corr_main(dld_highVoltage, sample_size, mode, calibration_mode, index_fig, plot, save):

    if calibration_mode == 'tof':
        mask_temporal = np.logical_and((variables.dld_t_calib > variables.selected_x1),
                                       (variables.dld_t_calib < variables.selected_x2))
        dld_t_peak_v = variables.dld_t_calib[mask_temporal]
    elif calibration_mode == 'mc':
        mask_temporal = np.logical_and((variables.mc_calib > variables.selected_x1),
                                       (variables.mc_calib < variables.selected_x2))
        dld_t_peak_v = variables.mc_calib[mask_temporal]


    dld_highVoltage_peak_v = dld_highVoltage[mask_temporal]
    print('The number of ions are:', len(dld_highVoltage_peak_v))
    print('The number of samples are:', int(len(dld_highVoltage_peak_v) / sample_size))
    fitresult = voltage_correction(dld_highVoltage_peak_v, dld_t_peak_v, index_fig=index_fig, figname='voltage_corr',
                                   sample_size=sample_size, mode=mode, plot=plot, save=save)

    f_v = voltage_corr(dld_highVoltage, *fitresult)

    if calibration_mode == 'tof':
        variables.dld_t_calib = variables.dld_t_calib * (1 / (f_v / f_v[0]))
    elif calibration_mode == 'mc':
        variables.mc_calib = variables.mc_calib * (1 / (f_v / f_v[0]))


    if plot:
        # plot how correction factor for selected peak
        fig1, ax1 = plt.subplots(figsize=(8, 4))

        # f_v = tof_calibration.voltage_corr(dld_highVoltage_peak_v, *fitresult)
        mask = np.random.randint(0, len(dld_highVoltage_peak_v), 1000)
        x = plt.scatter(dld_highVoltage_peak_v[mask], dld_t_peak_v[mask], color="blue", label='t', alpha=0.1)

        ax1.set_ylabel("Time of flight (ns)", color="red", fontsize=10)
        ax1.set_xlabel("Voltage (V)", color="red", fontsize=10)
        plt.grid(color='aqua', alpha=0.3, linestyle='-.', linewidth=2)

        # plot high voltage curve
        ax2 = ax1.twinx()
        f_v = voltage_corr(dld_highVoltage_peak_v, *fitresult)
        y = ax2.plot(dld_highVoltage_peak_v, 1 / (f_v / f_v[0]), color='r', label=r"$F_V$")
        ax2.set_ylabel(r"$F_V$", color="red", fontsize=10)

        plt.legend(handles=[x, y[0]], loc='upper right')

        if save:
            plt.savefig(variables.result_path + "//vol_corr_%s.svg" % index_fig, format="svg", dpi=600)
            plt.savefig(variables.result_path + "//vol_corr_%s.png" % index_fig, format="png", dpi=600)

        plt.show()
        # plot corrected tof.mc vs un calibrated tof/mc
        fig1, ax1 = plt.subplots(figsize=(8, 4))
        mask = np.random.randint(0, len(dld_highVoltage_peak_v), 10000)

        x = plt.scatter(dld_highVoltage_peak_v[mask], dld_t_peak_v[mask], color="blue", label='t', alpha=0.1)
        ax1.set_ylabel("Time of flight (ns)", color="red", fontsize=10)
        ax1.set_xlabel("Voltage (V)", color="red", fontsize=10)
        plt.grid(color='aqua', alpha=0.3, linestyle='-.', linewidth=2)

        f_v_plot = voltage_corr(dld_highVoltage_peak_v[mask], *fitresult)

        dld_t_plot = dld_t_peak_v[mask] * (1 / (f_v_plot / f_v_plot[0]))

        y = plt.scatter(dld_highVoltage_peak_v[mask], dld_t_plot, color="red", label=r"$t_V$", alpha=0.1)

        plt.legend(handles=[x, y], loc='upper right')
        if save:
            plt.savefig(variables.result_path + "//peak_tof_V_corr_%s.svg" % index_fig, format="svg", dpi=600)
            plt.savefig(variables.result_path + "//peak_tof_V_corr_%s.png" % index_fig, format="png", dpi=600)
        plt.show()


def bowl_corr_fit(data_xy, a, b, c, d, e, f):
    x = data_xy[0]
    y = data_xy[1]
    result = (a + b * x + c * y + d * (x ** 2) + e * x * y + f * (y ** 2))
    return result


def bowl_correction(dld_x_bowl, dld_y_bowl, dld_t_bowl, sample_size, index_fig, plot, save):
    x_sample_list = []
    y_sample_list = []
    dld_t_peak_list = []

    w1 = math.floor(np.min(dld_x_bowl))
    w2 = math.ceil(np.max(dld_x_bowl))
    h1 = math.floor(np.min(dld_y_bowl))
    h2 = math.ceil(np.max(dld_y_bowl))

    d = sample_size
    grid = product(range(h1, h2 - h2 % d, d), range(w1, w2 - w2 % d, d))
    x_y = np.vstack((dld_x_bowl, dld_y_bowl)).T

    for i, j in grid:
        box = (j, i, j + d, i + d)
        mask_x = np.logical_and((dld_x_bowl < j + d), (dld_x_bowl > j))
        mask_y = np.logical_and((dld_y_bowl < i + d), (dld_y_bowl > i))
        mask = np.logical_and(mask_x, mask_y)
        if len(mask[mask == True]) > 0:
            x_y_slected = x_y[mask]
            x_sample_list.append(np.median(x_y_slected[:, 0]))
            y_sample_list.append(np.median(x_y_slected[:, 1]))
            dld_t_peak_list.append(np.mean(dld_t_bowl[mask]) / variables.max_peak)

    parameters, covariance = curve_fit(bowl_corr_fit, [np.array(x_sample_list), np.array(y_sample_list)],
                                       np.array(dld_t_peak_list))

    if plot:
        # create surface function model
        # setup data points for calculating surface model
        model_x_data = np.linspace(-35, 35, 30)
        model_y_data = np.linspace(-35, 35, 30)
        # create coordinate arrays for vectorized evaluations
        X, Y = np.meshgrid(model_x_data, model_y_data)
        # calculate Z coordinate array
        Z = bowl_corr_fit(np.array([X, Y]), *parameters)

        # setup figure object
        fig = plt.figure()
        # setup 3d object
        ax = Axes3D(fig, auto_add_to_figure=False)
        fig.add_axes(ax)
        # plot surface
        ax.plot_surface(X, Y, Z)
        # plot input data
        # ax.scatter(detxIn, detyIn, mcIn, color='red')
        # set plot descriptions
        ax.set_xlabel('X', color="red", fontsize=10)
        ax.set_ylabel('Y', color="red", fontsize=10)
        ax.set_zlabel(r"$F_B$", color="red", fontsize=10)
        ax.tick_params(axis='both', which='major', labelsize=8)
        # ax.tick_params(axis='both', which='minor', labelsize=8)

        if save:
            plt.savefig(variables.result_path + "//bowl_corr_%s.svg" % index_fig, format="svg", dpi=600)
            plt.savefig(variables.result_path + "//bowl_corr_%s.png" % index_fig, format="png", dpi=600)

        plt.show()
    return parameters


def bowl_correction_main(dld_x, dld_y, dld_highVoltage, sample_size, calibration_mode, index_fig, plot, save):
    if calibration_mode == 'tof':
        mask_temporal = np.logical_and((variables.dld_t_calib > variables.selected_x1),
                                       (variables.dld_t_calib < variables.selected_x2))
        dld_t_peak_b = variables.dld_t_calib[mask_temporal]
        print('The number of ions are:', len(variables.dld_t_calib))
    elif calibration_mode == 'mc':
        mask_temporal = np.logical_and((variables.mc_calib > variables.selected_x1),
                                       (variables.mc_calib < variables.selected_x2))
        dld_t_peak_b = variables.mc_calib[mask_temporal]
        print('The number of ions are:', len(variables.mc_calib))



    dld_x_peak_b = dld_x[mask_temporal]
    dld_y_peak_b = dld_y[mask_temporal]
    dld_highVoltage_peak_b = dld_highVoltage[mask_temporal]

    parameters = bowl_correction(dld_x_peak_b, dld_y_peak_b, dld_t_peak_b, sample_size=sample_size, index_fig=index_fig,
                                 plot=plot, save=save)

    f_bowl = bowl_corr_fit([dld_x, dld_y], *parameters)
    if calibration_mode == 'tof':
        variables.dld_t_calib = variables.dld_t_calib * 1 / f_bowl
    elif calibration_mode == 'mc':
        variables.mc_calib = variables.mc_calib * 1 / f_bowl
    if plot:
        # plot how bowl correct tof/mc vs high voltage
        fig1, ax1 = plt.subplots(figsize=(8, 4))

        mask = np.random.randint(0, len(dld_highVoltage_peak_b), 10000)

        x = plt.scatter(dld_highVoltage_peak_b[mask], dld_t_peak_b[mask], color="blue", label=r"$t_V$", alpha=0.1)
        ax1.set_ylabel("Time of flight (ns)", color="red", fontsize=10)
        ax1.set_xlabel("Voltage (V)", color="red", fontsize=10)
        plt.grid(color='aqua', alpha=0.3, linestyle='-.', linewidth=2)

        f_bowl_plot = bowl_corr_fit([dld_x_peak_b[mask], dld_y_peak_b[mask]], *parameters)
        dld_t_plot = dld_t_peak_b[mask] * 1 / (f_bowl_plot)

        y = plt.scatter(dld_highVoltage_peak_b[mask], dld_t_plot, color="red", label=r"$t_B$", alpha=0.1)

        plt.legend(handles=[x, y], loc='upper right')

        if save:
            plt.savefig(variables.result_path + "//peak_tof_bowl_corr_%s.svg" % index_fig, format="svg", dpi=600)
            plt.savefig(variables.result_path + "//peak_tof_bowl_corr_%s.png" % index_fig, format="png", dpi=600)
        plt.show()
        # plot how bowl correction correct tof/mc vs dld_x position
        fig1, ax1 = plt.subplots(figsize=(8, 4))

        mask = np.random.randint(0, len(dld_highVoltage_peak_b), 10000)

        f_bowl_plot = bowl_corr_fit([dld_x_peak_b[mask], dld_y_peak_b[mask]], *parameters)
        dld_t_plot = dld_t_peak_b[mask] * 1 / f_bowl_plot

        x = plt.scatter(dld_x_peak_b[mask], dld_t_peak_b[mask], color="blue", label='X', alpha=0.1)
        y = plt.scatter(dld_x_peak_b[mask], dld_t_plot, color="red", label='X_corr', alpha=0.1)
        ax1.set_ylabel("Time of flight (ns)", color="red", fontsize=10)
        ax1.set_xlabel("position (mm)", color="red", fontsize=10)
        plt.grid(color='aqua', alpha=0.3, linestyle='-.', linewidth=2)
        plt.legend(handles=[x, y], loc='upper right')
        if save:
            plt.savefig(variables.result_path + "//peak_tof_bowl_corr_p_%s.svg" % index_fig, format="svg", dpi=600)
            plt.savefig(variables.result_path + "//peak_tof_bowl_corr_p_%s.png" % index_fig, format="png", dpi=600)
        plt.show()


def plot_FDM(xx, yy, save, bins_s):
    fig1, ax1 = plt.subplots(figsize=(7, 6), constrained_layout=True)
    # Plot and crop FDM
    FDM, xedges, yedges = np.histogram2d(xx, yy, bins=(bins_s[0],bins_s[1]))

    FDM[FDM == 0] = 1  # to have zero after apply log
    FDM = np.log(FDM)

    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    # set x-axis label
    ax1.set_xlabel("x [mm]", color="red", fontsize=10)
    # set y-axis label
    ax1.set_ylabel("y [mm]", color="red", fontsize=10)
    plt.title("FDM")
    img = plt.imshow(FDM.T, extent=extent, origin='lower', aspect="auto")
    fig1.colorbar(img)

    if save:
        plt.savefig(variables.result_path + "fdm.png", format="png", dpi=600)
        plt.savefig(variables.result_path + "fdm.svg", format="svg", dpi=600)
    plt.show(block=True)


