import ipywidgets as widgets
import numpy as np
from IPython.display import display, clear_output
from ipywidgets import Output

from pyccapt.calibration.calibration import calibration, mc_plot

# Define a layout for labels to make them a fixed width
label_layout = widgets.Layout(width='300px')


def initial_calibration(variables, calibration_mode, flight_path_length):
    if calibration_mode.value == 'tof_calib':
        v_dc = variables.data['high_voltage (V)'].to_numpy()
        t = variables.data['t (ns)'].to_numpy()
        xDet = variables.data['x_det (cm)'].to_numpy() * 1E-2
        yDet = variables.data['y_det (cm)'].to_numpy() * 1E-2
        flightPathLength = flight_path_length * 1E-3
        flightPathLength = xDet ** 2 + yDet ** 2 + flightPathLength ** 2
        ini_calib_factor_flight_path = flightPathLength / np.mean(flightPathLength)
        ini_calib_factor_voltage = v_dc / np.median(v_dc)
        variables.dld_t_calib = t * ini_calib_factor_flight_path * ini_calib_factor_voltage

    elif calibration_mode.value == 'mc_calib':
        print('initial mc calibration is not needed when calibrating directly the mc')

def reset_back_on_click(variables, calibration_mode):
    if calibration_mode.value == 'tof_calib':
        variables.dld_t_calib = np.copy(variables.dld_t_calib_backup)
    elif calibration_mode.value == 'mc_calib':
        variables.mc_calib = np.copy(variables.mc_calib_backup)


def save_on_click(variables, calibration_mode):
    if calibration_mode.value == 'tof_calib':
        variables.dld_t_calib_backup = np.copy(variables.dld_t_calib)
    elif calibration_mode.value == 'mc_calib':
        variables.mc_calib_backup = np.copy(variables.mc_calib)


def clear_plot_on_click(out):
    with out:
        out.clear_output()


