import matplotlib.pyplot as plt
import numpy as np
import pybaselines
from adjustText import adjust_text
from pybaselines import Baseline
from scipy.optimize import curve_fit
from scipy.signal import find_peaks, peak_widths

from pyccapt.calibration.calibration_tools import intractive_point_identification
from pyccapt.calibration.data_tools import data_loadcrop, plot_vline_draw, selectors_data


class APTHistogramPlotter:
    def __init__(self, mc_tof, variables, bin, label, range_data=None, adjust_label=False, ranging=False,
                 hist_color_range=False, log=True, mode='count', percent=50, peaks_find=True, peaks_find_plot=False,
                 plot=False, prominence=50, distance=None, h_line=False, selector='None', fast_hist=True, fig_name=None,
                 text_loc='right', fig_size=(9, 5), background={'calculation': False}):
        self.mc_tof = mc_tof
        self.variables = variables
        self.bin = bin
        self.label = label
        self.range_data = range_data
        self.adjust_label = adjust_label
        self.ranging = ranging
        self.hist_color_range = hist_color_range
        self.log = log
        self.mode = mode
        self.percent = percent
        self.peaks_find = peaks_find
        self.peaks_find_plot = peaks_find_plot
        self.plot = plot
        self.prominence = prominence
        self.distance = distance
        self.h_line = h_line
        self.selector = selector
        self.fast_hist = fast_hist
        self.fig_name = fig_name
        self.text_loc = text_loc
        self.fig_size = fig_size
        self.background = background

    def histogram(self):
        bins = np.linspace(np.min(self.mc_tof), np.max(self.mc_tof), round(np.max(self.mc_tof) / self.bin))

        if self.fast_hist:
            steps = 'stepfilled'
        else:
            steps = 'bar'

        if self.mode == 'count':
            y, x = np.histogram(self.mc_tof, bins=bins)
        elif self.mode == 'normalised':
            self.mc_tof = (self.mc_tof / self.bin) / len(self.mc_tof)
            y, x = np.histogram(self.mc_tof, bins=bins)

        return x, y

    def find_peaks(self, x, y):
        try:
            peaks, properties = find_peaks(y, prominence=self.prominence, distance=self.distance, height=0)
            index_peak_max = np.argmax(properties['peak_heights'])
            peak_widths_p = peak_widths(y, peaks, rel_height=(self.percent / 100), prominence_data=None)
            return peaks, properties, index_peak_max, peak_widths_p
        except ValueError:
            print('Peak finding failed.')
            return None, None, None, None

    def plot_histogram(self, x, y):
        fig1, ax1 = plt.subplots(figsize=self.fig_size)
        if self.ranging and self.hist_color_range:
            colors = self.range_data['color'].tolist()
            mc_low = self.range_data['mc_low'].tolist()
            mc_up = self.range_data['mc_up'].tolist()
            ion = self.range_data['ion'].tolist()
            mask_all = np.full(len(self.mc_tof), False)

            for i in range(len(ion) + 1):
                if i < len(ion):
                    mask = np.logical_and((self.mc_tof < mc_up[i]), self.mc_tof > mc_low[i])
                    mask_all = np.logical_or(mask_all, mask)

                    if ion[i] == 'unranged':
                        name_element = 'unranged'
                    else:
                        name_element = r'%s' % ion[i]

                    y, x, _ = plt.hist(self.mc_tof[mask], bins=x, log=self.log, histtype=steps, color=colors[i],
                                       label=name_element)
                elif i == len(ion):
                    mask_all = np.logical_or(mask_all, mask)
                    y, x, _ = plt.hist(self.mc_tof[~mask_all], bins=x, log=self.log, histtype=steps, color='slategray')
        else:
            y, x, _ = plt.hist(self.mc_tof, bins=x, log=self.log, histtype=steps, color='slategray')

        return fig1, ax1, x, y

    def calculate_background(self, x, y):
        if self.background['calculation']:
            if self.background['mode'] == 'aspls':
                baseline_fitter = Baseline(x_data=x[:-1])
                fit_1, params_1 = baseline_fitter.aspls(y, lam=5e10, tol=1e-1, max_iter=100)

            # Add other background calculation modes here...

            return fit_1

        return None

    def annotate_plot(self, ax1, x_peaks, y_peaks, peak_widths_f, background_ppm):
        ax1.set_ylabel("Frequency [cts]", fontsize=14)
        if self.label == 'mc':
            ax1.set_xlabel("Mass/Charge [Da]", fontsize=14)
        elif self.label == 'tof':
            ax1.set_xlabel("Time of Flight [ns]", fontsize=14)
        print("The peak index for MRP calculation is:", index_peak_max)
        if self.label == 'mc':
            mrp = '{:.2f}'.format(
                x_peaks[index_peak_max] / (peak_widths_f[3][index_peak_max] - peak_widths_f[2][index_peak_max]))
            if self.background['calculation'] and self.background['plot_no_back']:
                txt = 'bin width: %s Da\nnum atoms: %.2f$e^6$\nbackG: %s ppm/Da\nMRP(FWHM): %s' \
                      % (self.bin, len(self.mc_tof) / 1000000, int(background_ppm), mrp)
            else:
                upperLim = 4.5  # Da
                lowerLim = 3.5  # Da
                mask = np.logical_and((x >= lowerLim), (x <= upperLim))
                BG4 = np.sum(y[np.array(mask[:-1])]) / (upperLim - lowerLim)
                BG4 = BG4 / len(self.mc_tof) * 1E6
                txt = 'bin width: %s Da\nnum atoms: %.2f$e^6$\nBG@4: %s ppm/Da\nMRP(FWHM): %s' \
                      % (self.bin, (len(self.mc_tof) / 1000000), int(BG4), mrp)

        elif self.label == 'tof':
            mrp = '{:.2f}'.format(
                x_peaks[index_peak_max] / (peak_widths_f[3][index_peak_max] - peak_widths_f[2][index_peak_max]))
            if self.background['calculation'] and self.background['plot_no_back']:
                txt = 'bin width: %s ns\nnum atoms: %.2f$e^6$\nbackG: %s ppm/ns\nMRP(FWHM): %s' \
                      % (self.bin, len(self.mc_tof) / 1000000, int(background_ppm), mrp)
            else:
                upperLim = 50.5  # ns
                lowerLim = 49.5  # ns
                mask = np.logical_and((x >= lowerLim), (x <= upperLim))
                BG50 = np.sum(y[np.array(mask[:-1])]) / (upperLim - lowerLim)
                BG50 = BG50 / len(self.mc_tof) * 1E6
                txt = 'bin width: %s ns\nnum atoms: %.2f$e^6$ \nBG@50: %s ppm/ns\nMRP(FWHM): %s' \
                      % (self.bin, len(self.mc_tof) / 1000000, int(BG50), mrp)

        props = dict(boxstyle='round', facecolor='wheat', alpha=1)
        if self.text_loc == 'left':
            ax1.text(.01, .95, txt, va='top', ma='left', transform=ax1.transAxes, bbox=props, fontsize=10, alpha=1,
                     horizontalalignment='left', verticalalignment='top')
        elif self.text_loc == 'right':
            ax1.text(.98, .95, txt, va='top', ma='left', transform=ax1.transAxes, bbox=props, fontsize=10, alpha=1,
                     horizontalalignment='right', verticalalignment='top')

        ax1.tick_params(axis='both', which='major', labelsize=10)
        ax1.tick_params(axis='both', which='minor', labelsize=10)

        annotes = []
        texts = []
        if self.peaks_find_plot:
            if self.ranging:
                ion = self.range_data['ion'].tolist()
                x_peak_loc = self.range_data['mc'].tolist()
                y_peak_loc = self.range_data['peak_count'].tolist()
                for i in range(len(ion)):
                    texts.append(plt.text(x_peak_loc[i], y_peak_loc[i], r'%s' % ion[i], color='black', size=10,
                                          alpha=1))
                    annotes.append(str(i + 1))
            else:
                for i in range(len(x_peaks)):
                    if self.selector == 'range':
                        if i in self.variables.peaks_idx:
                            texts.append(plt.text(x_peaks[i], y_peaks[i], '%s' % '{:.2f}'.format(x_peaks[i]),
                                                  color='black',
                                                  size=10, alpha=1))
                    else:
                        texts.append(
                            plt.text(x_peaks[i], y_peaks[i], '%s' % '{:.2f}'.format(x_peaks[i]), color='black',
                                     size=10, alpha=1))

                    if self.h_line:
                        for i in range(len(self.variables.h_line_pos)):
                            if self.variables.h_line_pos[i] < np.max(self.mc_tof) + 10 and self.variables.h_line_pos[
                                i] > np.max(
                                    self.mc_tof) - 10:
                                plt.axvline(x=self.variables.h_line_pos[i], color='b', linestyle='--', linewidth=2)
                    annotes.append(str(i + 1))
        if self.adjust_label:
            adjust_text(texts, arrowprops=dict(arrowstyle='-', color='red', lw=0.5))
        if self.selector == 'rect':
            data_loadcrop.rectangle_box_selector(ax1, self.variables)
            plt.connect('key_press_event', selectors_data.toggle_selector(self.variables))
        elif self.selector == 'peak':
            af = intractive_point_identification.AnnoteFinder(x_peaks, y_peaks, annotes, self.variables, ax=ax1)
            fig1.canvas.mpl_connect('button_press_event', af)
            zoom_manager = plot_vline_draw.HorizontalZoom(ax1)
        elif self.selector == 'range':
            line_manager = plot_vline_draw.VerticalLineManager(self.variables, ax1, [], [])

    def fit_background(self, x, y):
        def fit_background_function(x, a, b):
            yy = (a / (2 * np.sqrt(b))) * 1 / (np.sqrt(x))
            return yy

        fitresult, _ = curve_fit(fit_background_function, self.background['non_mask'][:, 0],
                                 self.background['non_mask'][:, 1])
        yy = fit_background_function(x, *fitresult)
        return yy

    def plot(self):
        x, y = self.histogram()
        if self.peaks_find:
            peaks, properties, index_peak_max, peak_widths_p = self.find_peaks(x, y)
            peak_widths_f = []
            for i in range(len(peaks)):
                peak_widths_f.append(
                    [y[int(peak_widths_p[2][i])], x[int(peak_widths_p[2][i])], x[int(peak_widths_p[3][i])]])

            if self.background['calculation'] and self.background['plot_no_back']:
                x_peaks = x[peaks]
                y_peaks = y[peaks]
                mask_f = self.calculate_background(x, y)
            else:
                x_peaks = x[peaks]
                y_peaks = y[peaks]
                mask_f = None
            index_max_ini = np.argmax(y_peaks)
            self.variables.max_peak = x_peaks[index_max_ini]
            self.variables.peak = x_peaks
            self.variables.peak_y = y_peaks
        else:
            x_peaks = None
            y_peaks = None
            peak_widths_f = None
            mask_f = None

        fig1, ax1, x, y = self.plot_histogram(x, y)

        if self.background['calculation'] and self.background['plot_no_back']:
            background_ppm = (len(mask_f[mask_f == True]) * 1e6 / len(mask_f)) / np.max(self.mc_tof)
        else:
            background_ppm = None

        self.annotate_plot(ax1, x_peaks, y_peaks, peak_widths_f, background_ppm)
        plt.tight_layout()
        if self.fig_name is not None:
            if self.label == 'mc':
                plt.savefig(self.variables.result_path + "//mc_%s.svg" % self.fig_name, format="svg", dpi=300)
                plt.savefig(self.variables.result_path + "//mc_%s.png" % self.fig_name, format="png", dpi=300)
            elif self.label == 'tof':
                plt.savefig(self.variables.result_path + "//tof_%s.svg" % self.fig_name, format="svg", dpi=300)
                plt.savefig(self.variables.result_path + "//tof_%s.png" % self.fig_name, format="png", dpi=300)
        if self.ranging and self.hist_color_range:
            plt.legend(loc='center right')

        plt.show()
