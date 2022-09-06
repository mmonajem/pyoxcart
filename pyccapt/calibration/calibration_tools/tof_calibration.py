import numpy as np
from sklearn.preprocessing import MinMaxScaler
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

from calibration_tools import variables


def voltage_corr(x, a, b, c, d):
    #     return a / np.sqrt((b + (c * x) + (d * (x**2))))
    return (a / (b * (x ** 2) + c * x + d))


def voltage_coorection(dld_highVoltage_peak, dld_t_peak, index_fig, figname, num_sample=300, plot=True, save=False):
    if len(dld_highVoltage_peak) > num_sample:
        pass
    else:
        num_sample = len(dld_highVoltage_peak)
    mask = np.random.randint(0, len(dld_highVoltage_peak), num_sample)

    dld_t_peak_norm = np.median(dld_t_peak) / dld_t_peak[mask]
    fitresult, _ = curve_fit(voltage_corr, dld_highVoltage_peak[mask], dld_t_peak_norm)

    if plot:
        fig1, ax1 = plt.subplots(figsize=(8, 4))

        x = plt.scatter(dld_highVoltage_peak[mask], dld_t_peak[mask], color="blue", label='t', alpha=0.1)
        ax1.set_ylabel("Time of flight (ns)", color="red", fontsize=10)
        ax1.set_xlabel("Voltage (V)", color="red", fontsize=10)
        plt.grid(color='aqua', alpha=0.3, linestyle='-.', linewidth=2)

        # plot high voltage curve
        ax2 = ax1.twinx()
        y = ax2.plot(dld_highVoltage_peak, voltage_corr(dld_highVoltage_peak, *fitresult), color='r', label='F_V')

        plt.legend(handles=[x], loc='upper right')

        if save == True:
            plt.savefig(variables.result_path + "//vol_corr_%s_%s.svg" % (figname, index_fig), format="svg", dpi=600)
            plt.savefig(variables.result_path + "//vol_corr_%s_%s.png" % (figname, index_fig), format="png", dpi=600)

        plt.show()
    return fitresult


def bowl_corr_fit(data_xy, a, b, c, d, e, f):
    x = data_xy[0]
    y = data_xy[1]

    result = (a + b * x + c * y + d * (x ** 2) + e * x * y + f * (y ** 2))
    #     result = np.sqrt(a + b*x + c*y + d*(x**2) + e*x*y + f*(y**2))
    return result


def bowl_correction(dld_x_bowl, dld_y_bowl, dld_t_bowl, max_hist_tof, index_fig, figname, plot=True, save=False):
    scaler2 = MinMaxScaler(feature_range=(-1, 1))
    x_bowl = scaler2.fit_transform(dld_x_bowl.reshape(-1, 1)).reshape((-1,))
    y_bowl = scaler2.fit_transform(dld_y_bowl.reshape(-1, 1)).reshape((-1,))
    dld_t_bowl = max_hist_tof / dld_t_bowl

    parameters, covariance = curve_fit(bowl_corr_fit, [x_bowl, y_bowl], dld_t_bowl)

    if plot:
        # create surface function model
        # setup data points for calculating surface model
        model_x_data = np.linspace(-1, 1, 30)
        model_y_data = np.linspace(-1, 1, 30)
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
        ax.set_xlabel('X', color="red", fontsize=20)
        ax.set_ylabel('Y', color="red", fontsize=20)
        ax.set_zlabel(r"$F_B$", color="red", fontsize=20)
        ax.tick_params(axis='both', which='major', labelsize=8)
        # ax.tick_params(axis='both', which='minor', labelsize=8)

        if save:
            plt.savefig(variables.result_path + "//bowl_corr_%s_%s.svg" % (figname, index_fig), format="svg", dpi=600)
            plt.savefig(variables.result_path + "//bowl_corr_%s_%s.png" % (figname, index_fig), format="png", dpi=600)

        plt.show()
    return parameters
