"""
This is file contains tools for mass calibration process.
"""

import numpy as np
from scipy.signal import find_peaks, peak_widths
import matplotlib.pyplot as plt
import math
from scipy.optimize import curve_fit
from mpl_toolkits.mplot3d import Axes3D
from scipy import interpolate

# Local module and scripts
from pyccapt.calibration.calibration_tools import variables
from pyccapt.calibration.calibration_tools import intractive_point_identification
from pyccapt.calibration.calibration_tools import logging_library

logger = logging_library.logger_creator('data_loadcrop')

def massSpecPlot(mc, bin, mc_ideal=np.zeros(0), mode='count', percent=50, peaks_find=True, peaks_find_plot=True, plot=False,
                 prominence=500, distance=None, fig_name=None, text_loc='right', label='mc'):
    """
    massSpecPlot plots the data from pos to get a mass spectrum as a figure

    handle = plotMassSpec(mc, bin, mode)
    handle = plotMassSpec(mc, bin)

    INPUT
    mc:       is the mass-to-charge(mc)-ratio [Da] of the events in the
              APT measurement stored in pos, table

    bin:      is the width of the steps in which the plot is performed

    mode:     specifies the way the counts are applied
              'count' records the number of counts
              'normalised' records the number of counts if the bin was one Da
              wide over the overall number of counts
              default mode is 'count'

    OUTPUT
    handle:   handle to the plot that contains counts or
              (counts/Dalton)/totalCounts over Dalton. Used in further
              analysis to find new ions
    """

    def find_nearest(x, y, index_peak, percent):

        peak = y[index_peak]
        max_possible = min(abs(len(y) - index_peak), index_peak)

        for i in range(max_possible):
            if y[index_peak + i] < peak * percent / 100:
                index_right_edge = index_peak + i
                break
            if i == max_possible - 1:
                index_right_edge = index_peak + i

        for i in range(max_possible):
            if y[index_peak - i] < peak * percent / 100:
                index_left_edge = index_peak - i
                break
            if i == max_possible - 1:
                index_left_edge = index_peak + i

        return [x[index_left_edge], x[index_right_edge], y[index_left_edge], y[index_right_edge]]

    bins = np.linspace(np.min(mc), np.max(mc), round(np.max(mc) / bin))

    if mode == 'count':
        y, x = np.histogram(mc, bins=bins)
        logger.info("Selected Mode = count")
    elif mode == 'normalised':
        # calculate as counts/(Da * totalCts) so that mass spectra with different
        # count numbers are comparable
        y, x = np.histogram(mc, bins=bins)
        mc = mc / bin / len(mc)
        # med = median(y);
        logger.info("Selected Mode = normalised")
    else:
        y, x = np.histogram(mc, bins=bins)
        logger.info("Mode not selected")

    fig1, ax1 = plt.subplots(figsize=(8, 4))

    if peaks_find:
        max_hist = x[np.where(y == y.max())]
        index_max = np.where(y == y.max())[0].tolist()[0]
        edges = find_nearest(x, y, index_max, percent=percent)

        peaks, properties = find_peaks(y, prominence=prominence, distance=distance)
        # prominences, left_bases, right_bases = peak_prominences(y, peaks)
        # print(prominences, left_bases, right_bases)
        # find peak width
        results_half = peak_widths(y, peaks, rel_height=0.998, prominence_data=None)

        # results_full = peak_widths(y, peaks, rel_height=1)
        peaks = peaks.tolist()
        for i in range(len(peaks)):
            peakLocIs_tmp = [x[peaks[i]], y[peaks[i]]]
            if peakLocIs_tmp[0] > 0.8:
                index_peak = peaks[i]
                if 'peakLocIs' in locals():
                    edges = find_nearest(x, y, index_peak, percent=percent)
                    peakLocIs_tmp = np.append(peakLocIs_tmp, edges)
                    peakLocIs = np.append(peakLocIs, np.expand_dims(peakLocIs_tmp, 0), axis=0)
                else:
                    edges = find_nearest(x, y, index_peak, percent=percent)
                    peakLocIs_tmp = np.append(peakLocIs_tmp, edges)
                    peakLocIs = np.expand_dims(peakLocIs_tmp, 0)

        index_peak_max = np.argmax(peakLocIs[:, 1])
        edges = peakLocIs[index_peak_max, 2:4]

    if plot:
        y, x, _ = plt.hist(mc, bins=bins, log=True)
        if label == 'mc':
            plt.title("Mass Spectrum")
            ax1.set_xlabel("mass-to-charge-state ratio [Da]", color="red", fontsize=10)
        elif label == 'tof':
            plt.title("Time of Flight")
            ax1.set_xlabel("Time of Flight [ns]", color="red", fontsize=10)
        if mode == 'count':
            ax1.set_ylabel("frequency [cts / Da / totCts]", color="red", fontsize=10)
        elif mode == 'normalised':
            ax1.set_ylabel("frequency [cts / Da / totCts]", color="red", fontsize=10)

        # annotation with range stats
        upperLim = 4.5  # Da
        lowerLim = 3.5  # Da
        mask = np.logical_and((x >= lowerLim), (x <= upperLim))
        BG4 = np.sum(y[np.array(mask[:-1])]) / (upperLim - lowerLim)
        BG4 = BG4 / len(mc) * 1E6
        mrp = '{:.2f}'.format((max_hist / (edges[1] - edges[0]))[0])
        txt = 'bin width: %s Da\nnum atoms: %s\nbackG @ 4 Da: %s ppm/Da\nMRP: %s' % (bin, len(mc), int(BG4), mrp)

        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        if text_loc == 'left':
            ax1.text(0.05, 0.82, txt, transform=ax1.transAxes, bbox=props, fontsize=8)
        elif text_loc == 'right':
            ax1.text(0.7, 0.82, txt, transform=ax1.transAxes, bbox=props, fontsize=8)
        ax1.tick_params(axis='both', which='major', labelsize=12)
        ax1.tick_params(axis='both', which='minor', labelsize=10)

        if peaks_find_plot:

            if 'peakLocIs' in locals():

                plt.scatter(peakLocIs[:, 0], peakLocIs[:, 1], marker="x", color='red')
                # plot a red line for width of each peak
                # for i in range(len(peaks)):
                #     peakLocIs_tmp = [x[peaks[i]], y[peaks[i]]]
                # Draw a horizontal line for width of each peak
                # if peakLocIs_tmp[0] > 0.8:
                #     plt.hlines(results_half[1][i], x[int(results_half[2][i])], x[int(results_half[3][i])], color="red")
                annotes = []
                for i in range(len(peakLocIs)):
                    ax1.annotate('%s' % '{:.2f}'.format(peakLocIs[i, 0]),
                                 xy=(peakLocIs[i, 0], peakLocIs[i, 1]),
                                 xytext=(peakLocIs[i, 0] + 2.5, peakLocIs[i, 1]))
                    annotes.append(str(i + 1))
                af = intractive_point_identification.AnnoteFinder(peakLocIs[:, 0], peakLocIs[:, 1], annotes, ax=ax1)
                fig1.canvas.mpl_connect('button_press_event', af)

        if fig_name is not None:
            if label == 'mc':
                plt.savefig(variables.result_path + "//mc_%s.svg" % fig_name, format="svg", dpi=600)
                plt.savefig(variables.result_path + "//mc_%s.png" % fig_name, format="png", dpi=600)
            elif label == 'tof':
                plt.savefig(variables.result_path + "//tof_%s.svg" % fig_name, format="svg", dpi=600)
                plt.savefig(variables.result_path + "//tof_%s.png" % fig_name, format="png", dpi=600)
        if mc_ideal.any() != 0:
            for i in range(len(mc_ideal)):
                plt.axvline(mc_ideal[i], color='k', linewidth=1)
        plt.show()
    else:
        plt.close(fig1)

    if 'peakLocIs' in locals():
        max_paek_edges = [x[int(results_half[2][index_peak_max])], x[int(results_half[3][index_peak_max])]]
    else:
        max_hist = 0
        edges = 0
        peakLocIs = 0
        max_paek_edges = 0
        index_max = 0

    return max_hist, edges, peakLocIs, max_paek_edges, index_max


