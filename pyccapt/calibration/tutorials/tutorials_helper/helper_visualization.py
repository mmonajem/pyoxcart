import ipywidgets as widgets
from IPython.display import display, clear_output
from ipywidgets import Output

from pyccapt.calibration.calibration_tools import mc_plot
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
    rotary_fig_save_p3 = widgets.Dropdown(options=[('True', True), ('False', False)])
    element_percentage_p3 = widgets.Textarea(value=element_percentage)
    opacity = widgets.FloatText(value=0.5, min=0, max=1, step=0.1)
    save = widgets.Dropdown(options=[('True', True), ('False', False)], value=False)
    ions_individually_plots = widgets.Dropdown(options=[('True', True), ('False', False)], value=False)
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
                                               rotary_fig_save_p3.value, selected_area_specially_p3.value,
                                               selected_area_temporally_p3, figname_3d.value,
                                               save.value, ions_individually_plots.value)

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

            reconstruction.heatmap(variables, selected_area_specially_ph.value, selected_area_temporally_ph,
                                   element_percentage_ph.value, figure_sie=figure_size, save=save_heatmap.value)
        plot_heatmap_button.disabled = False

    selected_area_specially_pm = widgets.Dropdown(options=[('False', False), ('True', True)])
    selected_area_temporally_pm = widgets.Dropdown(options=[('False', False), ('True', True)])
    peak_find_plot = widgets.Dropdown(options=[('True', True), ('False', False)])
    rangging = widgets.Dropdown(options=[('False', False), ('True', True)])
    bin_size_pm = widgets.FloatText(value=0.1)
    lim_mc_pm = widgets.IntText(value=150)
    prominence = widgets.IntText(value=50)
    distance = widgets.IntText(value=50)
    figname_mc = widgets.Text(value='mc')
    figure_mc_size_x_mc = widgets.FloatText(value=9.0)
    figure_mc_size_y_mc = widgets.FloatText(value=5.0)
    save_mc = widgets.Dropdown(options=[('True', True), ('False', False)], value=False)

    plot_mc_button.on_click(lambda b: plot_mc(b, variables, out))

    def plot_mc(b, variables, out):
        plot_mc_button.disabled = True
        figure_size = (figure_mc_size_x_projection.value, figure_mc_size_y_projection.value)
        with out:
            if selected_area_specially_pm.value:
                variables.selected_z1 = variables.selected_y1
                variables.selected_z2 = variables.selected_y2
                variables.selected_y1 = variables.selected_x1
                variables.selected_y2 = variables.selected_x2
                print('Min x (nm):', variables.selected_x1, 'Max x (nm):', variables.selected_x2)
                print('Min y (nm):', variables.selected_y1, 'Max y (nm):', variables.selected_y2)
                print('Min z (nm):', variables.selected_z1, 'Max z (nm):', variables.selected_z2)

            mc_plot.hist_plot(variables, bin_size_pm.value, log=True, target='mc', mode='normal',
                              prominence=prominence.value, distance=distance.value, percent=50, selector='rect',
                              figname=figname_mc.value, lim=lim_mc_pm.value,
                              peaks_find_plot=peak_find_plot.value, range_plot=rangging.value,
                              selected_area_specially=selected_area_specially_pm.value,
                              selected_area_temporally=selected_area_temporally_pm.value,
                              print_info=False, figure_size=figure_size, save_fig=save_mc.value)

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
                                      x_or_y_pp.value,
                                      figure_size, figname_p.value, save_projection.value)
        plot_projection_button.disabled = False

    clear_button.on_click(lambda b: clear(b, out))

    def clear(b, out):
        with out:
            clear_output(True)
            print('')

    tab1 = widgets.VBox([
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
    tab2 = widgets.VBox([
        widgets.HBox([widgets.Label(value='Selected specially:', layout=label_layout), selected_area_specially_p3]),
        widgets.HBox([widgets.Label(value='Selected temporally:', layout=label_layout), selected_area_temporally_p3]),
        widgets.HBox([widgets.Label(value='Rotary save:', layout=label_layout), rotary_fig_save_p3]),
        widgets.HBox([widgets.Label(value='Element percentage:', layout=label_layout), element_percentage_p3]),
        widgets.HBox([widgets.Label(value='Opacity:', layout=label_layout), opacity]),
		widgets.HBox([widgets.Label(value='Fig name:', layout=label_layout), figname_3d]),
        widgets.HBox([widgets.Label(value='Save fig:', layout=label_layout), save]),
        widgets.HBox([widgets.Label(value='Ions individually plots:', layout=label_layout), ions_individually_plots]),
        widgets.HBox([plot_3d_button, clear_button]),
    ])
    tab3 = widgets.VBox([
        widgets.HBox([widgets.Label(value="Selected specially:", layout=label_layout), selected_area_specially_pm]),
        widgets.HBox([widgets.Label(value="Selected temporally:", layout=label_layout), selected_area_temporally_pm]),
        widgets.HBox([widgets.Label(value="Peak find:", layout=label_layout), peak_find_plot]),
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
    tab4 = widgets.VBox([
		widgets.HBox([widgets.Label(value='Selected specially:', layout=label_layout), selected_area_specially_ph]),
		widgets.HBox([widgets.Label(value='Selected temporally:', layout=label_layout), selected_area_temporally_ph]),
		widgets.HBox([widgets.Label(value='Element percentage:', layout=label_layout), element_percentage_ph]),
		widgets.HBox([widgets.Label(value='Fig name:', layout=label_layout), figname_heatmap]),
		widgets.HBox([widgets.Label(value='Save fig:', layout=label_layout), save_heatmap]),
		widgets.HBox([widgets.Label(value='Fig size:', layout=label_layout),
					  widgets.HBox([figure_mc_size_x_heatmap, figure_mc_size_y_heatmap])]),
		widgets.HBox([plot_heatmap_button, clear_button]),
		])

    tab = widgets.Tab(children=[tab1, tab2, tab3, tab4])
    tab.set_title(0, 'projection')
    tab.set_title(1, '3d plot')
    tab.set_title(2, 'mc plot')
    tab.set_title(3, 'heatmap plot')

    out = Output()

    display(widgets.VBox(children=[tab]))
    display(out)
