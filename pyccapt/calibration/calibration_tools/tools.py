"""
This is file contains tools for mass calibration process.
"""

import numpy as np

from scipy.signal import find_peaks, peak_widths
import matplotlib.pyplot as plt
import math
from scipy.optimize import curve_fit
from scipy.stats import gmean
from mpl_toolkits.mplot3d import Axes3D
from scipy import interpolate
from adjustText import adjust_text
from pybaselines import Baseline
import pybaselines
# Local module and scripts
from pyccapt.calibration.calibration_tools import variables, data_tools, data_loadcrop
from pyccapt.calibration.calibration_tools import intractive_point_identification, selectors_data
from pyccapt.calibration.calibration_tools import logging_library


from ipywidgets import fixed, interact_manual


def hist_plot(mc_tof, bin, range_data=None, mc_peak_label=False, adjust_label=False, ranging=False, log=True,
              mode='count', percent=50, peaks_find=True, peaks_find_plot=True, plot=False, prominence=500,
              distance=None, h_line=False, selector='None', fast_hist=True, fig_name=None, text_loc='right', label='mc',
            peak_val_plot=True, fig_size=(9/2.54, 6/2.54), background={'calculation': False}):
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
    logger = logging_library.logger_creator('data_loadcrop')

    bins = np.linspace(np.min(mc_tof), np.max(mc_tof), round(np.max(mc_tof) / bin))

    if mode == 'count':
        y, x = np.histogram(mc_tof, bins=bins)
        logger.info("Selected Mode = count")
    elif mode == 'normalised':
        # calculate as counts/(Da * totalCts) so that mass spectra with different
        # count numbers are comparable
        mc_tof = (mc_tof / bin) / len(mc_tof)
        y, x = np.histogram(mc_tof, bins=bins)
        # med = median(y);
        logger.info("Selected Mode = normalised")

    fig1, ax1 = plt.subplots(figsize=fig_size)

    if peaks_find:
        peaks, properties = find_peaks(y, prominence=prominence, distance=distance, height=0)
        index_peak_max = np.argmax(properties['peak_heights'])
        # find peak width
        peak_widths_p = peak_widths(y, peaks, rel_height=(percent / 100), prominence_data=None)

    # calculate the background
    if background['calculation']:

        baseline_fitter = Baseline(x_data=bins[:-1])
        fit_1, params_1 = baseline_fitter.aspls(y, lam=5e10, tol=1e-1, max_iter=100)

        if background['mode'] == 'fabc':
            fit_2, params_2 = pybaselines.classification.fabc(y, lam=background['lam'], num_std=background['num_std'],
                                                              pad_kwargs='edges')
        if background['mode'] == 'dietrich':
            fit_2, params_2 = pybaselines.classification.dietrich(y, num_std=background['num_std'])
        if background['mode'] == 'cwt_br':
            fit_2, params_2 = pybaselines.classification.cwt_br(y, poly_order=background['poly_order'],
                                                                num_std=background['num_std'], tol=background['tol'])
        if background['mode'] == 'selective_mask_t':
            p = np.poly1d(np.polyfit(background['non_mask'][:,0], background['non_mask'][:,1], 5))
            baseline_handle = ax1.plot(x, p(x), '--')
        if background['mode'] == 'selective_mask_mc':
            def fit(x, a, b):
                yy = (a/(2*np.sqrt(b))) * 1/(np.sqrt(x))
                return yy
            fitresult, _ = curve_fit(fit, background['non_mask'][:,0], background['non_mask'][:,1])
            yy = fit(x, *fitresult)
            ax1.plot(x, yy, '--')

        if background['plot_no_back']:
            mask_2 = params_2['mask']
            mask_f = np.full((len(mc_tof)), False)
            for i in range(len(mask_2)):
                if mask_2[i]:
                    step_loc = np.min(mc_tof) + bin * i
                    mask_t = np.logical_and((mc_tof < step_loc + bin), (mc_tof > step_loc))
                    mask_f = np.logical_or(mask_f, mask_t)
            background_ppm = (len(mask_f[mask_f == True]) * 1e6 / len(mask_f)) / np.max(mc_tof)

    if plot:
        if fast_hist:
            steps = 'stepfilled'
        else:
            steps = 'bar'

        y, x = plot_hist(ranging, range_data, mc_tof, bins, log, steps)
        if background['calculation']:
            if background['plot_no_back']:
                if background['plot']:
                    ax1.plot(bins[:-1], fit_2, label='class', color='r')
                    ax3 = ax1.twiny()
                    ax3.axis("off")
                    ax3.plot(fit_1, label='aspls', color='black')

                mask_2 = params_2['mask']
                if background['patch']:
                    ax1.plot(bins[:-1][mask_2], y[mask_2], 'o', color='orange')[0]

        if label == 'mc':
            ax1.set_xlabel("mass-to-charge-state ratio [Da]", fontsize=8)
        elif label == 'tof':
            ax1.set_xlabel("Time of Flight [ns]", fontsize=8)

        ax1.set_ylabel("frequency [cts]", fontsize=8)

        if peaks_find:
            print("The peak index for MRP calculation is:", index_peak_max)
            if label == 'mc':
                mrp = '{:.2f}'.format(x[peaks[index_peak_max]] / (x[int(peak_widths_p[3][index_peak_max])] -
                                                                  x[int(peak_widths_p[2][index_peak_max])]))
                if background['calculation'] and background['plot_no_back']:
                    txt = 'bin width: %s Da\nnum atoms: %.2f$e^6$\nbackG: %s ppm/Da\nMRP(FWHM): %s' \
                              % (bin, len(mc_tof)/1000000, int(background_ppm), mrp)
                else:
                    # annotation with range stats
                    upperLim = 4.5  # Da
                    lowerLim = 3.5  # Da
                    mask = np.logical_and((x >= lowerLim), (x <= upperLim))
                    BG4 = np.sum(y[np.array(mask[:-1])]) / (upperLim - lowerLim)
                    BG4 = BG4 / len(mc_tof) * 1E6

                    txt = 'bin width: %s Da\nnum atoms: %.2f$e^6$\nBG@4: %s ppm/Da\nMRP(FWHM): %s' \
                          % (bin, (len(mc_tof)/1000000), int(BG4), mrp)

            elif label == 'tof':
                mrp = '{:.2f}'.format(x[peaks[index_peak_max]] / (x[int(peak_widths_p[3][index_peak_max])] -
                                                            x[int(peak_widths_p[2][index_peak_max])]))
                if background['calculation'] and background['plot_no_back']:
                        txt = 'bin width: %s Da\nnum atoms: %.2f$e^6$\nbackG: %s ppm/ns\nMRP(FWHM): %s' \
                              % (bin, len(mc_tof)/1000000, int(background_ppm), mrp)
                else:
                    # annotation with range stats
                    upperLim = 50.5  # ns
                    lowerLim = 49.5  # ns
                    mask = np.logical_and((x >= lowerLim), (x <= upperLim))
                    BG50 = np.sum(y[np.array(mask[:-1])]) / (upperLim - lowerLim)
                    BG50 = BG50 / len(mc_tof) * 1E6
                    txt = 'bin width: %s Da\nnum atoms: %.2f$e^6$ \nBG@50: %s ppm/ns\nMRP(FWHM): %s' \
                          % (bin, len(mc_tof)/1000000, int(BG50), mrp)

            props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
            if text_loc == 'left':
                ax1.text(0.1, 0.95, txt, va='top', ma='left', transform=ax1.transAxes, bbox=props, fontsize=8, alpha=0.8)
            elif text_loc == 'right':
                ax1.text(0.50, 0.95, txt, va='top', ma='left', transform=ax1.transAxes, bbox=props, fontsize=8, alpha=0.8)


            ax1.tick_params(axis='both', which='major', labelsize=12)
            ax1.tick_params(axis='both', which='minor', labelsize=10)

            if peaks_find_plot:
                annotes = []
                texts = []
                if peak_val_plot:
                    for i in range(len(peaks)):
                        # if len(mc_tof_ideal) != 0:
                        #     mc_ideal = mc_tof_ideal[i]
                        #     mc_ideal = mc_ideal.split('+')
                        #     texts.append(
                        #         plt.text(x[peaks][i], y[peaks][i], r'$%s^%s$' % (mc_ideal[i], (len(mc_ideal) - 1) * '+'),
                        #                  color='gray', size=7,
                        #                  alpha=0.5))
                        if mc_peak_label:
                            phases = range_data['element'].tolist()
                            charge = range_data['charge'].tolist()
                            isotope = range_data['isotope'].tolist()
                            name_element = r'${}^{%s}%s^{%s+}$' % (isotope[i], phases[i], charge[i])
                            texts.append(
                                plt.text(x[peaks][i], y[peaks][i], name_element,
                                         color='r', size=7,
                                         alpha=0.7))

                            # ax1.annotate(r'$%s^%s$' % (mc_ideal[0], (len(mc_ideal) - 1) * '+'),
                            #              xy=(x[peaks][i], y[peaks][i]),
                            #              xytext=(x[peaks][i] + 1.5, y[peaks][i]), size=6, color='gray')
                            # plt.axvline(mc_ideal[i], color='k', linewidth=1)
                        else:
                            texts.append(plt.text(x[peaks][i], y[peaks][i], '%s' % '{:.2f}'.format(x[peaks][i]), color='r',
                                                  size=7, alpha=0.7))
                            #     ax1.annotate('%s' % '{:.2f}'.format(x[peaks][i]),
                            #                  xy=(x[peaks][i], y[peaks][i]),
                            #                  xytext=(x[peaks][i] + 1.5, y[peaks][i]), size=6, color='gray')
                        annotes.append(str(i + 1))
                        if h_line:
                            right_side_x = x[int(peak_widths_p[3][i])]
                            left_side_x = x[int(peak_widths_p[2][i])]
                            left_side_y = y[int(peak_widths_p[2][i])]
                            plt.hlines(left_side_y, left_side_x, right_side_x, color="red")
                if adjust_label:
                    adjust_text(texts, arrowprops=dict(arrowstyle='-', color='red', lw=0.5))
                if selector == 'rect':
                    # Connect and initialize rectangle box selector
                    data_loadcrop.rectangle_box_selector(ax1)
                    plt.connect('key_press_event', selectors_data.toggle_selector)
                elif selector == 'peak':
                    # connect peak selector
                    af = intractive_point_identification.AnnoteFinder(x[peaks], y[peaks], annotes, ax=ax1)
                    fig1.canvas.mpl_connect('button_press_event', af)
        plt.tight_layout()
        if fig_name is not None:
            if label == 'mc':
                plt.savefig(variables.result_path + "//mc_%s.eps" % fig_name, format="eps", dpi=300)
                plt.savefig(variables.result_path + "//mc_%s.png" % fig_name, format="png", dpi=300)
            elif label == 'tof':
                plt.savefig(variables.result_path + "//tof_%s.eps" % fig_name, format="eps", dpi=300)
                plt.savefig(variables.result_path + "//tof_%s.png" % fig_name, format="png", dpi=300)
        if ranging:
            plt.legend(loc='center right')

        plt.show()
    else:
        plt.close(fig1)

    peak_widths_f = []
    for i in range(len(peaks)):
        peak_widths_f.append([y[int(peak_widths_p[2][i])], x[int(peak_widths_p[2][i])], x[int(peak_widths_p[3][i])]])

    if background['calculation'] and background['plot_no_back']:
        return x[peaks], y[peaks], peak_widths_f, mask_f
    else:
        return x[peaks], y[peaks], peak_widths_f