def history_ex(mc, dld_highVoltage, mean_t=1.5, mc_max=100, plot=False, fig_name=None):
    MAXMC = mc_max  # maximum mc that makes sense
    HISTORYPIX = 1024  # number of pixels in the hit sequence tof image
    TOFPIX = 512  # number of vertical pixels for tof image

    mcTmp = mc[mc < MAXMC]
    VDCtmp = dld_highVoltage[mc < MAXMC]

    # [mcImage, tofImageCenters] = hist3([(1:length(mcTmp))', mcTmp],[HISTORYPIX,TOFPIX]);
    mcImage, xedges, yedges = np.histogram2d(VDCtmp, mcTmp, bins=(HISTORYPIX, TOFPIX))
    mcImage[mcImage == 0] = 1  # to have zero after apply log
    mcImage = np.log(mcImage)  # if weak peaks are to be imaged

    #### find the peaks
    mean = np.mean(mcImage.T, axis=1)
    # mean_t =  np.mean(mean)
    ##################

    maximum = np.amax(mean)
    index = np.where(mean == maximum)
    print(index)
    for i in range(100):
        if mean[index[0] + i] > mean_t:
            index_max = index[0] + i
            continue
        else:
            break

    for i in range(100):
        if mean[index[0] - i] > mean_t:
            index_min = index[0] - i
            continue
        else:
            break

    peak_mean = (index[0] / 512) * 100
    peak_begin = index_min * 100 / 512
    peak_end = index_max * 100 / 512

    #### plotting data history
    if plot:
        fig1, ax1 = plt.subplots(figsize=(6, 3))
        extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
        # set x-axis label
        ax1.set_xlabel("DC voltage", color="red", fontsize=20)
        # set y-axis label
        ax1.set_ylabel("mass to charge [Da]", color="red", fontsize=12)
        ax1.tick_params(axis='both', which='major', labelsize=12)
        ax1.tick_params(axis='both', which='minor', labelsize=12)
        plt.title("Experiment history")
        plt.imshow(mcImage.T, extent=extent, origin='lower', aspect="auto")
        # ax1.grid(axis='y', color='0.95')
        if fig_name is not None:
            plt.savefig(variables.result_path + "//ex_his_%s.svg" % fig_name, format="svg", dpi=600)
            plt.savefig(variables.result_path + "//ex_his_%s.png" % fig_name, format="png", dpi=600)
        plt.show()

    return [peak_begin, peak_end]  # peaks as beginning/end


