import ipywidgets as widgets
from IPython.display import display, clear_output
from ipywidgets import Output

from pyccapt.calibration.calibration_tools import mc_plot
from pyccapt.calibration.reconstructions import reconstruction


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

	figname_3d = widgets.Text(value='3d_plot', description='fig name')
	selected_area_specially_p3 = widgets.Dropdown(options=[('False', False), ('True', True)],
	                                              description='Selected specially')
	selected_area_temporally_p3 = widgets.Dropdown(options=[('False', False), ('True', True)],
	                                               description='Selected temporally')
	rotary_fig_save_p3 = widgets.Dropdown(options=[('True', True), ('False', False)], description='Rotary save')
	element_percentage_p3 = widgets.Textarea(value=element_percentage, description='Element percentage')
	opacity = widgets.FloatText(value=0.5, min=0, max=1, step=0.1, description='Opacity')
	save = widgets.Dropdown(options=[('True', True), ('False', False)], value=False, description='Save fig')
	ions_individually_plots = widgets.Dropdown(options=[('True', True), ('False', False)], value=False,
	                                           description='Ions individually plots')
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

	selected_area_specially_ph = widgets.Dropdown(options=[('False', False), ('True', True)],
	                                              description='Selected specially')
	selected_area_temporally_ph = widgets.Dropdown(options=[('False', False), ('True', True)],
	                                               description='Selected temporally')
	element_percentage_ph = widgets.Textarea(value=element_percentage, description='Element percentage')
	figname_heatmap = widgets.Text(value='heatmap', description='fig name')

	plot_heatmap_button.on_click(lambda b: plot_heatmap(b, variables, out))

	def plot_heatmap(b, variables, out):
		plot_heatmap_button.disabled = True
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
			                       element_percentage_ph.value, save=True)
		plot_heatmap_button.disabled = False

	selected_area_specially_pm = widgets.Dropdown(options=[('False', False), ('True', True)],
	                                              description='Selected specially')
	selected_area_temporally_pm = widgets.Dropdown(options=[('False', False), ('True', True)],
	                                               description='Selected temporally')
	peak_find_plot = widgets.Dropdown(options=[('True', True), ('False', False)], description='peak find')
	rangging = widgets.Dropdown(options=[('False', False), ('True', True)], description='rangging')
	bin_size_pm = widgets.FloatText(value=0.1, description='Bins size')
	lim_mc_pm = widgets.IntText(value=150, description='Limit mc')
	prominence = widgets.IntText(value=50, description='peak prominance:')
	distance = widgets.IntText(value=50, description='peak distance:')
	figname_mc = widgets.Text(value='mc', description='fig name')

	plot_mc_button.on_click(lambda b: plot_mc(b, variables, out))

	def plot_mc(b, variables, out):
		plot_mc_button.disabled = True
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
			                  print_info=False)

		plot_mc_button.disabled = False

	element_percentage_pp = widgets.Textarea(value=element_percentage, description='Element percentage')
	selected_area_specially_pp = widgets.Dropdown(options=[('False', False), ('True', True)],
	                                              description='Selected specially')
	selected_area_temporally_pp = widgets.Dropdown(options=[('False', False), ('True', True)],
	                                               description='Selected temporally')
	x_or_y_pp = widgets.Dropdown(options=['x', 'y'], value='x', description='X or Y')
	figname_p = widgets.Text(value='projection', description='fig name')

	plot_projection_button.on_click(lambda b: plot_projection(b, variables, out))

	def plot_projection(b, variables, out):
		plot_projection_button.disabled = True
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
			                          figname_p.value)
		plot_projection_button.disabled = False

	clear_button.on_click(lambda b: clear(b, out))

	def clear(b, out):
		with out:
			clear_output(True)
			print('')

	tab1 = widgets.VBox(
		children=[selected_area_temporally_pp, selected_area_specially_pp, x_or_y_pp, element_percentage_pp, figname_p,
		          plot_projection_button, clear_button])
	tab2 = widgets.VBox(
		children=[selected_area_temporally_p3, selected_area_specially_p3, rotary_fig_save_p3, element_percentage_p3,
		          ions_individually_plots, opacity,
		          figname_3d, save, plot_3d_button, clear_button])
	tab3 = widgets.VBox(
		children=[selected_area_temporally_pm, selected_area_specially_pm, bin_size_pm, prominence, distance, lim_mc_pm,
		          peak_find_plot, rangging, figname_mc,
		          plot_mc_button, clear_button])
	tab4 = widgets.VBox(
		children=[selected_area_temporally_ph, selected_area_specially_ph, element_percentage_ph, figname_heatmap,
		          plot_heatmap_button, clear_button])

	tab = widgets.Tab(children=[tab1, tab2, tab3, tab4])
	tab.set_title(0, 'projection')
	tab.set_title(1, '3d plot')
	tab.set_title(2, 'mc plot')
	tab.set_title(3, 'heatmap plot')

	out = Output()

	display(widgets.VBox(children=[tab]))
	display(out)
