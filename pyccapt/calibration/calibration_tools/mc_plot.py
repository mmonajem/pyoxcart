import matplotlib.pyplot as plt
import numpy as np
import pybaselines
from adjustText import adjust_text
from pybaselines import Baseline
from scipy.optimize import curve_fit
from scipy.signal import find_peaks, peak_widths, peak_prominences

from pyccapt.calibration.calibration_tools import intractive_point_identification
from pyccapt.calibration.data_tools import data_loadcrop, plot_vline_draw, selectors_data


def fit_background(x, a, b):
    """
    Calculate the fit function value for the given parameters.

    Args:
        x (array-like): Input array of values.
        a (float): Parameter a.
        b (float): Parameter b.

    Returns:
        array-like: Fit function values corresponding to the input array.
    """
    yy = (a / (2 * np.sqrt(b))) * 1 / (np.sqrt(x))
    return yy


class AptHistPlotter:
    def __init__(self, mc_tof, variables=None):
        self.mc_tof = mc_tof
        self.variables = variables
        self.x = None
        self.y = None
        self.peak_annotates = []
        self.annotates = []
        self.patches = None
        self.peaks = None
        self.properties = None
        self.peak_widths = None
        self.prominences = None
        self.mask_f = None
        self.legend_colors = []

    def find_peaks_and_widths(self, prominence=None, distance=None, percent=50):
        try:
            self.peaks, self.properties = find_peaks(self.y, prominence=prominence, distance=distance, height=0)
            self.peak_widths = peak_widths(self.y, self.peaks, rel_height=(percent / 100), prominence_data=None)
            self.prominences = peak_prominences(self.y, self.peaks, wlen=None)
        except ValueError:
            print('Peak finding failed.')
            self.peaks = None
            self.properties = None
            self.peak_widths = None
            self.prominences = None

    def plot_histogram(self, bin_width=0.1, mode='count', label='mc', log=True, steps='stepfilled', fig_size=(9, 5)):
        # Define the bins
        bins = np.linspace(np.min(self.mc_tof), np.max(self.mc_tof), round(np.max(self.mc_tof) / bin_width))

        # Plot the histogram directly
        self.fig, self.ax = plt.subplots(figsize=fig_size)
        steps = 'stepfilled' if steps == 'stepfilled' else 'bar'

        if mode == 'count':
            self.y, self.x, self.patches = self.ax.hist(self.mc_tof, bins=bins, alpha=0.9, color='slategray', edgecolor='k',
                                        histtype=steps)
        elif mode == 'normalized':
            self.y, self.x, self.patches = self.ax.hist((self.mc_tof / bin_width) / len(self.mc_tof), bins=bins, alpha=0.9,
                                        color='slategray', edgecolor='k', histtype=steps)

        self.ax.set_xlabel('Mass/Charge [Da]' if label == 'mc' else 'Time of Flight [ns]')
        self.ax.set_ylabel('Frequency [cts]')
        self.ax.set_yscale('log' if log else 'linear')
        plt.tight_layout()
        plt.show()

    def plot_range(self, range_data, legend=True):
        colors = range_data['color'].tolist()
        mc_low = range_data['mc_low'].tolist()
        mc_up = range_data['mc_up'].tolist()
        ion = range_data['ion'].tolist()

        for i in range(len(ion)):
            mask = np.logical_and(self.x[:-1] >= mc_low[i], self.x[1:] <= mc_up[i])
            for patch in np.array(self.patches)[mask]:
                patch.set_facecolor(colors[i])

            # Store the labels for the legend
            self.legend_colors.append((r'%s' %ion[i], plt.Rectangle((0, 0), 1, 1, fc=colors[i])))

        if legend:
            self.plot_color_legend()

    def plot_peaks(self, range_data=None, mode='peaks'):

        x_offset = 0.1  # Adjust this value as needed
        y_offset = 10  # Adjust this value as needed
        if range_data is not None:
            ion = range_data['ion'].tolist()
            x_peak_loc = range_data['mc'].tolist()
            y_peak_loc = range_data['peak_count'].tolist()
            for i in range(len(ion)):
                self.peak_annotates.append(plt.text(x_peak_loc[i] + x_offset, y_peak_loc[i] + y_offset,
                                                      r'%s' % ion[i], color='black', size=10, alpha=1))
                self.annotates.append(str(i + 1))
        else:
            for i in range(len(self.peaks)):
                if mode == 'range':
                    if i in self.variables.peaks_idx:
                        self.peak_annotates.append(
                            plt.text(self.x[self.peaks][i] + x_offset, self.y[self.peaks][i] + y_offset,
                                     '%s' % '{:.2f}'.format(self.x[self.peaks][i]), color='black', size=10, alpha=1))
                elif mode == 'peaks':
                    self.peak_annotates.append(
                        plt.text(self.x[self.peaks][i] + x_offset, self.y[self.peaks][i] + y_offset,
                                 '%s' % '{:.2f}'.format(self.x[self.peaks][i]), color='black', size=10, alpha=1))

                self.annotates.append(str(i + 1))

    def selector(self, selector='rect'):
        if selector == 'rect':
            # Connect and initialize rectangle box selector
            data_loadcrop.rectangle_box_selector(self.ax, self.variables)
            plt.connect('key_press_event', selectors_data.toggle_selector(self.variables))
        elif selector == 'peak':
            # connect peak selector
            af = intractive_point_identification.AnnoteFinder(self.x[self.peaks], self.y[self.peaks], self.annotates,
                                                              self.variables, ax=self.ax)
            self.fig.canvas.mpl_connect('button_press_event', af)
            zoom_manager = plot_vline_draw.HorizontalZoom(self.ax)
        elif selector == 'range':
            # connect range selector
            line_manager = plot_vline_draw.VerticalLineManager(self.variables, self.ax, [], [])

    def plot_color_legend(self, loc):
        self.ax.legend([label[1] for label in self.legend_labels], [label[0] for label in self.legend_labels],
                       loc=loc)

    def plot_hist_info_legend(self, label='mc', bin=0.1, background=None, loc='left'):
        index_peak_max = np.argmax(self.prominences)
        print("The peak index for MRP calculation is:", index_peak_max)
        if label == 'mc':
            mrp = '{:.2f}'.format(self.x[self.peaks[index_peak_max]] / (self.x[int(self.peak_widths[3][index_peak_max])] -
                                                              self.x[int(self.peak_widths[2][index_peak_max])]))
            if background is not None:
                txt = 'bin width: %s Da\nnum atoms: %.2f$e^6$\nbackG: %s ppm/Da\nMRP(FWHM): %s' \
                      % (bin, len(self.mc_tof) / 1000000, int(self.background_ppm), mrp)
            else:
                # annotation with range stats
                upperLim = 4.5  # Da
                lowerLim = 3.5  # Da
                mask = np.logical_and((self.x >= lowerLim), (self.x <= upperLim))
                BG4 = np.sum(self.y[np.array(mask[:-1])]) / (upperLim - lowerLim)
                BG4 = BG4 / len(self.mc_tof) * 1E6

                txt = 'bin width: %s Da\nnum atoms: %.2f$e^6$\nBG@4: %s ppm/Da\nMRP(FWHM): %s' \
                      % (bin, (len(self.mc_tof) / 1000000), int(BG4), mrp)

        elif label == 'tof':
            mrp = '{:.2f}'.format(self.x[self.peaks[index_peak_max]] / (self.x[int(self.peak_widths[3][index_peak_max])] -
                                                              self.x[int(self.peak_widths[2][index_peak_max])]))
            if background['calculation'] and background['plot_no_back']:
                txt = 'bin width: %s ns\nnum atoms: %.2f$e^6$\nbackG: %s ppm/ns\nMRP(FWHM): %s' \
                      % (bin, len(self.mc_tof) / 1000000, int(self.background_ppm), mrp)
            else:
                # annotation with range stats
                upperLim = 50.5  # ns
                lowerLim = 49.5  # ns
                mask = np.logical_and((self.x >= lowerLim), (self.x <= upperLim))
                BG50 = np.sum(self.y[np.array(mask[:-1])]) / (upperLim - lowerLim)
                BG50 = BG50 / len(self.mc_tof) * 1E6
                txt = 'bin width: %s ns\nnum atoms: %.2f$e^6$ \nBG@50: %s ppm/ns\nMRP(FWHM): %s' \
                      % (bin, len(self.mc_tof) / 1000000, int(BG50), mrp)

        props = dict(boxstyle='round', facecolor='wheat', alpha=1)
        if loc == 'left':
            self.ax.text(.01, .95, txt, va='top', ma='left', transform=self.ax.transAxes, bbox=props, fontsize=10, alpha=1,
                     horizontalalignment='left', verticalalignment='top')
        elif loc == 'right':
            self.ax.text(.98, .95, txt, va='top', ma='left', transform=self.ax.transAxes, bbox=props, fontsize=10, alpha=1,
                     horizontalalignment='right', verticalalignment='top')

    def plot_horizontal_lines(self):
        for i in range(len(self.variables.h_line_pos)):
            if np.max(self.mc_tof) + 10 > self.variables.h_line_pos[i] > np.max(self.mc_tof) - 10:
                plt.axvline(x=self.variables.h_line_pos[i], color='b', linestyle='--', linewidth=2)

    def plot_background(self, mode, non_peaks=None, lam=5e10, tol=1e-1, max_iter=100, num_std=3, poly_order=5,
                        plot_no_back=True, plot=True, patch=True):

        if mode == 'aspls':
            baseline_fitter = Baseline(x_data=self.bins[:-1])
            fit_1, params_1 = baseline_fitter.aspls(y, lam=lam, tol=tol, max_iter=max_iter)

        if mode == 'fabc':
            fit_2, params_2 = pybaselines.classification.fabc(y, lam=lam,
                                                              num_std=num_std,
                                                              pad_kwargs='edges')
        if mode == 'dietrich':
            fit_2, params_2 = pybaselines.classification.dietrich(y, num_std=num_std)
        if mode == 'cwt_br':
            fit_2, params_2 = pybaselines.classification.cwt_br(y, poly_order=poly_order,
                                                                num_std=num_std,
                                                                tol=tol)
        if mode == 'selective_mask_t':
            if non_peaks is None:
                print('Please give the non peaks')
            else:
                p = np.poly1d(np.polyfit(non_peaks[:, 0], non_peaks[:, 1], 5))
                baseline_handle = self.ax1.plot(self.x, p(self.x), '--')
        if mode == 'selective_mask_mc':
            if non_peaks is None:
                print('Please give the non peaks')
            else:
                fitresult, _ = curve_fit(fit_background, non_peaks[:, 0], non_peaks[:, 1])
                yy = fit_background(self.x, *fitresult)
                self.ax1.plot(self.x, yy, '--')

        if plot_no_back:
            mask_2 = params_2['mask']
            self.mask_f = np.full((len(self.mc_tof)), False)
            for i in range(len(mask_2)):
                if mask_2[i]:
                    step_loc = np.min(self.mc_tof) + bin * i
                    mask_t = np.logical_and((self.mc_tof < step_loc + bin), (self.mc_tof > step_loc))
                    self.mask_f = np.logical_or(self.mask_f, mask_t)
            self.background_ppm = (len(self.mask_f[self.mask_f == True]) * 1e6 / len(self.mask_f)) / np.max(self.mc_tof)

        if plot_no_back:
            if plot:
                self.ax1.plot(self.bins[:-1], fit_2, label='class', color='r')
                ax3 = self.ax1.twiny()
                ax3.axis("off")
                ax3.plot(fit_1, label='aspls', color='black')

            mask_2 = params_2['mask']
            if patch:
                self.ax1.plot(self.bins[:-1][mask_2], self.y[mask_2], 'o', color='orange')[0]

        return self.mask_f

    def adjust_labels(self):
        adjust_text(self.peak_annotates, arrowprops=dict(arrowstyle='-', color='red', lw=0.5))

    def save_fig(self, label, fig_name):
        if label == 'mc':
            plt.savefig(self.variables.result_path + "//mc_%s.svg" % fig_name, format="svg", dpi=300)
            plt.savefig(self.variables.result_path + "//mc_%s.png" % fig_name, format="png", dpi=300)
        elif label == 'tof':
            plt.savefig(self.variables.result_path + "//tof_%s.svg" % fig_name, format="svg", dpi=300)
            plt.savefig(self.variables.result_path + "//tof_%s.png" % fig_name, format="png", dpi=300)