def voltage_corr(highVoltage, mc, fitPeak, ionsPerFitSegment, plot=False, fig_name=None):
    def voltage_corr_f(x, a, b, c):
        # return (np.sqrt(b + x + c*(x**2))) * a
        return a * (x ** 2) + b * x + c

    if not isinstance(highVoltage, np.ndarray) or not isinstance(mc, np.ndarray) or not isinstance(fitPeak, np.ndarray):
        logger.error("Incorrect data type of passed arguments")
    numAtom = len(mc)
    numMcBins = math.floor(numAtom / ionsPerFitSegment)
    binLimitsIdx = np.round(np.linspace(0, numAtom - 1, numMcBins + 1))
    # binCenters = np.round((binLimitsIdx[1:] + binLimitsIdx[0:-1]) / 2)
    pkLoc = np.zeros(0)
    # limits = np.zeros((numMcBins, 2))
    VDC = np.zeros(0)
    for i in range(numMcBins):
        # limits[i, :] = [data[int(binLimitsIdx[i]), 0], data[int(binLimitsIdx[i + 1]), 0]]
        mask = np.logical_and((highVoltage > highVoltage[int(binLimitsIdx[i])]),
                              (highVoltage < highVoltage[int(binLimitsIdx[i + 1])]))
        mcBin = mc[mask]
        mcBin = mcBin[np.logical_and(mcBin > fitPeak[0], mcBin < fitPeak[1])]
        # for cases that the mcBin contains nothing
        # Based on ionsPerFitSegment, sth the mcBin = []
        if len(mcBin) == 0:
            pass
        else:
            pkLoc = np.append(pkLoc, np.median(mcBin))
            VDC = np.append(VDC, np.mean(highVoltage[np.array(mask)]))

    corr = pkLoc / pkLoc[0]

    # peak location vs DC voltage
    # Do the fit, defining the fitting function in-line
    fitresult, _ = curve_fit(voltage_corr_f, VDC, corr)

    a, b, c = fitresult
    if plot or fig_name is not None:
        fig1, ax1 = plt.subplots(figsize=(8, 6))
        ax1.scatter(VDC, corr)
        ax1.plot(VDC, voltage_corr_f(VDC, a, b, c))
        plt.title("Peak location vs DC voltage")
        ax1.set_xlabel("DC voltage", color="red", fontsize=20)
        ax1.set_ylabel(r"$F_V$", color="red", fontsize=20)
        # ax1.tick_params(axis='both', which='major', labelsize=12)
        # ax1.tick_params(axis='both', which='minor', labelsize=10)
        if fig_name is not None:
            plt.savefig(variables.result_path + "//vol_cor_%s.svg" % fig_name, format="svg", dpi=600)
            plt.savefig(variables.result_path + "//vol_cor_%s.png" % fig_name, format="png", dpi=600)
        if plot:
            plt.show()
        else:
            plt.close()
    return voltage_corr_f(highVoltage, a, b, c)