def plot_hist(ranging, range_data, mc_tof, bins, log, steps):

    if ranging:
        phases = range_data['element'].tolist()
        colors = range_data['color'].tolist()
        mc_low = range_data['mc_low'].tolist()
        mc_up = range_data['mc_up'].tolist()
        charge = range_data['charge'].tolist()
        isotope = range_data['isotope'].tolist()
        mask_all = np.full((len(mc_tof)), False)
        for i in range(len(phases) + 1):
            if i < len(phases):
                mask = np.logical_and((mc_tof < mc_up[i]), mc_tof > mc_low[i])
                mask_all = np.logical_or(mask_all, mask)
                if phases[i] == 'unranged':
                    name_element = 'unranged'
                else:
                    name_element = r'${}^{%s}%s^{%s+}$' % (isotope[i], phases[i], charge[i])

                y, x, _ = plt.hist(mc_tof[mask], bins=bins, log=log, histtype=steps, color=colors[i],
                                       label=name_element)
            elif i == len(phases):
                mask_all = np.logical_or(mask_all, mask)
                y, x, _ = plt.hist(mc_tof[~mask_all], bins=bins, log=log, histtype=steps, color='slategray')
    else:
        y, x, _ = plt.hist(mc_tof, bins=bins, log=log, histtype=steps, color='slategray')
    return y, x


