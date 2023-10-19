import ipywidgets as widgets
from IPython.display import display
from ipywidgets import Output

from pyccapt.calibration.reconstructions import reconstruction

# Define a layout for labels to make them a fixed width
label_layout = widgets.Layout(width='200px')


def call_x_y_z_calculation(variables, flight_path_length, element_selected):
	# Call the function or perform calculations here
	# You can replace this with the actual implementation

	# For demonstration purposes, I'm just printing the inputs
	out = Output()
	avg_dens = element_selected.value[2]
	field_evap = element_selected.value[3]

	if variables.range_data.empty:
		element_percentage = str([0.01])
	else:
		element_percentage = [0.01] * len(variables.range_data['element'].tolist())
		element_percentage = str(element_percentage)

	# Create widgets with initial values
	kf_widget = widgets.FloatText(value=4)
	det_eff_widget = widgets.FloatText(value=0.7)
	icf_widget = widgets.FloatText(value=1.4)
	field_evap_widget = widgets.FloatText(value=field_evap)
	avg_dens_widget = widgets.FloatText(value=avg_dens)
	element_percentage_widget = widgets.Textarea(value=element_percentage)
	rotary_fig_save_widget = widgets.Dropdown(options=[('True', True), ('False', False)], value=False)
	figname_widget = widgets.Text(value='3d')
	mode_widget = widgets.Dropdown(options=[('Gault', 'Gault'), ('Bas', 'Bas')])
	opacity_widget = widgets.FloatText(value=0.5)
	save_widget = widgets.Dropdown(options=[('True', True), ('False', False)], value=False)

	# Create a button widget to trigger the function
	button_calculate_plot = widgets.Button(description="reconstruct & plot")

	def on_button_click(b, variables, flight_path_length):
		# Disable the button while the code is running
		button_calculate_plot.disabled = True

		# Get the values from the widgets
		kf_value = kf_widget.value
		det_eff_value = det_eff_widget.value
		icf_value = icf_widget.value
		field_evap_value = field_evap_widget.value
		avg_dens_value = avg_dens_widget.value
		element_percentage_value = element_percentage_widget.value
		rotary_fig_save_value = rotary_fig_save_widget.value
		figname_value = figname_widget.value
		mode_value = mode_widget.value
		opacity_value = opacity_widget.value
		save_value = save_widget.value

		with out:
			out.clear_output()
			# Call the function
			reconstruction.x_y_z_calculation_and_plot(
				kf=kf_value,
				det_eff=det_eff_value,
				icf=icf_value,
				field_evap=field_evap_value,
				avg_dens=avg_dens_value,
				element_percentage=element_percentage_value,
				rotary_fig_save=rotary_fig_save_value,
				variables=variables,
				flight_path_length=flight_path_length.value,
				selected_are=False,
				figname=figname_value,
				mode=mode_value,
				opacity=opacity_value,
				save=save_value)

		# Enable the button when the code is finished
		button_calculate_plot.disabled = False

	button_calculate_plot.on_click(lambda b: on_button_click(b, variables, flight_path_length))

	widget_container = widgets.VBox([
		widgets.HBox([widgets.Label(value='KF:', layout=label_layout), kf_widget, widgets.Label(value='(eV/nm)')]),
		widgets.HBox([widgets.Label(value='Det_eff:', layout=label_layout), det_eff_widget]),
		widgets.HBox([widgets.Label(value='ICF:', layout=label_layout), icf_widget]),
		widgets.HBox([widgets.Label(value='Field_evap:', layout=label_layout), field_evap_widget,
		              widgets.Label(value='(V/nm)')]),
		widgets.HBox([widgets.Label(value='Avg_dens:', layout=label_layout), avg_dens_widget,
		              widgets.Label(value='(amu/nm^3)')]),
		widgets.HBox([widgets.Label(value='Element_percentage:', layout=label_layout), element_percentage_widget]),
		widgets.HBox([widgets.Label(value='Rotary_fig_save:', layout=label_layout), rotary_fig_save_widget]),
		widgets.HBox([widgets.Label(value='Fig name:', layout=label_layout), figname_widget]),
		widgets.HBox([widgets.Label(value='Save fig:', layout=label_layout), save_widget]),
		widgets.HBox([widgets.Label(value='Mode:', layout=label_layout), mode_widget]),
		widgets.HBox([widgets.Label(value='Opacity:', layout=label_layout), opacity_widget]),
		widgets.HBox([button_calculate_plot]),
	])

	display(widget_container)
	display(out)