def bowl_corr(x, y, mc, mcIdeal, mc_min, mc_max, plot=False, fig_name=None):
    def bowl_corr_fit(data_xy, a, b, c, d, e, f):
        x = data_xy[0]
        y = data_xy[1]
        return a + b * x + c * y + d * x ** 2 + e * x * y + f * y ** 2

    ideal = np.logical_and(mc > mc_min, mc < mc_max)
    detxIn = x[np.array(ideal)]
    detyIn = y[np.array(ideal)]
    mcIn = mc[np.array(ideal)]

    parameters, covariance = curve_fit(bowl_corr_fit, [detxIn, detyIn], mcIn)

    if plot or fig_name is not None:
        # create surface function model
        # setup data points for calculating surface model
        model_x_data = np.linspace(-38, 38, 30)
        model_y_data = np.linspace(-38, 38, 30)
        # create coordinate arrays for vectorized evaluations
        X, Y = np.meshgrid(model_x_data, model_y_data)
        # calculate Z coordinate array
        Z = bowl_corr_fit(np.array([X, Y]), *parameters) / mcIdeal

        # setup figure object
        fig = plt.figure()
        # setup 3d object
        ax = Axes3D(fig)
        # plot surface
        ax.plot_surface(X, Y, Z)
        # plot input data
        # ax.scatter(detxIn, detyIn, mcIn, color='red')
        # set plot descriptions
        ax.set_xlabel('X', color="red", fontsize=20)
        ax.set_ylabel('Y', color="red", fontsize=20)
        ax.set_zlabel(r"$F_B$", color="red", fontsize=20)

        # ax.tick_params(axis='both', which='major', labelsize=12)
        # ax.tick_params(axis='both', which='minor', labelsize=10)
        if fig_name is not None:
            plt.savefig(variables.result_path + "//bowl_cor_%s.svg" % fig_name, format="svg", dpi=600,
                        bbox_index='tight')
            plt.savefig(variables.result_path + "//bowl_cor_%s.png" % fig_name, format="png", dpi=600,
                        bbox_index='tight')
        if plot:
            plt.show()
        else:
            plt.close()
    corr = bowl_corr_fit([x, y], *parameters)
    return corr / mcIdeal


def linear_correction(mc, peaks, list_material, kind):
    peakLocIs = peaks
    peakLocIdeal = list_material

    corrRatio = peakLocIdeal / peakLocIs

    print(corrRatio)
    f = interpolate.interp1d(peakLocIs.T, peakLocIdeal.T, kind=kind, fill_value="extrapolate")

    return f(mc)