def find_closest_element(input_value):
    def closest_value(mass_list, element_list, input_value):
        element = np.array(element_list)
        closest_mass = []
        closest_element = []
        for i in range(4):
            arr = np.asarray(mass_list / (i + 1))
            i = (np.abs(arr - input_value)).argmin()
            closest_mass.append(arr[i])
            closest_element.append(element[i] + '%s+' % (i + 1))
        return closest_mass, closest_element

    isotopeTableFile = '../../../files/isotopeTable.h5'
    dataframe = data_tools.read_hdf5_through_pandas(isotopeTableFile)
    mass_list = dataframe['weight']
    element_list = dataframe['element']
    closest_mass, closest_element = closest_value(mass_list, element_list, input_value)

    return closest_mass, closest_element


# def history_ex(mc, dld_highVoltage, label='mc', mean_t=1.5, mc_max=100, plot=False, fig_name=None):
#     MAXMC = mc_max  # maximum mc that makes sense
#     HISTORYPIX = 1024  # number of pixels in the hit sequence tof image
#     TOFPIX = 512  # number of vertical pixels for tof image
#
#     mcTmp = mc[mc < MAXMC]
#     VDCtmp = dld_highVoltage[mc < MAXMC]
#
#     # [mcImage, tofImageCenters] = hist3([(1:length(mcTmp))', mcTmp],[HISTORYPIX,TOFPIX]);
#     mcImage, xedges, yedges = np.histogram2d(VDCtmp, mcTmp, bins=(HISTORYPIX, TOFPIX))
#     mcImage[mcImage == 0] = 1  # to have zero after apply log
#     mcImage = np.log(mcImage)  # if weak peaks are to be imaged

    # #### find the peaks
    # mean = np.mean(mcImage.T, axis=1)
    # # mean_t =  np.mean(mean)
    # ##################
    #
    # maximum = np.amax(mean)
    # index = np.where(mean == maximum)
    # print(index)
    # for i in range(100):
    #     if mean[index[0] + i] > mean_t:
    #         index_max = index[0] + i
    #         continue
    #     else:
    #         break
    #
    # for i in range(100):
    #     if mean[index[0] - i] > mean_t:
    #         index_min = index[0] - i
    #         continue
    #     else:
    #         break
    #
    # peak_mean = (index[0] / 512) * 100
    # peak_begin = index_min * 100 / 512
    # peak_end = index_max * 100 / 512

    # #### plotting data history
    # if plot:
    #     fig1, ax1 = plt.subplots(figsize=(5, 2.5))
    #     extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    #     # set x-axis label
    #     ax1.set_xlabel("dc voltage [V]", color="red", fontsize=12)
    #     # set y-axis label
    #     if label == 'mc':
    #         ax1.set_ylabel("mass to charge [Da]", color="red", fontsize=12)
    #     elif label == 'tof':
    #         ax1.set_ylabel("time 0f flight [ns]", color="red", fontsize=12)
    #     ax1.tick_params(axis='both', which='major', labelsize=12)
    #     ax1.tick_params(axis='both', which='minor', labelsize=12)
    #
    #     plt.imshow(mcImage.T, extent=extent, origin='lower', aspect="auto")
    #     # ax1.grid(axis='y', color='0.95')
    #     if fig_name is not None:
    #         plt.savefig(variables.result_path + "//ex_his_%s.svg" % fig_name, format="svg", dpi=600)
    #         plt.savefig(variables.result_path + "//ex_his_%s.png" % fig_name, format="png", dpi=600)
    #     plt.show()

    # return [peak_begin, peak_end]  # peaks as beginning/end


