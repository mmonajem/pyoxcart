import ipywidgets as widgets
import numpy as np
from IPython.display import display, clear_output
from ipywidgets import Output

from pyccapt.calibration.calibration_tools import calibration, mc_plot

# Define a layout for labels to make them a fixed width
label_layout = widgets.Layout(width='300px')


def reset_back_on_click(variables):
    variables.dld_t_calib = np.copy(variables.dld_t_calib_backup)
    variables.mc_calib = np.copy(variables.mc_calib_backup)



def save_on_click(variables):
    variables.dld_t_calib_backup = np.copy(variables.dld_t_calib)


def clear_plot_on_click(out):
    with out:
        out.clear_output()


def call_voltage_bowl_calibration(variables, det_diam, calibration_mode):
    out = Output()
    out_status = Output()
    # Define widgets and labels for histplot function
    bin_size = widgets.FloatText(value=0.1, description='bin size:', layout=label_layout)
    prominence = widgets.IntText(value=100, description='peak prominance:', layout=label_layout)
    distance = widgets.IntText(value=500, description='peak distance:', layout=label_layout)
    lim_tof = widgets.IntText(value=variables.max_tof, description='lim tof/mc:', layout=label_layout)
    percent = widgets.IntText(value=50, description='percent MRP:', layout=label_layout)
    index_fig = widgets.IntText(value=1, description='fig save index:', layout=label_layout)
    plot_peak = widgets.Dropdown(
        options=[('True', True), ('False', False)],
        description='plot peak',
        layout=label_layout
    )
    save = widgets.Dropdown(
        options=[('False', False), ('True', True)],
        description='save fig:',
        layout=label_layout
    )
    figure_mc_size_x = widgets.FloatText(value=9.0, description="Fig. size W:", layout=label_layout)
    figure_mc_size_y = widgets.FloatText(value=5.0, description="Fig. size H:", layout=label_layout)

    def hist_plot(b, variables, out, calibration_mode):
        plot_button.disabled = True
        figure_size = (figure_mc_size_x.value, figure_mc_size_y.value)
        with out:
            out.clear_output()
            mc_plot.hist_plot(variables, bin_size.value, log=True, target=calibration_mode.value, mode='normal',
                              prominence=prominence.value, distance=distance.value, percent=percent.value,
                              selector='rect', figname=index_fig.value, lim=lim_tof.value, save_fig=save.value,
                              peaks_find_plot=plot_peak.value, print_info=False, figure_size=figure_size)
        plot_button.disabled = False

    # Create a button widget to voltage correction function
    sample_size_v = widgets.IntText(value=100, description='sample size:', layout=label_layout)
    index_fig_v = widgets.IntText(value=1, description='fig index:', layout=label_layout)
    plot_v = widgets.Dropdown(
        options=[('False', False), ('True', True)],
        description='plot fig:',
        layout=label_layout
    )
    save_v = widgets.Dropdown(
        options=[('False', False), ('True', True)],
        description='save fig:',
        layout=label_layout
    )
    mode_v = widgets.Dropdown(
        options=[('ion_seq', 'ion_seq'), ('voltage', 'voltage')],
        description='sample mode:',
        layout=label_layout
    )
    peak_mode = widgets.Dropdown(
        options=[('peak', 'peak'), ('mean', 'mean'), ('median', 'median')],
        description='peak mode:',
        layout=label_layout
    )
    num_cluster = widgets.IntText(value=1, description='num_cluster:', layout=label_layout)
    apply_v = widgets.Dropdown(
        options=[('all', 'all'), ('voltage', 'voltage'), ('voltage_temporal', 'voltage_temporal')],
        description='apply mode:',
        layout=label_layout
    )
    figure_v_size_x = widgets.FloatText(value=5.0, description="Fig. size W:", layout=label_layout)
    figure_v_size_y = widgets.FloatText(value=5.0, description="Fig. size H:", layout=label_layout)

    def vol_correction(b, variables, out, out_status, calibration_mode):
        vol_button.disabled = True
        with out_status:
            out_status.clear_output()
            pb_vol.value = "<b>Starting...</b>"
            if variables.selected_x1 == 0 or variables.selected_x2 == 0:
                print('Please first select a peak')
            else:
                print('Selected mc ranges are: (%s, %s)' % (variables.selected_x1, variables.selected_x2))
                with out:
                    figure_size = (figure_v_size_x.value, figure_v_size_y.value)
                    sample_size_p = sample_size_v.value
                    index_fig_p = index_fig_v.value
                    plot_p = plot_v.value
                    save_p = save_v.value
                    mode_p = mode_v.value
                    peak_mode_p = peak_mode.value
                    calibration.voltage_corr_main(variables.dld_high_voltage, variables, sample_size=sample_size_p,
                                                  calibration_mode=calibration_mode.value,
                                                  index_fig=index_fig_p, plot=plot_p, save=save_p,
                                                  apply_local=apply_v.value,
                                                  num_cluster=num_cluster.value, mode=mode_p, peak_mode=peak_mode_p,
                                                  fig_size=figure_size)
            pb_vol.value = "<b>Finished</b>"
        vol_button.disabled = False

    # Create a button widget to bowl correction function
    sample_size_b = widgets.IntText(value=11, description='sample size:', layout=label_layout)
    index_fig_b = widgets.IntText(value=1, description='fig index:', layout=label_layout)
    maximum_cal_method_b = widgets.Dropdown(
        options=[('mean', 'mean'), ('histogram', 'histogram')],
        description='calib method:',
        layout=label_layout
    )
    plot_b = widgets.Dropdown(
        options=[('False', False), ('True', True)],
        description='plot fig:',
        layout=label_layout
    )

    save_b = widgets.Dropdown(
        options=[('False', False), ('True', True)],
        description='save fig:',
        layout=label_layout
    )
    apply_b = widgets.Dropdown(
        options=[('all', 'all'), ('temporal', 'temporal'), ],
        description='apply mode:',
        layout=label_layout
    )

    figure_b_size_x = widgets.FloatText(value=5.0, description="Fig. size W:", layout=label_layout)
    figure_b_size_y = widgets.FloatText(value=5.0, description="Fig. size H:", layout=label_layout)

    def bowl_correction(b, variables, out, out_status, calibration_mode):
        bowl_button.disabled = True
        with out_status:
            out_status.clear_output()
            pb_bowl.value = "<b>Starting...</b>"
            if variables.selected_x1 == 0 or variables.selected_x2 == 0:
                print('Please first select a peak')
            else:
                print('Selected mc ranges are: (%s, %s)' % (variables.selected_x1, variables.selected_x2))
                sample_size_p = sample_size_b.value
                index_fig_p = index_fig_b.value
                plot_p = plot_b.value
                save_p = save_b.value
                maximum_cal_method_p = maximum_cal_method_b.value
                figure_size = (figure_b_size_x.value, figure_b_size_y.value)
                with out:
                    calibration.bowl_correction_main(variables.dld_x_det, variables.dld_y_det,
                                                     variables.dld_high_voltage,
                                                     variables, det_diam.value,
                                                     sample_size=sample_size_p, maximum_cal_method=maximum_cal_method_p,
                                                     apply_local=apply_b.value, fig_size=figure_size,
                                                     calibration_mode=calibration_mode.value, index_fig=index_fig_p,
                                                     plot=plot_p, save=save_p)

            pb_bowl.value = "<b>Finished</b>"
        bowl_button.disabled = False

    def stat_plot(b, variables, out):
        with out:
            clear_output(True)
            calibration.plot_selected_statistic(variables, bin_fdm.value, index_fig.value, calibration_mode='tof',
                                                save=True)

    # Create a button widget to trigger the function
    pb_bowl = widgets.HTML(
        value=" ",
        placeholder='Status:',
        description='Status:',
        layout=label_layout
    )
    pb_vol = widgets.HTML(
        value=" ",
        placeholder='Status:',
        description='Status:',
        layout=label_layout
    )
    plot_button = widgets.Button(
        description='plot hist',
        layout=label_layout
    )
    plot_stat_button = widgets.Button(
        description='plot stat',
        layout=label_layout
    )
    reset_back_button = widgets.Button(
        description='reset back correction',
        layout=label_layout
    )
    save_button = widgets.Button(
        description='save correction',
        layout=label_layout
    )
    bowl_button = widgets.Button(
        description='bowl correction',
        layout=label_layout
    )
    vol_button = widgets.Button(
        description='voltage correction',
        layout=label_layout
    )
    bin_fdm = widgets.IntText(value=256, description='bin FDM:', layout=label_layout)

    clear_plot = widgets.Button(description="clear plots", layout=label_layout)

    plot_button.on_click(lambda b: hist_plot(b, variables, out, calibration_mode))
    plot_stat_button.on_click(lambda b: stat_plot(b, variables, out))
    reset_back_button.on_click(lambda b: reset_back_on_click(variables))
    save_button.on_click(lambda b: save_on_click(variables))
    vol_button.on_click(lambda b: vol_correction(b, variables, out, out_status, calibration_mode))
    bowl_button.on_click(lambda b: bowl_correction(b, variables, out, out_status, calibration_mode))
    clear_plot.on_click(lambda b: clear_plot_on_click(out))

    # Create the layout with three columns
    column11 = widgets.VBox([bin_size, prominence, distance, lim_tof, percent, bin_fdm, plot_peak, index_fig, save,
                             figure_mc_size_x, figure_mc_size_y])
    column12 = widgets.VBox([plot_button, save_button, reset_back_button, clear_plot, plot_stat_button])
    column22 = widgets.VBox([sample_size_b, index_fig_b, maximum_cal_method_b, apply_b, plot_b, save_b, figure_b_size_x,
                             figure_b_size_y])
    column21 = widgets.VBox([bowl_button, pb_bowl])
    column33 = widgets.VBox([sample_size_v, index_fig_v, mode_v, apply_v, num_cluster, peak_mode, plot_v, save_v,
                             figure_v_size_x, figure_v_size_y])
    column32 = widgets.VBox([vol_button, pb_vol])

    # Create the overall layout by arranging the columns side by side
    layout1 = widgets.HBox([column11, column22, column33])
    layout2 = widgets.HBox([column12, column21, column32])

    layout = widgets.VBox([layout1, layout2])

    # Display the layout
    display(layout)

    out = Output()
    display(out)