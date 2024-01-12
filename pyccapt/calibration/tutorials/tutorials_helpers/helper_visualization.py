import json

import ipywidgets as widgets
import matplotlib.colors as mcolors
from IPython.display import display, clear_output, HTML
from ipywidgets import Output

from pyccapt.calibration.calibration_tools import mc_plot, ion_selection
from pyccapt.calibration.data_tools import data_loadcrop
from pyccapt.calibration.reconstructions import reconstruction

# Define a layout for labels to make them a fixed width
label_layout = widgets.Layout(width='200px')


def call_visualization(variables):
    plot_3d_button = widgets.Button(
        description='plot 3D',
    )
    plot_heatmap_button = widgets.Button(
        description='plot heatmap',
    )
    plot_mc_button = widgets.Button(
        description='plot mc',
    )
    plot_projection_button = widgets.Button(
        description='plot projection',
    )

    clear_button = widgets.Button(
        description='Clear plots',
    )

    if variables.range_data.empty:
        element_percentage = str([0.01])
    else:
        element_percentage = [0.01] * len(variables.range_data['element'].tolist())
        element_percentage = str(element_percentage)

    figname_3d = widgets.Text(value='3d_plot')
    selected_area_specially_p3 = widgets.Dropdown(options=[('False', False), ('True', True)])
    selected_area_temporally_p3 = widgets.Dropdown(options=[('False', False), ('True', True)])
    rotary_fig_save_p3 = widgets.Dropdown(options=[('False', False), ('True', True)])
    element_percentage_p3 = widgets.Textarea(value=element_percentage)
    opacity = widgets.FloatText(value=0.5, min=0, max=1, step=0.1)
    save_3d = widgets.Dropdown(options=[('True', True), ('False', False)], value=False)
    ions_individually_plots = widgets.Dropdown(options=[('True', True), ('False', False)], value=False)
    make_gif_p3 = widgets.Dropdown(options=[('True', True), ('False', False)], value=False)
    plot_3d_button.on_click(lambda b: plot_3d(b, variables, out))

    def plot_3d(b, variables, out):
        plot_3d_button.disabled = True
        with out:
            if selected_area_specially_p3.value:
                variables.selected_z1 = variables.selected_y1
                variables.selected_z2 = variables.selected_y2
                variables.selected_y1 = variables.selected_x1
                variables.selected_y2 = variables.selected_x2
                print('Min x (nm):', variables.selected_x1, 'Max x (nm):', variables.selected_x2)
                print('Min y (nm):', variables.selected_y1, 'Max y (nm):', variables.selected_y2)
                print('Min z (nm):', variables.selected_z1, 'Max z (nm):', variables.selected_z2)

            reconstruction.reconstruction_plot(variables, element_percentage_p3.value, opacity.value,
                                               rotary_fig_save_p3.value, figname_3d.value,
                                               save_3d.value, make_gif_p3.value, selected_area_specially_p3.value,
                                               selected_area_temporally_p3.value, ions_individually_plots.value)


        plot_3d_button.disabled = False

    selected_area_specially_ph = widgets.Dropdown(options=[('False', False), ('True', True)])
    selected_area_temporally_ph = widgets.Dropdown(options=[('False', False), ('True', True)])
    element_percentage_ph = widgets.Textarea(value=element_percentage)
    figname_heatmap = widgets.Text(value='heatmap')
    save_heatmap = widgets.Dropdown(options=[('True', True), ('False', False)], value=False)
    figure_mc_size_x_heatmap = widgets.FloatText(value=5.0)
    figure_mc_size_y_heatmap = widgets.FloatText(value=5.0)
    plot_heatmap_button.on_click(lambda b: plot_heatmap(b, variables, out))

    def plot_heatmap(b, variables, out):
        plot_heatmap_button.disabled = True
        figure_size = (figure_mc_size_x_heatmap.value, figure_mc_size_y_heatmap.value)
        with out:
            if selected_area_specially_pm.value:
                variables.selected_z1 = variables.selected_y1
                variables.selected_z2 = variables.selected_y2
                variables.selected_y1 = variables.selected_x1
                variables.selected_y2 = variables.selected_x2
                print('Min x (nm):', variables.selected_x1, 'Max x (nm):', variables.selected_x2)
                print('Min y (nm):', variables.selected_y1, 'Max y (nm):', variables.selected_y2)
                print('Min z (nm):', variables.selected_z1, 'Max z (nm):', variables.selected_z2)
            reconstruction.heatmap(variables, selected_area_specially_ph.value, selected_area_temporally_ph.value,
                                   element_percentage_ph.value, figname_heatmap.value, figure_sie=figure_size,
                                   save=save_heatmap.value)
        plot_heatmap_button.disabled = False

    selected_area_specially_pm = widgets.Dropdown(options=[('False', False), ('True', True)])
    selected_area_temporally_pm = widgets.Dropdown(options=[('False', False), ('True', True)])
    peak_find_plot = widgets.Dropdown(options=[('True', True), ('False', False)])
    peaks_find = widgets.Dropdown(options=[('True', True), ('False', False)])
    rangging = widgets.Dropdown(options=[('True', True), ('False', False)])
    target_mode = widgets.Dropdown(options=[('mc_c', 'mc_c'), ('tof_c', 'tof_c'), ('mc', 'mc'), ('tof', 'tof')])
    bin_size_pm = widgets.FloatText(value=0.1)
    lim_mc_pm = widgets.IntText(value=150)
    prominence = widgets.IntText(value=50)
    distance = widgets.IntText(value=50)
    figname_mc = widgets.Text(value='mc')
    figure_mc_size_x_mc = widgets.FloatText(value=9.0)
    figure_mc_size_y_mc = widgets.FloatText(value=5.0)
    save_mc = widgets.Dropdown(options=[('True', True), ('False', False)], value=False)
    plot_ranged_ions = widgets.Dropdown(options=[('False', False), ('True', True)], value=False)

    points_per_frame_anim = widgets.IntText(value=50000)
    selected_area_temporally_anim = widgets.Dropdown(options=[('False', False), ('True', True)])
    selected_area_specially_anim = widgets.Dropdown(options=[('False', False), ('True', True)])
    figname_anim = widgets.Text(value='detector_animation')
    figure_size_x_anim = widgets.FloatText(value=5.0)
    figure_size_y_anim = widgets.FloatText(value=5.0)
    ranged_anim = widgets.Dropdown(options=[('False', False), ('True', True)])

    plot_animated_heatmap_button = widgets.Button(description="plot animated heatmap")

    def plot_animated_heatmap(b, variables, out):

        points_per_frame = points_per_frame_anim.value
        selected_area_temporally = selected_area_temporally_anim.value
        selected_area_specially = selected_area_specially_anim.value
        figure_name = figname_anim.value
        figure_size = (figure_size_x_anim.value, figure_size_y_anim.value)
        ranged = ranged_anim.value

        plot_animated_heatmap_button.disabled = True
        with out:
            reconstruction.detector_animation(variables, points_per_frame, ranged, selected_area_specially,
                                              selected_area_temporally, figure_name,
                                              figure_size, save=True)
            display(HTML(variables.animation_detector_html))
        plot_animated_heatmap_button.disabled = False

    plot_animated_heatmap_button.on_click(lambda b: plot_animated_heatmap(b, variables, out))

    selected_area_specially_pm = widgets.Dropdown(options=[('False', False), ('True', True)])
    selected_area_temporally_pm = widgets.Dropdown(options=[('False', False), ('True', True)])
    peak_find_plot = widgets.Dropdown(options=[('True', True), ('False', False)])
    peaks_find = widgets.Dropdown(options=[('True', True), ('False', False)])
    rangging = widgets.Dropdown(options=[('True', True), ('False', False)])
    target_mode = widgets.Dropdown(options=[('mc_c', 'mc_c'), ('tof_c', 'tof_c'), ('mc', 'mc'), ('tof', 'tof')])
    bin_size_pm = widgets.FloatText(value=0.1)
    lim_mc_pm = widgets.IntText(value=150)
    prominence = widgets.IntText(value=50)
    distance = widgets.IntText(value=50)
    figname_mc = widgets.Text(value='mc')
    figure_mc_size_x_mc = widgets.FloatText(value=9.0)
    figure_mc_size_y_mc = widgets.FloatText(value=5.0)
    save_mc = widgets.Dropdown(options=[('True', True), ('False', False)], value=False)
    plot_ranged_ions = widgets.Dropdown(options=[('False', False), ('True', True)], value=False)
    plot_mc_button.on_click(lambda b: plot_mc(b, variables, out))


    def plot_mc(b, variables, out):
        plot_mc_button.disabled = True
        figure_size = (figure_mc_size_x_mc.value, figure_mc_size_y_mc.value)
        with out:
            if selected_area_specially_pm.value:
                variables.selected_z1 = variables.selected_y1
                variables.selected_z2 = variables.selected_y2
                variables.selected_y1 = variables.selected_x1
                variables.selected_y2 = variables.selected_x2
                print('Min x (nm):', variables.selected_x1, 'Max x (nm):', variables.selected_x2)
                print('Min y (nm):', variables.selected_y1, 'Max y (nm):', variables.selected_y2)
                print('Min z (nm):', variables.selected_z1, 'Max z (nm):', variables.selected_z2)

            mc_plot.hist_plot(variables, bin_size_pm.value, log=True, target=target_mode.value, mode='normal',
                              prominence=prominence.value, distance=distance.value, percent=50, selector='rect',
                              figname=figname_mc.value, lim=lim_mc_pm.value, peaks_find=peaks_find.value,
                              peaks_find_plot=peak_find_plot.value, range_plot=rangging.value,
                              selected_area_specially=selected_area_specially_pm.value,
                              selected_area_temporally=selected_area_temporally_pm.value,
                              print_info=False, figure_size=figure_size, save_fig=save_mc.value,
                              plot_ranged_ions=plot_ranged_ions.value)

        plot_mc_button.disabled = False

    element_percentage_pp = widgets.Textarea(value=element_percentage)
    selected_area_specially_pp = widgets.Dropdown(options=[('False', False), ('True', True)])
    selected_area_temporally_pp = widgets.Dropdown(options=[('False', False), ('True', True)])
    x_or_y_pp = widgets.Dropdown(options=['x', 'y'], value='x')
    figname_p = widgets.Text(value='projection')
    save_projection = widgets.Dropdown(options=[('True', True), ('False', False)], value=False)
    figure_mc_size_x_projection = widgets.FloatText(value=5.0)
    figure_mc_size_y_projection = widgets.FloatText(value=5.0)

    plot_projection_button.on_click(lambda b: plot_projection(b, variables, out))

    def plot_projection(b, variables, out):
        plot_projection_button.disabled = True
        figure_size = (figure_mc_size_x_projection.value, figure_mc_size_y_projection.value)
        with out:
            if selected_area_specially_pp.value:
                variables.selected_z1 = variables.selected_y1
                variables.selected_z2 = variables.selected_y2
                variables.selected_y1 = variables.selected_x1
                variables.selected_y2 = variables.selected_x2
                print('Min x (nm):', variables.selected_x1, 'Max x (nm):', variables.selected_x2)
                print('Min y (nm):', variables.selected_y1, 'Max y (nm):', variables.selected_y2)
                print('Min z (nm):', variables.selected_z1, 'Max z (nm):', variables.selected_z2)

            reconstruction.projection(variables, element_percentage_pp.value, selected_area_specially_pp.value,
                                      selected_area_temporally_pp.value, x_or_y_pp.value,
                                      figname_p.value, figure_size, save_projection.value)
        plot_projection_button.disabled = False

    clear_button.on_click(lambda b: clear(b, out))

    # Define widgets for each parameter
    frac_fdm_widget = widgets.FloatText(value=1.0)
    bins_x_fdm = widgets.IntText(value=256)
    bins_y_fdm = widgets.IntText(value=256)
    figure_size_x_fdm = widgets.FloatText(value=5.0)
    figure_size_y_fdm = widgets.FloatText(value=4.0)
    save_fdm_widget = widgets.Dropdown(options=[('True', True), ('False', False)], value=False)
    figname_fdm_widget = widgets.Text(value='fdm_ini')

    plot_fdm_button = widgets.Button(description="plot")

    first_axis = widgets.Dropdown(options=['x', 'y', 'z'], value='x')
    second_axis = widgets.Dropdown(options=['x', 'y', 'z'], value='y')
    bins_x_2d_hist = widgets.IntText(value=256)
    bins_y_2d_hist = widgets.IntText(value=256)
    percentage_2d_hist = widgets.FloatText(value=1.0)
    selected_area_specially_2d_hist = widgets.Dropdown(options=[('False', False), ('True', True)])
    selected_area_temporally_2d_hist = widgets.Dropdown(options=[('False', False), ('True', True)])
    save_2d_hist = widgets.Dropdown(options=[('True', True), ('False', False)], value=False)
    figname_2d_hist = widgets.Text(value='2d_hist')
    figure_size_x_2d_hist = widgets.FloatText(value=5.0)
    figure_size_y_2d_hist = widgets.FloatText(value=4.0)

    range_1_2d_hist = widgets.Textarea(value='[0,0]')
    range_2_2d_hist = widgets.Textarea(value='[0,0]')

    plot_reconstruction_2d_hist_button = widgets.Button(description="plot")

    def plot_reconstruction_2d_hist(b, variables, out):

        if first_axis.value == 'x' and second_axis.value == 'y':
            x = variables.x
            y = variables.y
        elif first_axis.value == 'y' and second_axis.value == 'x':
            x = variables.y
            y = variables.x
        elif first_axis.value == 'x' and second_axis.value == 'z':
            x = variables.x
            y = variables.z
        elif first_axis.value == 'z' and second_axis.value == 'x':
            x = variables.z
            y = variables.x
        elif first_axis.value == 'y' and second_axis.value == 'z':
            x = variables.y
            y = variables.z
        elif first_axis.value == 'z' and second_axis.value == 'y':
            x = variables.z
            y = variables.y
        else:
            raise ValueError('Invalid axis')

        bins = (bins_x_2d_hist.value, bins_y_2d_hist.value)
        percentage = percentage_2d_hist.value
        plot_reconstruction_2d_hist_button.disabled = True
        xlabel = first_axis.value + ' (nm)'
        ylabel = second_axis.value + ' (nm)'
        figure_name = figname_2d_hist.value + '_' + first_axis.value + '_' + second_axis.value
        save = save_2d_hist.value
        figure_size = (figure_size_x_2d_hist.value, figure_size_y_2d_hist.value)
        selected_area_specially = selected_area_specially_2d_hist.value
        selected_area_temporally = selected_area_temporally_2d_hist.value
        try:
            # Use json.loads to convert the entered string to a list
            range_1 = json.loads(range_1_2d_hist.value)
            range_2 = json.loads(range_2_2d_hist.value)
            if range_1 == [0, 0] or range_2 == [0, 0]:
                range_1 = []
                range_2 = []
        except json.JSONDecodeError:
            # Handle invalid input
            range_1 = []
            range_2 = []
            print(f"Invalid input: {range_1_2d_hist.value} or {range_2_2d_hist.value}")

        with out:  # Capture the output within the 'out' widget
            reconstruction.reconstruction_2d_histogram(variables, x, y, bins,
                                                       selected_area_specially, selected_area_temporally, percentage,
                                                       range_1, range_2,
                                                       xlabel, ylabel, save, figure_name,
                                                       figure_size)
        plot_reconstruction_2d_hist_button.disabled = False

    plot_reconstruction_2d_hist_button.on_click(lambda b: plot_reconstruction_2d_hist(b, variables, out))

    def plot_fdm(b, variables, out):
        plot_fdm_button.disabled = True

        # Get the values from the widgets
        frac = frac_fdm_widget.value
        bins = (bins_x_fdm.value, bins_y_fdm.value)
        figure_size = (figure_size_x_fdm.value, figure_size_y_fdm.value)
        save = save_fdm_widget.value
        figname = figname_fdm_widget.value

        with out:  # Capture the output within the 'out' widget
            # Call the function
            data = variables.data.copy()
            data_loadcrop.plot_crop_fdm(data, variables, bins, frac, True, figure_size,
                                        False, save, figname)

        # Enable the button when the code is finished
        plot_fdm_button.disabled = False

    plot_fdm_button.on_click(lambda b: plot_fdm(b, variables, out))

    # Define widgets and labels for each parameter
    max_tof_mc_widget = widgets.FloatText(value=variables.max_tof)
    frac_mc_widget = widgets.FloatText(value=1.0)
    bins_x_mc = widgets.IntText(value=1200)
    bins_y_mc = widgets.IntText(value=800)
    figure_size_x_mc = widgets.FloatText(value=7.0)
    figure_size_y_mc = widgets.FloatText(value=3.0)
    draw_rect_mc_widget = widgets.fixed(False)
    data_crop_mc_widget = widgets.fixed(True)
    pulse_plot_mc_widget = widgets.Dropdown(options=[('False', False), ('True', True)], value=False)
    dc_plot_mc_widget = widgets.Dropdown(options=[('True', True), ('False', False)], value=True)
    pulse_mode_mc_widget = widgets.Dropdown(options=[('voltage', 'voltage'), ('laser', 'laser')], value='voltage')
    save_mc_widget = widgets.Dropdown(options=[('True', True), ('False', False)], value=False)
    figname_mc_widget = widgets.Text(value='hist_ini')

    plot_experiment_button = widgets.Button(description="plot experiment")

    def plot_experimetns_hitstory(b, variables, out):
        plot_experiment_button.disabled = True
        with out:
            data = variables.data.copy()
            variables = variables
            max_tof = max_tof_mc_widget.value
            frac = frac_mc_widget.value

            # Get the values from the editable widgets and create tuples
            bins = (bins_x_mc.value, bins_y_mc.value)
            figure_size = (figure_size_x_mc.value, figure_size_y_mc.value)

            draw_rect = draw_rect_mc_widget.value
            data_crop = data_crop_mc_widget.value
            pulse_plot = pulse_plot_mc_widget.value
            dc_plot = dc_plot_mc_widget.value
            pulse_mode = pulse_mode_mc_widget.value
            save = save_mc_widget.value
            figname = figname_mc_widget.value

            with out:  # Capture the output within the 'out' widget
                # Call the actual function with the obtained values
                data_loadcrop.plot_crop_experiment_history(data, variables, max_tof, frac, bins, figure_size,
                                                           draw_rect, data_crop, pulse_plot, dc_plot,
                                                           pulse_mode, save, figname)
        plot_experiment_button.disabled = False

    plot_experiment_button.on_click(lambda b: plot_experimetns_hitstory(b, variables, out))

    show_color = widgets.Button(
        description='show color',
    )
    change_color = widgets.Button(
        description='change color',
    )
    row_index = widgets.IntText(value=0, description='index row:')
    color_picker = widgets.ColorPicker(description='Select a color:')

    show_color.on_click(lambda b: show_color_ions(b, variables, out))

    def show_color_ions(b, variables, output):
        with output:
            clear_output(True)
            display(variables.range_data.style.applymap(ion_selection.display_color, subset=['color']))

    change_color.on_click(lambda b: change_color_m(b, variables, out))

    def change_color_m(b, variables, output):
        with output:
            selected_color = mcolors.to_hex(color_picker.value)
            variables.range_data.at[row_index.value, 'color'] = selected_color
            clear_output(True)
            display(variables.range_data.style.applymap(ion_selection.display_color, subset=['color']))

    def clear(b, out):
        with out:
            clear_output(True)
            print('')

    tab1 = widgets.VBox([
        widgets.HBox([widgets.Label(value="Selected specially:", layout=label_layout), selected_area_specially_pm]),
        widgets.HBox([widgets.Label(value="Selected temporally:", layout=label_layout), selected_area_temporally_pm]),
        widgets.HBox([widgets.Label(value="Target:", layout=label_layout), target_mode]),
        widgets.HBox([widgets.Label(value="Peak find:", layout=label_layout), peaks_find]),
        widgets.HBox([widgets.Label(value="Peak find plot:", layout=label_layout), peak_find_plot]),
        widgets.HBox([widgets.Label(value="Plot ions:", layout=label_layout), plot_ranged_ions]),
        widgets.HBox([widgets.Label(value="Rangging:", layout=label_layout), rangging]),
        widgets.HBox([widgets.Label(value="Bins size:", layout=label_layout), bin_size_pm]),
        widgets.HBox([widgets.Label(value="Limit mc:", layout=label_layout), lim_mc_pm]),
        widgets.HBox([widgets.Label(value="Peak prominance:", layout=label_layout), prominence]),
        widgets.HBox([widgets.Label(value="Peak distance:", layout=label_layout), distance]),
        widgets.HBox([widgets.Label(value="Fig name:", layout=label_layout), figname_mc]),
        widgets.HBox([widgets.Label(value="Save fig:", layout=label_layout), save_mc]),
        widgets.HBox([widgets.Label(value="Fig size:", layout=label_layout),
                      widgets.HBox([figure_mc_size_x_mc, figure_mc_size_y_mc])]),

        widgets.HBox([plot_mc_button, clear_button])])
    tab2 = widgets.VBox([
        widgets.HBox([widgets.Label(value='Selected specially:', layout=label_layout), selected_area_specially_p3]),
        widgets.HBox([widgets.Label(value='Selected temporally:', layout=label_layout), selected_area_temporally_p3]),
        widgets.HBox([widgets.Label(value='Element percentage:', layout=label_layout), element_percentage_p3]),
        widgets.HBox([widgets.Label(value='Opacity:', layout=label_layout), opacity]),
        widgets.HBox([widgets.Label(value='Fig name:', layout=label_layout), figname_3d]),
        widgets.HBox([widgets.Label(value='Rotary save:', layout=label_layout), rotary_fig_save_p3]),
        widgets.HBox([widgets.Label(value='Save GIF:', layout=label_layout), make_gif_p3]),
        widgets.HBox([widgets.Label(value='Save fig:', layout=label_layout), save_3d]),
        widgets.HBox([widgets.Label(value='Ions individually plots:', layout=label_layout), ions_individually_plots]),
        widgets.HBox([plot_3d_button, clear_button]),
    ])
    tab3 = widgets.VBox([
        widgets.HBox([widgets.Label(value='Fraction:', layout=label_layout), frac_fdm_widget]),
        widgets.HBox([widgets.Label(value='Bins:', layout=label_layout), widgets.HBox([bins_x_fdm, bins_y_fdm])]),
        widgets.HBox([widgets.Label(value='Fig name:', layout=label_layout), figname_fdm_widget]),
        widgets.HBox([widgets.Label(value='Save:', layout=label_layout), save_fdm_widget]),
        widgets.HBox([widgets.Label(value='Fig size:', layout=label_layout),
                      widgets.HBox([figure_size_x_fdm, figure_size_y_fdm])]),
        widgets.HBox([plot_fdm_button, clear_button]),
    ])

    tab4 = widgets.VBox([
        widgets.HBox([widgets.Label(value='Max TOF:', layout=label_layout), max_tof_mc_widget]),
        widgets.HBox([widgets.Label(value='Fraction:', layout=label_layout), frac_mc_widget]),
        widgets.HBox([widgets.Label(value='Bins:', layout=label_layout), widgets.HBox([bins_x_mc, bins_y_mc])]),
        widgets.HBox([widgets.Label(value='Pulse Plot:', layout=label_layout), pulse_plot_mc_widget]),
        widgets.HBox([widgets.Label(value='DC Plot:', layout=label_layout), dc_plot_mc_widget]),
        widgets.HBox([widgets.Label(value='Pulse Mode:', layout=label_layout), pulse_mode_mc_widget]),
        widgets.HBox([widgets.Label(value='Fig name:', layout=label_layout), figname_mc_widget]),
        widgets.HBox([widgets.Label(value='Save:', layout=label_layout), save_mc_widget]),
        widgets.HBox([widgets.Label(value='Fig size:', layout=label_layout),
                      widgets.HBox([figure_size_x_mc, figure_size_y_mc])]),
        widgets.HBox([plot_experiment_button, clear_button]),
    ])

    tab6 = widgets.VBox([
        widgets.HBox([widgets.Label(value='Points per frame:', layout=label_layout), points_per_frame_anim]),
        widgets.HBox([widgets.Label(value='Ranged:', layout=label_layout), ranged_anim]),
        widgets.HBox([widgets.Label(value='Selected specially:', layout=label_layout), selected_area_specially_anim]),
        widgets.HBox([widgets.Label(value='Selected temporally:', layout=label_layout), selected_area_temporally_anim]),
        widgets.HBox([widgets.Label(value='Fig name:', layout=label_layout), figname_anim]),
        widgets.HBox([widgets.Label(value='Fig size:', layout=label_layout),
                      widgets.HBox([figure_size_x_anim, figure_size_y_anim])]),
        widgets.HBox([plot_animated_heatmap_button, clear_button]),
    ])

    tab5 = widgets.VBox([
        widgets.HBox([widgets.Label(value='Element percentage:', layout=label_layout), element_percentage_pp]),
        widgets.HBox([widgets.Label(value='Selected specially:', layout=label_layout), selected_area_specially_pp]),
        widgets.HBox([widgets.Label(value='Selected temporally:', layout=label_layout), selected_area_temporally_pp]),
        widgets.HBox([widgets.Label(value='X or Y:', layout=label_layout), x_or_y_pp]),
        widgets.HBox([widgets.Label(value='Fig name:', layout=label_layout), figname_p]),
        widgets.HBox([widgets.Label(value='Save fig:', layout=label_layout), save_projection]),
        widgets.HBox([widgets.Label(value='Fig size:', layout=label_layout),
                      widgets.HBox([figure_mc_size_x_projection, figure_mc_size_y_projection])]),
        widgets.HBox([plot_projection_button, clear_button])
    ])

    tab7 = widgets.VBox([
        widgets.HBox([widgets.Label(value='Selected specially:', layout=label_layout), selected_area_specially_ph]),
        widgets.HBox([widgets.Label(value='Selected temporally:', layout=label_layout), selected_area_temporally_ph]),
        widgets.HBox([widgets.Label(value='Element percentage:', layout=label_layout), element_percentage_ph]),
        widgets.HBox([widgets.Label(value='Fig name:', layout=label_layout), figname_heatmap]),
        widgets.HBox([widgets.Label(value='Save fig:', layout=label_layout), save_heatmap]),
        widgets.HBox([widgets.Label(value='Fig size:', layout=label_layout),
                      widgets.HBox([figure_mc_size_x_heatmap, figure_mc_size_y_heatmap])]),
        widgets.HBox([plot_heatmap_button, clear_button]),
    ])

    tab8 = widgets.VBox([
        widgets.HBox([widgets.Label(value='First axis:', layout=label_layout), first_axis]),
        widgets.HBox([widgets.Label(value='Second axis:', layout=label_layout), second_axis]),
        widgets.HBox(
            [widgets.Label(value='Bins:', layout=label_layout), widgets.HBox([bins_x_2d_hist, bins_y_2d_hist])]),
        widgets.HBox([widgets.Label(value='Percentage:', layout=label_layout), percentage_2d_hist]),
        widgets.HBox([widgets.Label(value='Range axis 1:', layout=label_layout), range_1_2d_hist]),
        widgets.HBox([widgets.Label(value='Range axis 2:', layout=label_layout), range_2_2d_hist]),
        widgets.HBox(
            [widgets.Label(value='Selected specially:', layout=label_layout), selected_area_specially_2d_hist]),
        widgets.HBox(
            [widgets.Label(value='Selected temporally:', layout=label_layout), selected_area_temporally_2d_hist]),
        widgets.HBox([widgets.Label(value='Fig name:', layout=label_layout), figname_2d_hist]),
        widgets.HBox([widgets.Label(value='Save:', layout=label_layout), save_2d_hist]),
        widgets.HBox([widgets.Label(value='Fig size:', layout=label_layout),
                      widgets.HBox([figure_size_x_2d_hist, figure_size_y_2d_hist])]),
        widgets.HBox([plot_reconstruction_2d_hist_button, clear_button]),
    ])

    tab9 = widgets.VBox([
        widgets.HBox([widgets.Label(value='Index row:', layout=label_layout), row_index]),
        widgets.HBox([widgets.Label(value='Color:', layout=label_layout), color_picker]),
        widgets.HBox([show_color, change_color]),
    ])

    tab = widgets.Tab(children=[tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9])
    tab.set_title(0, 'mc')
    tab.set_title(1, '3d')
    tab.set_title(2, 'FDM')
    tab.set_title(3, 'Experiment history')
    tab.set_title(4, 'Heatmap')
    tab.set_title(5, 'animated heatmap')
    tab.set_title(6, 'Projection')
    tab.set_title(7, '2D reconstruction histogram')
    tab.set_title(8, 'Color')

    out = Output()

    display(widgets.VBox(children=[tab]))
    display(out)