# def voltage_corr(highVoltage, mc, fitPeak, ionsPerFitSegment, plot=False, fig_name=None):
#     def voltage_corr_f(x, a, b, c):
#         # return (np.sqrt(b + x + c*(x**2))) * a
#         return a * (x ** 2) + b * x + c
#
#     logger = logging_library.logger_creator('data_loadcrop')
#     if not isinstance(highVoltage, np.ndarray) or not isinstance(mc, np.ndarray) or not isinstance(fitPeak, np.ndarray):
#         logger.error("Incorrect data type of passed arguments")
#     numAtom = len(mc)
#     numMcBins = math.floor(numAtom / ionsPerFitSegment)
#     binLimitsIdx = np.round(np.linspace(0, numAtom - 1, numMcBins + 1))
#     # binCenters = np.round((binLimitsIdx[1:] + binLimitsIdx[0:-1]) / 2)
#     pkLoc = np.zeros(0)
#     # limits = np.zeros((numMcBins, 2))
#     VDC = np.zeros(0)
#     for i in range(numMcBins):
#         # limits[i, :] = [data[int(binLimitsIdx[i]), 0], data[int(binLimitsIdx[i + 1]), 0]]
#         mask = np.logical_and((highVoltage > highVoltage[int(binLimitsIdx[i])]),
#                               (highVoltage < highVoltage[int(binLimitsIdx[i + 1])]))
#         mcBin = mc[mask]
#         mcBin = mcBin[np.logical_and(mcBin > fitPeak[0], mcBin < fitPeak[1])]
#         # for cases that the mcBin contains nothing
#         # Based on ionsPerFitSegment, sth the mcBin = []
#         if len(mcBin) == 0:
#             pass
#         else:
#             pkLoc = np.append(pkLoc, np.median(mcBin))
#             VDC = np.append(VDC, np.mean(highVoltage[np.array(mask)]))
#
#     corr = pkLoc / pkLoc[0]
#
#     # peak location vs DC voltage
#     # Do the fit, defining the fitting function in-line
#     fitresult, _ = curve_fit(voltage_corr_f, VDC, corr)
#
#     a, b, c = fitresult
#     if plot or fig_name is not None:
#         fig1, ax1 = plt.subplots(figsize=(8, 6))
#         ax1.scatter(VDC, corr)
#         ax1.plot(VDC, voltage_corr_f(VDC, a, b, c))
#
#         ax1.set_xlabel("DC voltage", color="red", fontsize=12)
#         ax1.set_ylabel(r"$F_V$", color="red", fontsize=12)
#         # ax1.tick_params(axis='both', which='major', labelsize=12)
#         # ax1.tick_params(axis='both', which='minor', labelsize=10)
#         if fig_name is not None:
#             plt.savefig(variables.result_path + "//vol_cor_%s.svg" % fig_name, format="svg", dpi=600)
#             plt.savefig(variables.result_path + "//vol_cor_%s.png" % fig_name, format="png", dpi=600)
#         if plot:
#             plt.show()
#         else:
#             plt.close()
#     return voltage_corr_f(highVoltage, a, b, c)
#
#
# def bowl_corr(x, y, mc, mcIdeal, mc_min, mc_max, plot=False, fig_name=None):
#     def bowl_corr_fit(data_xy, a, b, c, d, e, f):
#         x = data_xy[0]
#         y = data_xy[1]
#         return a + b * x + c * y + d * x ** 2 + e * x * y + f * y ** 2
#
#     ideal = np.logical_and(mc > mc_min, mc < mc_max)
#     detxIn = x[np.array(ideal)]
#     detyIn = y[np.array(ideal)]
#     mcIn = mc[np.array(ideal)]
#
#     parameters, covariance = curve_fit(bowl_corr_fit, [detxIn, detyIn], mcIn)
#
#     if plot or fig_name is not None:
#         # create surface function model
#         # setup data points for calculating surface model
#         model_x_data = np.linspace(-38, 38, 30)
#         model_y_data = np.linspace(-38, 38, 30)
#         # create coordinate arrays for vectorized evaluations
#         X, Y = np.meshgrid(model_x_data, model_y_data)
#         # calculate Z coordinate array
#         Z = bowl_corr_fit(np.array([X, Y]), *parameters) / mcIdeal
#
#         # setup figure object
#         fig = plt.figure()
#         # setup 3d object
#         ax = Axes3D(fig)
#         # plot surface
#         ax.plot_surface(X, Y, Z)
#         # plot input data
#         # ax.scatter(detxIn, detyIn, mcIn, color='red')
#         # set plot descriptions
#         ax.set_xlabel('X', color="red", fontsize=20)
#         ax.set_ylabel('Y', color="red", fontsize=20)
#         ax.set_zlabel(r"$F_B$", color="red", fontsize=20)
#
#         # ax.tick_params(axis='both', which='major', labelsize=12)
#         # ax.tick_params(axis='both', which='minor', labelsize=10)
#         if fig_name is not None:
#             plt.savefig(variables.result_path + "//bowl_cor_%s.svg" % fig_name, format="svg", dpi=600,
#                         bbox_index='tight')
#             plt.savefig(variables.result_path + "//bowl_cor_%s.png" % fig_name, format="png", dpi=600,
#                         bbox_index='tight')
#         if plot:
#             plt.show()
#         else:
#             plt.close()
#     corr = bowl_corr_fit([x, y], *parameters)
#     return corr / mcIdeal
#
#
# def linear_correction(mc, peaks, list_material, kind):
#     peakLocIs = peaks
#     peakLocIdeal = list_material
#
#     corrRatio = peakLocIdeal / peakLocIs
#
#     print(corrRatio)
#     f = interpolate.interp1d(peakLocIs.T, peakLocIdeal.T, kind=kind, fill_value="extrapolate")
#
#     return f(mc)