def call_voltage_bowl_calibration(variables, det_diam, flight_path_length):
    out = Output()
    out_status = Output()

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

    auto_button = widgets.Button(
        description='auto calibration',
        layout=label_layout
    )
    initial_calib_button = widgets.Button(
        description='initial calibration',
        layout=label_layout
    )
    calibration_mode = widgets.Dropdown(
        options=[('mass_to_charge', 'mc_calib'), ('time_of_flight', 'tof_calib')],
        description='calibration mode:')

    def sample_size_v_set(sample_size_v):
        # Create a button widget to voltage correction function
        if calibration_mode.value == 'tof_calib':
            lim_tof.value = variables.max_tof
        elif calibration_mode.value == 'mc_calib':
            lim_tof.value = 400
        mc_plot.hist_plot(variables, bin_size.value, log=True, target=calibration_mode.value, mode='normal',
                          prominence=prominence.value, distance=distance.value, percent=percent.value,
                          selector='rect', figname=index_fig.value, lim=lim_tof.value, save_fig=save.value,
                          peaks_find_plot=plot_peak.value, draw_calib_rect=True, print_info=False, mrp_all=False,
                          figure_size=(figure_mc_size_x.value, figure_mc_size_y.value), plot_show=False)

        if calibration_mode.value == 'tof_calib':
            mask_temporal = np.logical_and(
                (variables.dld_t_calib > variables.selected_x1),
                (variables.dld_t_calib < variables.selected_x2)
            )
        elif calibration_mode.value == 'mc_calib':
            mask_temporal = np.logical_and(
                (variables.mc_calib > variables.selected_x1),
                (variables.mc_calib < variables.selected_x2)

            )
        sample_size = int(len(variables.dld_high_voltage[mask_temporal]) / 100)
        sample_size_v.value = sample_size

    calibration_mode.observe(lambda change: sample_size_v_set(sample_size_v), names='value')

    clear_plot = widgets.Button(description="clear plots", layout=label_layout)

    plot_button.on_click(lambda b: hist_plot(b, variables, out, calibration_mode))
    plot_stat_button.on_click(lambda b: stat_plot(b, variables, calibration_mode, out))
    reset_back_button.on_click(lambda b: reset_back_on_click(variables, calibration_mode))
    save_button.on_click(lambda b: save_on_click(variables, calibration_mode))
    vol_button.on_click(lambda b: vol_correction(b, variables, out, out_status, calibration_mode))
    bowl_button.on_click(lambda b: bowl_correction(b, variables, out, out_status, calibration_mode))
    clear_plot.on_click(lambda b: clear_plot_on_click(out))
    auto_button.on_click(lambda b: automatic_calibration(b, variables, out, out_status, calibration_mode))
    initial_calib_button.on_click(lambda b: initial_calibration(variables, calibration_mode, flight_path_length))

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
                              peaks_find_plot=plot_peak.value, draw_calib_rect=True, print_info=True, mrp_all=True,
                              figure_size=figure_size)
        plot_button.disabled = False

    plot_button.click()

    sample_size_v = widgets.IntText(value=10000, description='sample size:', layout=label_layout)
    sample_size_v_set(sample_size_v)


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
    maximum_cal_method_v = widgets.Dropdown(
        options=[('mean', 'mean'), ('histogram', 'histogram'), ('median', 'median')],
        description='peak max:',
        layout=label_layout
    )
    maximum_sample_method_v = widgets.Dropdown(
        options=[('histogram', 'histogram'), ('mean', 'mean'), ('median', 'median')],
        description='sample max:',
        layout=label_layout
    )
    apply_v = widgets.Dropdown(
        options=[('all', 'all'), ('voltage', 'voltage'), ('voltage_temporal', 'voltage_temporal')],
        description='apply mode:',
        layout=label_layout
    )

    noise_remove_v = widgets.Dropdown(
        options=[('False', False), ('True', True)],
        description='noise remove:',
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
                    print('----------------Voltage Calibration-------------------')
                    figure_size = (figure_v_size_x.value, figure_v_size_y.value)
                    sample_size_p = sample_size_v.value
                    index_fig_p = index_fig_v.value
                    plot_p = plot_v.value
                    save_p = save_v.value
                    mode_p = mode_v.value
                    maximum_cal_method_p = maximum_cal_method_v.value
                    maximum_sample_method_p = maximum_sample_method_v.value
                    noise_remove_p = noise_remove_v.value
                    if calibration_mode.value == 'tof_calib':
                        calibration_mode_t = 'tof'
                    elif calibration_mode.value == 'mc_calib':
                        calibration_mode_t = 'mc'
                    calibration.voltage_corr_main(variables.dld_high_voltage, variables, sample_size=sample_size_p,
                                                  calibration_mode=calibration_mode_t,
                                                  index_fig=index_fig_p, plot=plot_p, save=save_p,
                                                  apply_local=apply_v.value, mode=mode_p,
                                                  maximum_cal_method=maximum_cal_method_p,
                                                  noise_remove=noise_remove_p,
                                                  maximum_sample_method=maximum_sample_method_p,
                                                  fig_size=figure_size)
            pb_vol.value = "<b>Finished</b>"
        vol_button.disabled = False

    # Create a button widget to bowl correction function
    sample_size_b = int(det_diam / 8)
    # Check if the rounded number is even
    if sample_size_b % 2 == 0:
        # If even, adjust to the nearest odd number
        sample_size_b = sample_size_b - 1
    else:
        pass

    sample_size_b = widgets.IntText(value=sample_size_b, description='sample size:', layout=label_layout)
    fit_mode_b = widgets.Dropdown(options=[('curve_fit', 'curve_fit'), ('hemisphere_fit', 'hemisphere_fit')],
                                  description='fit mode:', layout=label_layout)
    index_fig_b = widgets.IntText(value=1, description='fig index:', layout=label_layout)
    maximum_cal_method_b = widgets.Dropdown(
        options=[('mean', 'mean'), ('histogram', 'histogram')],
        description='peak max:',
        layout=label_layout
    )
    maximum_sample_method_b = widgets.Dropdown(
        options=[('histogram', 'histogram'), ('mean', 'mean')],
        description='sample max:',
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
                fit_mode_p = fit_mode_b.value
                index_fig_p = index_fig_b.value
                plot_p = plot_b.value
                save_p = save_b.value
                maximum_cal_method_p = maximum_cal_method_b.value
                maximum_sample_method_p = maximum_sample_method_b.value
                figure_size = (figure_b_size_x.value, figure_b_size_y.value)
                if calibration_mode.value == 'tof_calib':
                    calibration_mode_t = 'tof'
                elif calibration_mode.value == 'mc_calib':
                    calibration_mode_t = 'mc'
                with out:
                    print('------------------Bowl Calibration---------------------')
                    calibration.bowl_correction_main(variables.dld_x_det, variables.dld_y_det,
                                                     variables.dld_high_voltage,
                                                     variables, det_diam,
                                                     sample_size=sample_size_p, fit_mode=fit_mode_p,
                                                     maximum_cal_method=maximum_cal_method_p,
                                                     maximum_sample_method=maximum_sample_method_p,
                                                     apply_local=apply_b.value, fig_size=figure_size,
                                                     calibration_mode=calibration_mode_t, index_fig=index_fig_p,
                                                     plot=plot_p, save=save_p)

            pb_bowl.value = "<b>Finished</b>"
        bowl_button.disabled = False

    def stat_plot(b, variables, calibration_mode, out):
        if calibration_mode.value == 'tof_calib':
            calibration_mode_t = 'tof'
        elif calibration_mode.value == 'mc_calib':
            calibration_mode_t = 'mc'
        with out:
            clear_output(True)
            calibration.plot_selected_statistic(variables, bin_fdm.value, index_fig.value,
                                                calibration_mode=calibration_mode_t, save=True)

    def automatic_calibration(b, variables, out, out_status, calibration_mode):

        auto_button.disabled = True
        counter = 1
        try_counter = 0
        index_fig_val = index_fig.value
        continue_calibration = True
        mrp_last = 0
        if calibration_mode.value == 'tof_calib':
            back_tof_mc = np.copy(variables.dld_t_calib)
        elif calibration_mode.value == 'mc_calib':
            back_tof_mc = np.copy(variables.mc_calib)
        while continue_calibration:
            with out:
                # if calibration_mode.value == 'tof_calib' and counter == 1:
                #     print('Initial calibration')
                #     initial_calibration(variables, calibration_mode, flight_path_length)
                print('=======================================================')
                print('Starting calibration number %s' % counter)
                figure_size = (figure_mc_size_x.value, figure_mc_size_y.value)
                mrp = mc_plot.hist_plot(variables, bin_size.value, log=True, target=calibration_mode.value, mode='normal',
                                  prominence=prominence.value, distance=distance.value, percent=percent.value,
                                        selector='rect', figname=index_fig_val, lim=lim_tof.value, save_fig=save.value,
                                  peaks_find_plot=plot_peak.value, print_info=False, figure_size=figure_size,
                                  plot_show=False)
                print('The MRPs at (0.5, 0.1, 0.01) are:', mrp)

                counter += 1
                index_fig_val += 1
                if abs(mrp_last - mrp[0]) < 10 or counter > 15:
                    try_counter += 1
                    if try_counter == 2:
                        print('*********************************************************')
                        print('Calibration is not improving, stopping', try_counter)
                        print('*********************************************************')
                        continue_calibration = False
                        continue
                else:
                    try_counter = 0


            vol_correction(variables, out, out_status, calibration_mode)
            bowl_correction(variables, out, out_status, calibration_mode)


            if mrp_last < mrp[0]:
                if calibration_mode.value == 'tof_calib':
                    variables.dld_t_calib = np.copy(back_tof_mc)
                elif calibration_mode.value == 'mc_calib':
                    variables.mc_calib = np.copy(back_tof_mc)
            mrp_last = mrp[0]
            if calibration_mode.value == 'tof_calib':
                back_tof_mc = np.copy(variables.dld_t_calib)
            elif calibration_mode.value == 'mc_calib':
                back_tof_mc = np.copy(variables.mc_calib)
        auto_button.disabled = False
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

    bin_fdm = widgets.IntText(value=256, description='bin FDM:', layout=label_layout)




    # Create the layout with three columns
    column11 = widgets.VBox([bin_size, prominence, distance, lim_tof, percent, bin_fdm, plot_peak, index_fig, save,
                             figure_mc_size_x, figure_mc_size_y])
    column12 = widgets.VBox([plot_button, auto_button, initial_calib_button, save_button, reset_back_button, clear_plot,
                             plot_stat_button])
    column22 = widgets.VBox([sample_size_b, fit_mode_b, index_fig_b, maximum_cal_method_b, maximum_sample_method_b,
                             apply_b, plot_b, save_b, figure_b_size_x, figure_b_size_y])
    column21 = widgets.VBox([bowl_button, pb_bowl])
    column33 = widgets.VBox([sample_size_v, index_fig_v, mode_v, apply_v, noise_remove_v, maximum_cal_method_v,
                             maximum_sample_method_v, plot_v, save_v, figure_v_size_x, figure_v_size_y])
    column32 = widgets.VBox([vol_button, pb_vol])
    column34 = widgets.VBox([calibration_mode])

    # Create the overall layout by arranging the columns side by side
    layout1 = widgets.HBox([column11, column22, column33, column34])
    layout2 = widgets.HBox([column12, column21, column32])

    layout = widgets.VBox([layout1, layout2])

    # Display the layout
    display(layout)

    out = Output()
    display(out)